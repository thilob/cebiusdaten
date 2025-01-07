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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

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
        self.truncateGebref.setGeometry(QRect(100, 110, 371, 21))
        self.truncateGebref.setChecked(True)
        self.truncateKreis = QCheckBox(datenDialog)
        self.truncateKreis.setObjectName(u"truncateKreis")
        self.truncateKreis.setEnabled(False)
        self.truncateKreis.setGeometry(QRect(100, 140, 261, 21))
        self.importGebref = QCheckBox(datenDialog)
        self.importGebref.setObjectName(u"importGebref")
        self.importGebref.setGeometry(QRect(100, 190, 321, 21))
        self.importGebref.setChecked(True)
        self.importKreis = QCheckBox(datenDialog)
        self.importKreis.setObjectName(u"importKreis")
        self.importKreis.setEnabled(False)
        self.importKreis.setGeometry(QRect(100, 220, 201, 21))
        self.exportCebius = QCheckBox(datenDialog)
        self.exportCebius.setObjectName(u"exportCebius")
        self.exportCebius.setGeometry(QRect(100, 270, 281, 21))
        self.exportCebius.setChecked(True)
        self.CheckboxGebrefHolen = QCheckBox(datenDialog)
        self.CheckboxGebrefHolen.setObjectName(u"CheckboxGebrefHolen")
        self.CheckboxGebrefHolen.setGeometry(QRect(100, 20, 381, 23))
        self.CheckboxGebrefHolen.setChecked(True)
        self.UrlGebrefHolen = QLineEdit(datenDialog)
        self.UrlGebrefHolen.setObjectName(u"UrlGebrefHolen")
        self.UrlGebrefHolen.setGeometry(QRect(10, 50, 621, 25))

        self.retranslateUi(datenDialog)
        self.abbrechen.clicked.connect(datenDialog.abbrechen)
        self.starten.clicked.connect(datenDialog.weiter)

        QMetaObject.connectSlotsByName(datenDialog)
    # setupUi

    def retranslateUi(self, datenDialog):
        datenDialog.setWindowTitle(QCoreApplication.translate("datenDialog", u"Dialog", None))
        self.starten.setText(QCoreApplication.translate("datenDialog", u"starten", None))
        self.abbrechen.setText(QCoreApplication.translate("datenDialog", u"abbrechen", None))
        self.truncateGebref.setText(QCoreApplication.translate("datenDialog", u"Gebref-Tabellen leeren", None))
        self.truncateKreis.setText(QCoreApplication.translate("datenDialog", u"Kreistabelle leeren", None))
        self.importGebref.setText(QCoreApplication.translate("datenDialog", u"Gebref-Tabellen neu einlesen", None))
        self.importKreis.setText(QCoreApplication.translate("datenDialog", u"Kreistabelle neu einlesen", None))
        self.exportCebius.setText(QCoreApplication.translate("datenDialog", u"Cebiusdateien ausgeben", None))
        self.CheckboxGebrefHolen.setText(QCoreApplication.translate("datenDialog", u"Geb\u00e4udereferenzdatei neu laden", None))
        self.UrlGebrefHolen.setText(QCoreApplication.translate("datenDialog", u"https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/gebref_EPSG25832_ASCII.zip", None))
    # retranslateUi

