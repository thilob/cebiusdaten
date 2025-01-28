import os
import shutil
import requests
import pandas as pd
import geopandas as gpd
from io import StringIO
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from tqdm import tqdm
from datetime import datetime, timedelta

url = "https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/gebref_EPSG25832_ASCII.zip"

class GeoDataProcessor:
    """
    Eine Klasse zur Verarbeitung von Geodaten.

    Attribute:
        url (str): Die URL zum Herunterladen der Daten.
        gdf (GeoDataFrame): Das GeoDataFrame, das die geladenen und verarbeiteten Daten enthält.
    """

    def __init__(self, url):
        """
        Initialisiert die GeoDataProcessor-Klasse mit der angegebenen URL.

        Args:
            url (str): Die URL zum Herunterladen der Daten.
        """
        self.url = url
        self.gdf = None

    def download_and_extract(self):
        """
        Lädt die Gebäudereferenzdaten herunter und extrahiert sie, wenn die Datei 'gebref.txt' nicht vorhanden ist
        oder älter als 24 Stunden ist.
        """
        download = False
        if not os.path.exists('gebref.txt'):
            download = True
        else:
            file_mod_time = datetime.fromtimestamp(os.path.getmtime('gebref.txt'))
            if datetime.now() - file_mod_time > timedelta(hours=24):
                download = True

        if download:
            print("Gebäudereferenzen werden heruntergeladen....")
            r = requests.get(self.url, allow_redirects=True)
            with open('gebref.zip', 'wb') as f:
                f.write(r.content)
            print('Gebäudereferenzen werden entpackt...')
            shutil.unpack_archive("gebref.zip")
            print("Gebäudereferenzen wurden entpackt!")
            if not os.path.exists('output'):
                os.mkdir('output')
        else:
            print("Die Datei 'gebref.txt' ist bereits vorhanden und aktuell. Es wird keine neue Datei heruntergeladen.")

    def load_data(self):
        """
        Lädt die Daten aus der Datei 'gebref.txt' und verarbeitet sie.
        """
        chunks = []
        expected_columns = [
            "nba", "oid", "qua", "landschl", "land", "regbezschl", "regbez", "kreisschl", "kreis", "gmdschl",
            "gmd", "ottschl", "ott", "strschl", "str", "hnr", "adz", "zone", "ostwert", "nordwert", "datum"
        ]
        with open('gebref.txt', 'r', encoding='utf-8') as file:
            total_lines = sum(1 for line in file)
            file.seek(0)
            for chunk in tqdm(pd.read_csv(file, header=None, sep=';', chunksize=10000, na_filter=False, on_bad_lines='skip', encoding='utf-8'), total=total_lines//10000, desc="Einlesen der Datei"):
                if len(chunk.columns) != len(expected_columns):
                    print(f"Fehlerhafte Zeile: {chunk}")
                    raise ValueError("Fehlerhafte Zeile gefunden. Programm wird beendet.")
                chunks.append(chunk)

        df = pd.concat(chunks, ignore_index=True)
        if len(df.columns) != len(expected_columns):
            raise ValueError(f"Anzahl der Spalten stimmt nicht überein. Erwartet: {len(expected_columns)}, Gefunden: {len(df.columns)}")
        df.columns = expected_columns
        print("Spaltennamen:", df.columns)  # Ausgabe der Spaltennamen
        self.gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['ostwert'], df['nordwert']))
        self.gdf = self.gdf.set_crs("EPSG:25832")  # Setzen des Koordinatensystems EPSG:25832
        self.gdf = self.gdf.to_crs("EPSG:31466")  # Transformieren in das gewünschte Koordinatensystem EPSG:31466
        print(self.gdf)

    def group_and_sort(self, group_column):
        """
        Gruppiert und sortiert die Daten nach der angegebenen Spalte.

        Args:
            group_column (str): Die Spalte, nach der gruppiert und sortiert werden soll.

        Returns:
            list: Eine Liste der gruppierten und sortierten Werte.
        """
        grouped = self.gdf[group_column].value_counts().sort_index()
        return grouped.index.tolist()

    def filter_and_sort_data(self, filter_column, filter_value, sort_columns):
        """
        Filtert und sortiert die Daten nach den angegebenen Spalten.

        Args:
            filter_column (str): Die Spalte, nach der gefiltert werden soll.
            filter_value (str): Der Wert, nach dem gefiltert werden soll.
            sort_columns (list): Die Spalten, nach denen sortiert werden soll.
        """
        self.gdf = self.gdf[self.gdf[filter_column] == filter_value].sort_values(by=sort_columns)

    def save_data(self):
        """
        Speichert die gefilterten und sortierten Daten in separaten Dateien für jeden Wert der Spalte 'gmd'.
        """
        unique_gmd_values = self.gdf['gmd'].unique()
        for value in unique_gmd_values:
            df_filtered = self.gdf[self.gdf['gmd'] == value]
            filename = f"output/{value}.txt"
            df_filtered.to_csv(filename, index=False, sep=';', encoding='utf-8')
            print(f"Gefilterte und sortierte Daten für '{value}' wurden in '{filename}' gespeichert.")

    def clean_up(self):
        """
        Entfernt die heruntergeladene ZIP-Datei.
        """
        if os.path.exists('gebref.zip'):
            os.remove('gebref.zip')

def display_paginated_list(items, page_size=20):
    """
    Zeigt eine paginierte Liste von Elementen an und ermöglicht die Auswahl eines Elements.

    Args:
        items (list): Die Liste der anzuzeigenden Elemente.
        page_size (int): Die Anzahl der Elemente pro Seite.

    Returns:
        str: Das ausgewählte Element oder None, wenn keine Auswahl getroffen wurde.
    """
    console = Console()
    total_pages = (len(items) + page_size - 1) // page_size
    current_page = 0

    while True:
        start_index = current_page * page_size
        end_index = start_index + page_size
        page_items = items[start_index:end_index]

        table = Table(title=f"Seite {current_page + 1} von {total_pages}")
        table.add_column("Nummer", justify="right", style="cyan", no_wrap=True)
        table.add_column("Wert", style="magenta")

        for i, item in enumerate(page_items, start=start_index + 1):
            table.add_row(str(i), str(item))

        console.print(table)

        if current_page < total_pages - 1:
            next_page = console.input("Drücken Sie Enter für die nächste Seite, geben Sie die Nummer zum Auswählen ein oder 'q' zum Beenden: ")
            if next_page.lower() == 'q':
                return None
            elif next_page.isdigit() and int(next_page) in range(start_index + 1, end_index + 1):
                return items[int(next_page) - 1]
            else:
                console.print(Panel("Ungültige Eingabe. Bitte versuchen Sie es erneut.", style="red"))
            current_page += 1
        else:
            selection = console.input("Geben Sie die Nummer zum Auswählen ein oder 'q' zum Beenden: ")
            if selection.lower() == 'q':
                return None
            elif selection.isdigit() and int(selection) in range(start_index + 1, end_index + 1):
                return items[int(selection) - 1]
            else:
                console.print(Panel("Ungültige Eingabe. Bitte versuchen Sie es erneut.", style="red"))
            break

def print_police_car():
    """
    Gibt eine ASCII-Grafik eines Polizeiautos mit Blaulicht aus.
    """
    police_car = """
\033[1;34m
       _______
  ____//  __|___
 |___    ___   |
     |  |   |  |
     |__|___|__|
    (o)     (o)
\033[0m
    """
    print(police_car)
    
    
def GemeindelisteAusgeben(gdf):
    """
    Gruppiert und sortiert die Daten nach den angegebenen Spalten und speichert sie in einer Datei.

    Args:
        gdf (GeoDataFrame): Das GeoDataFrame, das die Daten enthält.
        filename (str): Der Name der Datei, in die die gruppierten und sortierten Daten gespeichert werden sollen.
    """
    filename='output/__Gemeindeliste.txt'
    grouped_sorted_df = gdf.groupby(['landschl', 'regbezschl', 'kreisschl', 'gmdschl', 'gmd']).size().reset_index(name='count')
    grouped_sorted_df = grouped_sorted_df.sort_values(by=['landschl', 'regbezschl', 'kreisschl', 'gmdschl', 'gmd'])
#    grouped_sorted_df.to_csv(filename, index=False, sep=';', encoding='utf-8')
    with open(filename, 'w', encoding='utf-8') as file:
        for _, zeile in grouped_sorted_df.iterrows():
            file.write(f"{int(zeile['landschl']):02d};{zeile['regbezschl']};{zeile['kreisschl']};{int(zeile['gmdschl']):03d};-;{zeile['gmd']}\n")    
            
    print(f"Gruppierte und sortierte Daten wurden in '{filename}' gespeichert.")

def save_gmd_str_values(kreis_value, gdf):
    """
    Speichert alle eindeutigen Werte aus 'str', die zu 'gmd' gehören, in einer Textdatei.

    Args:
        kreis_value (str): Der Wert aus der Spalte 'kreis', nach dem gefiltert werden soll.
    """
    # Filtere die Daten nach dem angegebenen 'kreis'-Wert
    filtered_gdf = gdf[gdf['kreis'] == kreis_value]

    # Ermittle alle eindeutigen Werte aus 'gmd', die zu 'kreis' gehören
    unique_gmd_values = filtered_gdf['gmd'].unique()

    for gmd_value in unique_gmd_values:
        # Filtere die Daten nach dem aktuellen 'gmd'-Wert
        gmd_filtered_gdf = filtered_gdf[filtered_gdf['gmd'] == gmd_value]

        # Ermittle alle eindeutigen Werte aus 'str', die zu 'gmd' gehören
        unique_str_values = gmd_filtered_gdf['str'].unique()

        # Erstelle eine Textdatei mit dem Namen aus 'gmd'
        filename = f"output/{gmd_value}_str.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            for str_value in unique_str_values:
                file.write(f"{str_value}\n")

        print(f"Alle Werte aus 'str', die zu '{gmd_value}' gehören, wurden in '{filename}' gespeichert.")
        # Erstelle eine zweite Textdatei mit dem Namen aus 'gmd' + "Hausnummern"
        filename_hnr = f"output/{gmd_value}_Hausnummern.txt"
# The code snippet you provided is writing the house numbers (`hnr`) along with the corresponding
# geographical coordinates (latitude and longitude) of each row in the filtered GeoDataFrame
# (`gmd_filtered_gdf`) to a text file.
        with open(filename_hnr, 'w', encoding='utf-8') as file:
            for _, row in gmd_filtered_gdf.iterrows():
             #   print("Spaltennamen:", gmd_filtered_gdf.columns.tolist())
                file.write(f"{row['hnr']};{row['geometry'].x};{row['geometry'].y}\n")
# row['hnr'] = f"{int(row['hnr']):03d}"  # Formatieren der Hausnummern als 3-stellige Zahlen
# row['hnr'] = f"{row['hnr']:>20}"  # Formatieren der Hausnummern als rechtsbündige Strings

        print(f"Alle Hausnummern und Geokoordinaten, die zu '{gmd_value}' gehören, wurden in '{filename_hnr}' gespeichert.")


def main():
    """
    Hauptfunktion des Programms. Führt den gesamten Prozess der Datenverarbeitung durch.
    """
    processor = GeoDataProcessor(url)
    processor.download_and_extract()
    processor.load_data()
    
    # Gruppieren und sortieren
    group_column = 'kreis'  # Gruppieren nach der Spalte 'kreis'
    grouped_values = processor.group_and_sort(group_column)
    
    # Gruppierte und sortierte Werte seitenweise anzeigen und Auswahl treffen
    filter_value = display_paginated_list(grouped_values)
    if filter_value is None:
        print("Keine Auswahl getroffen. Programm wird beendet.")
        return
    else:
        GemeindelisteAusgeben(processor.gdf)
        save_gmd_str_values(filter_value, processor.gdf)
    
    # Filtern und sortieren
    sort_columns = ['land', 'gmd']  # Beispielspalten zum Sortieren
    processor.filter_and_sort_data(group_column, filter_value, sort_columns)
    processor.save_data()
    processor.clean_up()

    # ASCII-Grafik eines Polizeiautos ausgeben
    print_police_car()

if __name__ == "__main__":
    main()