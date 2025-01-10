"""Importe
"""
import re
import os
import glob
import requests
import slugify
import psycopg2
import shutil
import psycopg2.extras
from PySide6 import QtWidgets
from DatenDialog_ui import Ui_datenDialog

"""Initialer Aufbau des Datenbank-Verbindung
Der Cursor wird anschließend im weiteren Programm verwendet.
"""
print("Programm gestartet")
conn = psycopg2.connect(
    "dbname=cebiusdaten user=cebiusdaten password=cebiusdaten")
cur = conn.cursor()
print("Verbindung hergestellt")


def GebrefLadenUndEntpacken(url):
    """falls aktiviert, läd die Funktion die gezippte Gebäudereferenzdatei herunter und entpackt sie
    Args:
        url (URL-String): Die zum Download verwendete URL. Kann in der GUI angepasst werden.
    """
    print("Gebäudereferenzen werden heruntergeladen....")
    r = requests.get(url, allow_redirects=True)
    open('gebref.zip', 'wb').write(r.content)
    print('Gebäudereferenzen werden entpackt...')
    shutil.unpack_archive("gebref.zip")
    print("Gebäudereferenzen wurden entpackt!")


def StrassentabelleAusgeben(Kreis, Gemeindename):
    curgem = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    SQL = "select * from gebref where gmd='{}'".format(Gemeindename)
    print(SQL)
    curgem.execute(SQL)
    print("Nach Execute:  ")
    row_count = 0
    zeile1 = ""
    for row in curgem:
        row_count += 1
        print(row_count)
        zeile1 = row['landschl'] + ";" + row['regbezschl'] + \
            ";" + row['kreisschl'] + ";" + row['gmdschl'] + ";"

    F2 = open("./output/" + slugify.slugify(Kreis) + "_" + slugify.slugify(Gemeindename) +
              "_Strassen.txt", "w", encoding="windows-1252", newline='\r\n')
    # F2 = open("./output/" + slugify.slugify(Kreis) + "_" + slugify.slugify(Gemeindename) + "_Strassen.txt", "w")
    curstrasse = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    SQL2 = "select distinct strschl, str from gebref where gmd='" + \
        Gemeindename + "' order by str"
    curstrasse.execute(SQL2)
    # print(SQL2)
    records = curstrasse.fetchall()
    for strasse in records:
        zeile = strasse["strschl"] + ";0;" + strasse["str"] + "\n"
        zeile2 = str(zeile1) + str(zeile)
        F2.write(zeile2)
    F2.close()


def HausnummerntabelleAusgeben(Kreis, Gemeindename):
    curgem = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    SQL = "select * from gebref where gmd='{}'".format(Gemeindename)
    print(SQL)
    curgem.execute(SQL)
    print("Nach Execute")
    row_count = 0
    zeile1 = ""
    for row in curgem:
        row_count += 1
        print(row_count)
        zeile1 = row['landschl'] + ";" + row['regbezschl'] + \
            ";" + row['kreisschl'] + ";" + row['gmdschl'] + ";"

    F2 = open("./output/" + slugify.slugify(Kreis) + "_" + slugify.slugify(Gemeindename) +
              "_Hausnummern.txt", "w", encoding="windows-1252", newline='\r\n')
    curstrasse = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    SQL2 = "select strschl, hnr, adz, st_x(geom31466)::text as x, st_y(geom31466)::text as y  from " \
           "gebref where gmd='" + Gemeindename + "' order by str,hnr"
    curstrasse.execute(SQL2)
    print(SQL2)
    records = curstrasse.fetchall()
    for strasse in records:
        zeile = strasse["strschl"] + ";" + strasse["hnr"] + ";" + strasse["adz"] \
            + ";001;" + strasse["x"] + ";" + strasse["y"] + ";A;00\n"
        zeile2 = str(zeile1) + str(zeile)
        print(zeile2)
        F2.write(zeile2)
    F2.close()


def truncateGebref():
    """Gebäudereferenztabellen leeren
    """
    cur.execute("truncate gebref")


""" def gemeindeschluessel_einlesen():
    # Aktuelle Daten des Gemeindeschlüssels einlesen
    cur.execute("truncate gebref_schluessel")
    F = open("gebref_schluessel.txt", "r", encoding="utf-8")
    for line in F:
        line = line.strip()
        while line.count(";") < 5:
            line = line + ";"
        print(line + "     " + str(line.count(";")))
        m = re.split(';', line)
        print(m[0] + "  " + str(m[5]))
        SQL = "insert into gebref_schluessel (field_1,field_2,field_3,field_4,field_5,field_6) values (%s,%s,%s,%s,%s,%s);"
        data = (m[0], m[1], m[2], m[3], m[4], m[5])
        cur.execute(SQL, data)
    conn.commit() """


def gebaeudereferenzen_einlesen(nurOberbergLaden):
    print("Lese Gebäudereferenzen ein. Dies kann etwas dauern ......")
    # Aktuelle Gebäudereferenzen des Landes einlesen
    F = open("gebref.txt", "r", encoding="utf-8")
    i = -1
    cur.execute("truncate gebref")
    for line in F:
        line = line.strip()
        m = re.split(';', line)
        # print ('Spalten:' + str(len(m)))
        punkt = "POINT(" + m[18].replace(",", ".") + \
            " " + m[19].replace(",", ".") + ")"
        SQL = """INSERT INTO public.gebref(nba, oid, qua, landschl, land, regbezschl, regbez, kreisschl, kreis, gmdschl, gmd, ottschl, ott, strschl, str, hnr, adz, zone, ostwert, nordwert, datum, geom25832)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], m[9], m[10],
                m[11], m[12], m[13], m[14], m[15], m[16], m[17], m[18], m[19], m[20], punkt)
        if (nurOberbergLaden):
            if m[3] == "05" and m[5] == '3' and m[7] == '74':
                if i >= 0:
                    cur.execute(SQL, data)
                if i == 1000:
                    conn.commit()
                    i = 0
                    print("\r" + m[1])
                i += 1
        else:
            if i >= 0:
                cur.execute(SQL, data)
            if i == 1000:
                conn.commit()
                i = 0
                print("\r" + m[1])
            i += 1

    print('Geom31466 erstellen')
    SQL = 'update gebref set geom31466=st_transform(geom25832,31466)'
    cur.execute(SQL)
    conn.commit()
    print("\rFertig!")


class DatenDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super(DatenDialog, self).__init__()
        self.ui = Ui_datenDialog()
        self.ui.setupUi(self)
        self.ui.abbrechen.clicked.connect(self.abbrechen)
        self.ui.starten.clicked.connect(self.weiter)

    def abbrechen(self):
        print("abbrechen")
        exit(1)

    def weiter(self):
        if (self.ui.checkBoxCleanOutput.isChecked()):
            # Getting All Files List
            fileList = glob.glob('output/*.txt', recursive=True)
            # Remove all files one by one
            for file in fileList:
                try:
                    os.remove(file)
                except OSError:
                    print("Error while deleting file")

        ausfuehren(self.ui.importGebref.isChecked(
        ), self.ui.exportCebius.isChecked(), self.ui.CheckboxGebrefHolen.isChecked(), self.ui.UrlGebrefHolen.text(), self.ui.checkBoxNurOberbergLaden.isChecked())

        exit(0)


def ausfuehren(importGebref,  exportCebius, gebrefHolen, gebrefUrl, checkBoxNurOberbergLaden):
    print("ausführen wurde aufgerufen!")

    if (gebrefHolen):
        GebrefLadenUndEntpacken(gebrefUrl)

    if (importGebref):
        # gemeindeschluessel_einlesen()
        gebaeudereferenzen_einlesen(checkBoxNurOberbergLaden)

    try:
        os.remove("gebref.txt")
        os.remove("gebref.zip")
    except OSError:
        print("Error while deleting file")

    # Gemeinden aus Datenbank auslesen
    SQL = "select distinct kreis, gmd from gebref order by kreis, gmd"
    curgemeinde = conn.cursor()
    curgemeinde.execute(SQL)
    # print(SQL2)
    gemeinden = curgemeinde.fetchall()
    print(gemeinden)
    for gemeinde in gemeinden:
        print(gemeinde[0], gemeinde[1])
    if (exportCebius):
        #        GemeindenamenUndKennungenAusgeben()
        for gemeinde in gemeinden:
            print("Tabellen ausgeben für: " + str(gemeinde))
            StrassentabelleAusgeben(gemeinde[0], gemeinde[1])
            HausnummerntabelleAusgeben(gemeinde[0], gemeinde[1])
    cur.close()
    conn.close()
    exit()


def GemeindenamenUndKennungenAusgeben():
    exit()


def main():
    app = QtWidgets.QApplication([])
    application = DatenDialog()
    application.show()
    app.exec()


if __name__ == "__main__":
    main()
