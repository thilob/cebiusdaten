# cebiusdaten

Gebäudereferenzen können hier abgerufen werden:
<https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/>

## Dokumentierte Änderungen

Stand: 15.03.2026

- Die Dateinamenerzeugung wurde auf `python-slugify` umgestellt.
- Das bisherige Dateinamenschema bleibt erhalten: Kreis und Gemeinde werden mit Unterstrich getrennt, Umlaute bleiben in den Ausgabedateien erhalten.
- Die alte, nicht mit Python 3 kompatible Abhängigkeit `slugify==0.0.1` wurde ersetzt.
- `requirements.txt` wurde auf die direkt für das Projekt benötigten Pakete reduziert:
  `geopandas`, `pandas`, `python-slugify`, `requests`, `rich`, `tqdm`.
- Die lokale virtuelle Umgebung wurde bereinigt; nicht benötigte Alt- und Fremdpakete wurden entfernt.
