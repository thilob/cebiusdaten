# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatenDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_datenDialog(object):
    def setupUi(self, datenDialog):
        if not datenDialog.objectName():
            datenDialog.setObjectName(u"datenDialog")
        datenDialog.resize(640, 480)
        self.starten = QPushButton(datenDialog)
        self.starten.setObjectName(u"starten")
        self.starten.setGeometry(QRect(540, 440, 89, 28))
        self.abbrechen = QPushButton(datenDialog)
        self.abbrechen.setObjectName(u"abbrechen")
        self.abbrechen.setGeometry(QRect(440, 440, 89, 28))
        self.truncateGebref = QCheckBox(datenDialog)
        self.truncateGebref.setObjectName(u"truncateGebref")
        self.truncateGebref.setGeometry(QRect(20, 170, 371, 21))
        self.truncateGebref.setChecked(True)
        self.importGebref = QCheckBox(datenDialog)
        self.importGebref.setObjectName(u"importGebref")
        self.importGebref.setGeometry(QRect(20, 220, 581, 21))
        self.importGebref.setChecked(True)
        self.exportCebius = QCheckBox(datenDialog)
        self.exportCebius.setObjectName(u"exportCebius")
        self.exportCebius.setGeometry(QRect(20, 300, 481, 21))
        self.exportCebius.setChecked(True)
        self.CheckboxGebrefHolen = QCheckBox(datenDialog)
        self.CheckboxGebrefHolen.setObjectName(u"CheckboxGebrefHolen")
        self.CheckboxGebrefHolen.setGeometry(QRect(20, 90, 381, 23))
        self.CheckboxGebrefHolen.setChecked(True)
        self.UrlGebrefHolen = QLineEdit(datenDialog)
        self.UrlGebrefHolen.setObjectName(u"UrlGebrefHolen")
        self.UrlGebrefHolen.setGeometry(QRect(20, 110, 621, 25))
        self.label = QLabel(datenDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 20, 581, 21))
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label_2 = QLabel(datenDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 50, 151, 17))
        self.checkBoxNurOberbergLaden = QCheckBox(datenDialog)
        self.checkBoxNurOberbergLaden.setObjectName(u"checkBoxNurOberbergLaden")
        self.checkBoxNurOberbergLaden.setGeometry(QRect(80, 250, 331, 23))
        self.checkBoxNurOberbergLaden.setChecked(True)
        self.checkBoxCleanOutput = QCheckBox(datenDialog)
        self.checkBoxCleanOutput.setObjectName(u"checkBoxCleanOutput")
        self.checkBoxCleanOutput.setGeometry(QRect(80, 320, 381, 23))
        self.checkBoxCleanOutput.setChecked(True)

        self.retranslateUi(datenDialog)
        self.abbrechen.clicked.connect(datenDialog.abbrechen)
        self.starten.clicked.connect(datenDialog.weiter)

        QMetaObject.connectSlotsByName(datenDialog)
    # setupUi

    def retranslateUi(self, datenDialog):
        datenDialog.setWindowTitle(QCoreApplication.translate("datenDialog", u"Dialog", None))
        self.starten.setText(QCoreApplication.translate("datenDialog", u"starten", None))
        self.abbrechen.setText(QCoreApplication.translate("datenDialog", u"abbrechen", None))
        self.truncateGebref.setText(QCoreApplication.translate("datenDialog", u"Geb\u00e4udereferenz-Tabellen leeren", None))
        self.importGebref.setText(QCoreApplication.translate("datenDialog", u"Geb\u00e4udrefernz-Tabellen neu aus heruntergeladener Datei einlesen", None))
        self.exportCebius.setText(QCoreApplication.translate("datenDialog", u"Cebius-Stra\u00dfen- und -hausnumern-Dateien ausgeben", None))
        self.CheckboxGebrefHolen.setText(QCoreApplication.translate("datenDialog", u"Geb\u00e4udereferenzdatei neu von Opengeodata NRW laden, URL:", None))
        self.UrlGebrefHolen.setText(QCoreApplication.translate("datenDialog", u"https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/gebref_EPSG25832_ASCII.zip", None))
        self.label.setText(QCoreApplication.translate("datenDialog", u"Cebius-Hausnummernprozessor", None))
        self.label_2.setText(QCoreApplication.translate("datenDialog", u"Thilo Berger, 2025", None))
        self.checkBoxNurOberbergLaden.setText(QCoreApplication.translate("datenDialog", u"nur Dateien f\u00fcr den Oberbergischen Kreis laden", None))
        self.checkBoxCleanOutput.setText(QCoreApplication.translate("datenDialog", u"vorhandene Dateien im output-Ordner l\u00f6schen", None))
    # retranslateUi

