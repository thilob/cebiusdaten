import re
import sys

import psycopg2 as psycopg2
import psycopg2.extras
from PyQt5 import QtWidgets

from DatenDialog import Ui_datenDialog

# Datenbankverbindung herstellen und Bewegungsdatentabellen leeren
print("Programm gestartet")
conn = psycopg2.connect("dbname=cebiusdaten user=cebiusdaten password=cebiusdaten")
cur = conn.cursor()
#cur.execute("truncate gmadressen")
#cur.commit()
print("Verbindung hergestellt")


# Funktionen definieren

def truncateGebref():
    cur.execute("truncate gebref_schluessel")
    cur.execute("truncate gebref")


def truncateKreis():
    cur.execute("truncate gmadressen")


def StrassentabelleAusgeben(Gemeindename):
    curgem = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    SQL = "select * from gebref_schluessel where field_6='{}'".format(Gemeindename)
    print(SQL)
    curgem.execute(SQL)
    print("Nach Execute")
    row_count = 0
    zeile1 = ""
    for row in curgem:
        row_count += 1
        #   print(row_count)
        zeile1 = row['field_2'] + ";" + row['field_3'] + ";" + row['field_4'] + ";" + row['field_5'] + ";"

    F2 = open(Gemeindename + "_Strassen.txt", "w", encoding="windows-1252", newline='\r\n')
    curstrasse = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    SQL2 = "select distinct strassenschluessel, strassenname from gmadressen where gemeinde_stadt='" + Gemeindename + "' order by strassenname"
    curstrasse.execute(SQL2)
    # print(SQL2)
    records = curstrasse.fetchall()
    for strasse in records:
        zeile = strasse["strassenschluessel"] + ";0;" + strasse["strassenname"] + "\n"
        zeile2 = str(zeile1) + str(zeile)
        F2.write(zeile2)
    F2.close()


def Hausnummerntabelle(Gemeindename):
    curgem = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    SQL = "select * from gebref_schluessel where field_6='{}'".format(Gemeindename)
    print(SQL)
    curgem.execute(SQL)
    print("Nach Execute")
    row_count = 0
    zeile1 = ""
    for row in curgem:
        row_count += 1
        print(row_count)
        zeile1 = row['field_2'] + ";" + row['field_3'] + ";" + row['field_4'] + ";" + row['field_5'] + ";"

    F2 = open(Gemeindename + "_Hausnummern.txt", "w", encoding="windows-1252")
    curstrasse = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    SQL2 = "select strassenschluessel, nummernteil, buchstaben, st_x(geom31466)::text as x, st_y(geom31466)::text as y  from " \
           "gmadressen where gemeinde_stadt='" + Gemeindename + "' order by strassenname, hsnr"
    curstrasse.execute(SQL2)
    print(SQL2)
    records = curstrasse.fetchall()
    for strasse in records:
        zeile = strasse["strassenschluessel"] + ";" + strasse["nummernteil"] + ";" + strasse["buchstaben"] \
                + ";001;" + strasse["x"] + ";" + strasse["y"] + ";A;00\n"
        zeile2 = str(zeile1) + str(zeile)
        print(zeile2)
        F2.write(zeile2)
    F2.close()


def kreisdaten_einlesen():
    print ("Kreidaten einlesen aufgerufen")
    # Aktuelle Daten der Kreisverwaltung einlesen
    cur.execute("truncate gmadressen")
    print ("Truncate durchgeführt")
    F = open("hausnummern_polizei_.csv", "r", encoding="windows-1252")
    print ("Datei geöffnet")
    i = -1;

    for line in F:
        print("Zeile gelesen")
        line = line.strip()
        print(line + "     " + str(line.count(";")))
        m = re.split(';', line)
        print(m[0] + "  " + str(m[5]))
        SQL = "insert into gmadressen (gemeinde_stadt, ortsteil, strassenschluessel, strassenname, hsnr, ostwert, nordwert) " \
              "values (%s, %s, %s, %s, %s, %s, %s);"
        data = (m[0], m[1], m[2], m[3], m[4], m[5], m[6])
        if i >= 0:
            cur.execute(SQL, data)
        i += 1
    conn.commit()
    SQL = """update gmadressen set 
    geom25832=st_setsrid(st_point(cast(replace(ostwert,',','.') as float), cast(replace(nordwert,',','.') as float)),25832)"""
    cur.execute(SQL)
    conn.commit()
    SQL = "update gmadressen set geom31466=st_transform(geom25832,31466)"
    cur.execute(SQL)
    SQL = "update gmadressen set nummernteil=substring(hsnr,'^[\d]*'), buchstaben=substring(hsnr,'[a-z]*$')"
    cur.execute(SQL)
    conn.commit()


def gemeindeschluessel_einlesen():
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
    conn.commit()


def gebaeudereferenzen_einlesen():
    # Aktuelle Gebäudereferenzen des Landes einlesen
    F = open("gebref.txt", "r", encoding="utf-8")
    i = -1
    cur.execute("truncate gebref")
    for line in F:
        line = line.strip()
        m = re.split(';', line)
        #print ('Spalten:' + str(len(m)))
        punkt = "POINT(" + m[18].replace(",", ".") + " " + m[19].replace(",", ".") + ")"
        SQL = """INSERT INTO public.gebref(nba, oid, qua, landschl, land, regbezschl, regbez, kreisschl, kreis, gmdschl, gmd, ottschl, ott, strschl, str, hnr, adz, zone, ostwert, nordwert, datum, geom25832)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14],m[15],m[16],m[17],m[18],m[19],m[20],punkt) 
        if i >= 0:
             cur.execute(SQL, data)
        if i == 1000:
             conn.commit()
             i = 0
             print("\r" + m[1])
        i += 1
    # print("\rBaue Straßennamen zusammen")
    # SQL = """update gebref set adresse = strassenname || ' ' || hnr || coalesce(zusatz,'')"""
    # cur.execute(SQL)
    # conn.commit()
    # print("\rFülle Geospalten")
    # SQL = """update gebref set geom4647=st_setsrid(st_point(cast(replace(rechts,',','.') as float), cast(replace(hoch,',','.') as float)),4647),
    # geom25832=st_setsrid(st_point(cast(replace(rechts,',','.') as float), cast(replace(hoch,',','.') as float)),25832),
    # geom31466=st_setsrid(st_point(cast(replace(rechts,',','.') as float), cast(replace(hoch,',','.') as float)),31466)"""
    # cur.execute(SQL)
    # conn.commit()
    # print("\rsetze Gemeindenamen")
    # SQL = """update gebref set gemeindename=(select field_6 from gebref_schluessel a where a.field_3=regbez and a.field_4=kreis and a.field_5=gemeinde) where gemeinde<>'000';"""
    # cur.execute(SQL)
    # conn.commit()
    # SQL = """update gebref set gemeindename=(select field_5 from gebref_schluessel a where a.field_3=regbez and a.field_4=kreis and a.field_1='K') where gemeinde='000';"""
    # cur.execute(SQL)
    # conn.commit()
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
        sys.exit(app.exec_())

    def weiter(self):
        ausfuehren(self.ui.truncateGebref.isChecked(),self.ui.truncateKreis.isChecked(),self.ui.importGebref.isChecked(),self.ui.importKreis.isChecked(),self.ui.exportCebius.isChecked())
        sys.exit(app.exec_())


def ausfuehren(truncGebref,truncKreis,importGebref,importKreis,exportCebius):
    print ("ausführen wurde aufgerufen!")
    if (importGebref):
        #gemeindeschluessel_einlesen()
        gebaeudereferenzen_einlesen()


    if (importKreis):
        kreisdaten_einlesen()

    gemeinden = (
    "Radevormwald", "Hückeswagen", "Wipperfürth", "Lindlar", "Gummersbach", "Bergneustadt", "Wiehl", "Reichshof",
    "Nümbrecht", "Engelskirchen", "Waldbröl", "Morsbach", "Marienheide")



    if (exportCebius):
        for gemeinde in gemeinden:
            StrassentabelleAusgeben(gemeinde)
            Hausnummerntabelle(gemeinde)
    cur.close()
    conn.close()


def main():
    app = QtWidgets.QApplication([])
    application = DatenDialog()
    application.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
