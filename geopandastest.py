import os
import shutil
import requests
import pandas as pd
import geopandas as gpd

url="https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/gebref_EPSG25832_ASCII.zip"

def main():
    # Datendatei herunterladen
    print("Gebäudereferenzen werden heruntergeladen....")
    r = requests.get(url, allow_redirects=True)
    open('gebref.zip', 'wb').write(r.content)
    # Datendatei entpacken
    print('Gebäudereferenzen werden entpackt...')
    shutil.unpack_archive("gebref.zip")
    print("Gebäudereferenzen wurden entpackt!")
    if not (os.path.exists('output')):
        os.mkdir('output')
    # Datendatei in ein GeoDataFrame einlesen
    df = pd.read_csv('gebref.txt')
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    # Geodaten transformieren
    gdf = gdf.set_crs("EPSG:4326")
    gdf = gdf.to_crs("EPSG:31466")
    print(gdf)
    # Geodaten speichern
    # Datendatei und Zipfile löschen
    
    

if __name__ == "__main__":
    main()