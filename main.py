"""Importe"""

import os
import shutil
import requests
import pandas as pd
import geopandas as gpd
from slugify import slugify
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from tqdm import tqdm
from datetime import datetime, timedelta


url = "https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/gebref_EPSG25832_ASCII.zip"


class GeoDataProcessor:
    """
    Eine Klasse zur Verarbeitung von Geodaten zum Zwecke des Hausnummernimports in eCebius.
    Der Ablauf skizziert sich wie folgt:
        1. Ist eine Gebäudereferenzdatei (gebref.txt) vorhanden und aktuell?
        2. Herunterladen und Entpacken der Gebäudereferenzen, falls erforderlich.
        3. Laden der Daten aus der Datei 'gebref.txt' und Verarbeitung in einem GeoDataFrame.
        4. Gruppieren und Sortieren der Daten nach Land, Regierungsbezirk und Landkreis.
        5. Anzeigen der gruppierten und sortierten Werte und Auswahl eines Landkreises.
        6. Speichern der Gemeindeliste des ausgewählten Landkreises in der Datei __Gemeindeliste.txt.
        7. Speichern aller Straßen und Hausnummern des ausgewählten Landkreises in separaten Dateien.

    Attribute:
        gdf (GeoDataFrame): Das GeoDataFrame, das die geladenen und verarbeiteten Daten enthält.
        url (str): Die URL zum Herunterladen der Gebäudereferenzen.
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
        if not os.path.exists(
            "gebref.txt"
        ):  # Prüfen, ob die Datei 'gebref.txt' vorhanden ist
            download = True
        else:
            file_mod_time = datetime.fromtimestamp(os.path.getmtime("gebref.txt"))
            if datetime.now() - file_mod_time > timedelta(
                hours=24
            ):  # Prüfen, ob die Datei älter als 24 Stunden ist
                download = True

        if download:
            print("Gebäudereferenzen werden heruntergeladen....")
            r = requests.get(self.url, allow_redirects=True)
            with open("gebref.zip", "wb") as f:
                f.write(r.content)
            print("Gebäudereferenzen werden entpackt...")
            shutil.unpack_archive("gebref.zip")
            print("Gebäudereferenzen wurden entpackt!")
            if not os.path.exists("output"):
                os.mkdir("output")  # Erstellen des Ausgabeverzeichnisses
        else:
            print(
                "Die Datei 'gebref.txt' ist bereits vorhanden und aktuell. Es wird keine neue Datei heruntergeladen."
            )

    def load_data(self):
        """
        Lädt die Daten aus der Datei 'gebref.txt' und verarbeitet sie.
        """
        chunks = []
        expected_columns = [  # Entspricht den Spaltennamen in der Datei 'gebref.txt'
            "nba",
            "oid",
            "qua",
            "landschl",
            "land",
            "regbezschl",
            "regbez",
            "kreisschl",
            "kreis",
            "gmdschl",
            "gmd",
            "ottschl",
            "ott",
            "strschl",
            "str",
            "hnr",
            "adz",
            "zone",
            "ostwert",
            "nordwert",
            "datum",
        ]
        """Verarbeitung in Chunks

            Der folgende Abschnitt liest die große Datenmenge in Chunks von 10000 Zeilen ein und überprüft die Anzahl der Spalten.
            Fehlerhafte Spalten werden auf dem Bildschirm ausgegeben.
            Die Verwendung von Chunks erfolgt wegen der deutlich besseren Performance gegenüber zeilenweiem Einlesen 
            oder der Verwendung einer zusätzlichen Datenbank.
            
        """
        with open("gebref.txt", "r", encoding="utf-8") as file:
            total_lines = sum(1 for line in file)
            file.seek(0)
            for chunk in tqdm(
                pd.read_csv(
                    file,
                    header=None,
                    sep=";",
                    chunksize=10000,
                    na_filter=False,
                    on_bad_lines="skip",
                    encoding="utf-8",
                ),
                total=total_lines // 10000,
                desc="Einlesen der Datei ",
            ):
                if len(chunk.columns) != len(expected_columns):
                    print(f"Fehlerhafte Zeile: {chunk}")
                    raise ValueError(
                        "Fehlerhafte Zeile gefunden. Die Zeile wird übersprungen."
                    )
                chunks.append(chunk)

        df = pd.concat(chunks, ignore_index=True)
        if len(df.columns) != len(expected_columns):
            raise ValueError(
                f"Anzahl der Spalten stimmt nicht überein. Erwartet: {len(expected_columns)}, Gefunden: {len(df.columns)}"
            )
        df.columns = expected_columns
        print("Spaltennamen:", df.columns)  # Ausgabe der Spaltennamen
        self.gdf = gpd.GeoDataFrame(  # Ost- und Nordwert werden in einen Geopandas-GeoDataFrame umgewandelt
            df, geometry=gpd.points_from_xy(df["ostwert"], df["nordwert"])
        )
        self.gdf = self.gdf.set_crs(
            "EPSG:25832"  # Im Original werden die Geodaten im Koordinatensystem EPSG:25832 ("UTM 32N") geliefert
        )
        self.gdf = self.gdf.to_crs(
            "EPSG:31466"  # Transformieren in das von Cebius verwendete Koordinatensystem EPSG:31466 ("Gauss-Krüger 2")
        )
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
        self.gdf = self.gdf[self.gdf[filter_column] == filter_value].sort_values(
            by=sort_columns
        )

    def clean_up(self):
        """
        Entfernt die heruntergeladene ZIP-Datei.
        """
        if os.path.exists("gebref.zip"):
            os.remove("gebref.zip")

    def output_leeren(self):
        """
        Löscht alle Dateien im Unterverzeichnis 'output'.
        """
        output_dir = "output"
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Datei '{file_path}' wurde gelöscht.")
            except Exception as e:
                print(f"Fehler beim Löschen der Datei '{file_path}': {e}")

    def GemeindelisteAusgeben(self, gdf, landkreis):
        """
        Gruppiert und sortiert die Daten nach 'landschl', 'regbezschl', 'kreisschl', 'gmdschl' und 'gmd' und speichert sie in einer Textdatei.
        Die Textdatei wird von Cebius als Referenz zwischen Gemeindename und verschiedener Schlüsselnummern benötigt.

        Args:
            gdf (GeoDataFrame): Das GeoDataFrame, das die Daten enthält.
            filename (str): Der Name der Datei, in die die gruppierten und sortierten Daten gespeichert werden sollen.
        """
        filename = "output/__Gemeindeliste.txt"
        filtered_gdf = gdf[gdf["kreis"] == landkreis]
        grouped_sorted_df = (
            filtered_gdf.groupby(
                ["landschl", "regbezschl", "kreisschl", "gmdschl", "gmd"]
            )
            .size()
            .reset_index(name="count")
        )
        grouped_sorted_df = grouped_sorted_df.sort_values(
            by=["landschl", "regbezschl", "kreisschl", "gmdschl", "gmd"]
        )
        with open(filename, "w", encoding="utf-8") as file:
            for _, zeile in grouped_sorted_df.iterrows():
                file.write(
                    f"{int(zeile['landschl']):02d};{zeile['regbezschl']};{zeile['kreisschl']};{int(zeile['gmdschl']):03d};-;{zeile['gmd']}\n"
                )

        print(f"Gemeindeliste mit Schlüsselwerten wurden in '{filename}' gespeichert.")

    def save_gmd_str_values(self, kreis_value, gdf):
        """
        Speichert alle Straßen einer Gemeinde in einer Textdatei und alle Hausnummern mit Geokoordinaten in einer zweiten Textdatei.

        Args:
            kreis_value (str): Der Wert aus der Spalte 'kreis', nach dem gefiltert werden soll.
        """
        # Filtere die Daten nach dem angegebenen 'kreis'-Wert
        filtered_gdf = gdf[gdf["kreis"] == kreis_value]

        # Ermittle alle eindeutigen Werte aus 'gmd', die zu 'kreis' gehören
        unique_gmd_values = filtered_gdf["gmd"].unique()

        for gmd_value in unique_gmd_values:
            # Filtere die Daten nach dem aktuellen 'gmd'-Wert
            gmd_filtered_gdf = filtered_gdf[filtered_gdf["gmd"] == gmd_value]
            gmd_filtered_gdf = (
                gmd_filtered_gdf.groupby(
                    [
                        "landschl",
                        "regbezschl",
                        "kreisschl",
                        "gmdschl",
                        "gmd",
                        "strschl",
                        "str",
                    ]
                )
                .size()
                .reset_index(name="count")
            )
            gmd_filtered_gdf = gmd_filtered_gdf.sort_values(
                by=[
                    "landschl",
                    "regbezschl",
                    "kreisschl",
                    "gmdschl",
                    "gmd",
                    "strschl",
                    "str",
                ]
            )

            # Bewahrt das bisherige Dateinamenschema mit Umlauten und Trenner-Unterstrich.
            base_filename = (
                f"{slugify(kreis_value, allow_unicode=True)}_"
                f"{slugify(gmd_value, allow_unicode=True)}"
            )

            # Erstellt eine Textdatei mit allen Straßen einer Gemeinde samt Schlüsselwerten
            filename = "output/" + base_filename + "_strassen.txt"
            with open(filename, "w", encoding="utf-8") as file:
                for _, zeile in gmd_filtered_gdf.iterrows():
                    file.write(
                        f"{int(zeile['landschl']):02d};{zeile['regbezschl']};{zeile['kreisschl']};{int(zeile['gmdschl']):03d};{zeile['strschl']};0;{zeile['str']}\n"
                    )
            print(f"Alle Straßen aus '{gmd_value}' wurden in '{filename}' gespeichert.")

            # Erstellt eine zweite Textdatei mit den Hausnummernkoordinaten aller Straßen einer Gemeinde
            filename_hnr = "output/" + base_filename + "_hausnummern.txt"
            gmd_filtered_gdf = filtered_gdf[filtered_gdf["gmd"] == gmd_value]
            gmd_filtered_gdf = (
                gmd_filtered_gdf.groupby(
                    [
                        "landschl",
                        "regbezschl",
                        "kreisschl",
                        "gmdschl",
                        "gmd",
                        "strschl",
                        "str",
                        "hnr",
                        "adz",
                        "geometry",
                    ]
                )
                .size()
                .reset_index(name="count")
            )
            gmd_filtered_gdf = gmd_filtered_gdf.sort_values(
                by=[
                    "landschl",
                    "regbezschl",
                    "kreisschl",
                    "gmdschl",
                    "gmd",
                    "strschl",
                    "str",
                    "hnr",
                    "adz",
                    "geometry",
                ]
            )

            with open(filename_hnr, "w", encoding="utf-8") as file:
                for _, zeile in gmd_filtered_gdf.iterrows():
                    file.write(
                        f"{int(zeile['landschl']):02d};{zeile['regbezschl']};{zeile['kreisschl']};{int(zeile['gmdschl']):03d};{zeile['strschl']};{zeile['hnr']};{zeile['adz']};{zeile['geometry'].x};{zeile['geometry'].y};A;00\n"
                    )
            print(
                f"Alle Hausnummern und Geokoordinaten, die zu '{gmd_value}' gehören, wurden in '{filename_hnr}' gespeichert."
            )

    def clearScreen(self):
        if os.name == "nt":  # for windows
            _ = os.system("cls")
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = os.system("clear")

    def HinweiseAusgeben(self):
        """Gibt die Hinweise zum Programmstart aus."""
        self.clearScreen()
        print("Cebius-Hausnummerntool - Thilo Berger, 2025")
        print("=================================================")
        print()

    def display_paginated_list(self, items, page_size=20):
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
            self.clearScreen()
            self.HinweiseAusgeben()
            table = Table(title=f"Seite {current_page + 1} von {total_pages}")
            table.add_column("Nummer", justify="right", style="cyan", no_wrap=True)
            table.add_column("Wert", style="magenta")

            for i, item in enumerate(page_items, start=start_index + 1):
                table.add_row(str(i), str(item))

            console.print(table)

            if current_page < total_pages - 1:
                next_page = console.input(
                    "Drücken Sie Enter für die nächste Seite, geben Sie die Nummer zum Auswählen ein oder 'q' zum Beenden: "
                )
                if next_page.lower() == "q":
                    return None
                elif next_page.isdigit() and int(next_page) in range(
                    start_index + 1, end_index + 1
                ):
                    return items[int(next_page) - 1]
                else:
                    console.print(
                        Panel(
                            "Ungültige Eingabe. Bitte versuchen Sie es erneut.",
                            style="red",
                        )
                    )
                current_page += 1
            else:
                selection = console.input(
                    "Geben Sie die Nummer zum Auswählen ein oder 'q' zum Beenden: "
                )
                if selection.lower() == "q":
                    return None
                elif selection.isdigit() and int(selection) in range(
                    start_index + 1, end_index + 1
                ):
                    return items[int(selection) - 1]
                else:
                    console.print(
                        Panel(
                            "Ungültige Eingabe. Bitte versuchen Sie es erneut.",
                            style="red",
                        )
                    )
                break


def main():
    """
    Hauptfunktion des Programms. Führt den gesamten Prozess der Datenverarbeitung durch.
    """
    processor = GeoDataProcessor(url)
    processor.HinweiseAusgeben()
    processor.download_and_extract()
    processor.load_data()
    processor.output_leeren()
    # Gruppieren und sortieren
    group_column = "kreis"  # Gruppieren nach der Spalte 'kreis'
    grouped_values = processor.group_and_sort(group_column)

    # Gruppierte und sortierte Werte seitenweise anzeigen und Auswahl treffen
    filter_value = processor.display_paginated_list(grouped_values)
    if filter_value is None:
        print("Keine Auswahl getroffen. Programm wird beendet.")
        return
    else:
        processor.GemeindelisteAusgeben(processor.gdf, filter_value)
        processor.save_gmd_str_values(filter_value, processor.gdf)

    # Filtern und sortieren
    sort_columns = ["land", "gmdschl", "strschl"]  # Beispielspalten zum Sortieren
    processor.filter_and_sort_data(group_column, filter_value, sort_columns)

    # processor.save_data()
    processor.clean_up()

    """_summary_
    """


if __name__ == "__main__":
    main()
