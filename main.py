"""Desktop-GUI für das Cebius-Hausnummerntool."""

import argparse
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from PySide6 import QtCore, QtGui, QtWidgets
from slugify import slugify


URL = "https://www.opengeodata.nrw.de/produkte/geobasis/lk/akt/gebref_txt/gebref_EPSG25832_ASCII.zip"


def get_runtime_dir():
    """Liefert das Verzeichnis der Script- oder Bundle-Datei."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


class GeoDataProcessor:
    """Dateibasierte Verarbeitung der Gebäudereferenzdaten."""

    def __init__(self, url, log_callback=None, progress_callback=None):
        self.url = url
        self.gdf = None
        self.runtime_dir = get_runtime_dir()
        self.gebref_path = self.runtime_dir / "gebref.txt"
        self.gebref_zip_path = self.runtime_dir / "gebref.zip"
        self.output_dir = self.runtime_dir / "output"
        self.log_callback = log_callback or (lambda _message: None)
        self.progress_callback = progress_callback or (lambda _value, _text=None: None)
        self.expected_columns = [
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

    def log(self, message):
        self.log_callback(message)

    def set_progress(self, value, text=None):
        self.progress_callback(value, text)

    def ensure_output_dir(self):
        self.output_dir.mkdir(exist_ok=True)

    def download_and_extract(self):
        """Laedt die Datendatei bei Bedarf herunter."""
        download = False
        self.ensure_output_dir()
        if not self.gebref_path.exists():
            download = True
        else:
            file_mod_time = datetime.fromtimestamp(self.gebref_path.stat().st_mtime)
            if datetime.now() - file_mod_time > timedelta(hours=24):
                download = True

        if not download:
            self.log("gebref.txt ist bereits vorhanden und aktuell.")
            return True

        self.log("Gebäudereferenzen werden heruntergeladen...")
        self.set_progress(5, "Download gestartet")
        try:
            response = requests.get(self.url, allow_redirects=True, timeout=120)
            response.raise_for_status()
            with self.gebref_zip_path.open("wb") as handle:
                handle.write(response.content)
            self.log("Download abgeschlossen. Archiv wird entpackt...")
            shutil.unpack_archive(
                str(self.gebref_zip_path),
                extract_dir=str(self.runtime_dir),
            )
            self.log("Gebäudereferenzen wurden entpackt.")
            self.set_progress(15, "Download abgeschlossen")
            return True
        except requests.RequestException as exc:
            self.log(
                "Fehler beim Herunterladen. Bitte Netzwerk pruefen oder gebref.txt "
                "neben dem Programm ablegen."
            )
            self.log(f"Details: {exc}")
            return False

    def _count_total_lines(self):
        with self.gebref_path.open("r", encoding="utf-8") as handle:
            return sum(1 for _ in handle)

    def _iter_chunks(self, usecols=None):
        with self.gebref_path.open("r", encoding="utf-8") as handle:
            for chunk in pd.read_csv(
                handle,
                header=None,
                sep=";",
                chunksize=10000,
                na_filter=False,
                on_bad_lines="skip",
                encoding="utf-8",
                dtype=str,
                usecols=usecols,
            ):
                yield chunk

    def load_kreise(self):
        """Liest nur die Landkreisnamen ein und spart so viel Speicher."""
        self.log("Landkreise werden speicherschonend aus gebref.txt gelesen...")
        total_lines = self._count_total_lines()
        total_chunks = max(1, total_lines // 10000)
        kreise = set()
        for index, chunk in enumerate(self._iter_chunks(usecols=[8]), start=1):
            if len(chunk.columns) != 1:
                raise ValueError("Spaltenformat der Quelldatei ist unerwartet.")
            kreise.update(value for value in chunk.iloc[:, 0].tolist() if value)
            percent = 15 + int((index / total_chunks) * 65)
            self.set_progress(min(percent, 80), f"Landkreise lesen ({index}/{total_chunks})")
        result = sorted(kreise)
        self.log(f"{len(result)} Landkreise wurden gefunden.")
        return result

    def load_kreis_data(self, kreis_value):
        """Laedt nur die Daten eines einzelnen Landkreises."""
        self.log(f"Daten fuer {kreis_value} werden geladen...")
        total_lines = self._count_total_lines()
        total_chunks = max(1, total_lines // 10000)
        filtered_chunks = []

        for index, chunk in enumerate(self._iter_chunks(), start=1):
            if len(chunk.columns) != len(self.expected_columns):
                raise ValueError("Fehlerhafte Zeile gefunden. Bitte Quelldaten pruefen.")
            chunk.columns = self.expected_columns
            filtered = chunk[chunk["kreis"] == kreis_value]
            if not filtered.empty:
                filtered_chunks.append(filtered.copy())
            percent = 15 + int((index / total_chunks) * 45)
            self.set_progress(min(percent, 60), f"Landkreisdaten lesen ({index}/{total_chunks})")

        if not filtered_chunks:
            raise ValueError(f"Keine Daten fuer {kreis_value} gefunden.")

        df = pd.concat(filtered_chunks, ignore_index=True)
        self.log(f"{len(df):,} Zeilen fuer {kreis_value} gefunden. Geometrie wird erzeugt...")
        self.gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["ostwert"], df["nordwert"]))
        self.gdf = self.gdf.set_crs("EPSG:25832")
        self.gdf = self.gdf.to_crs("EPSG:31466")
        self.set_progress(75, "Landkreisdaten aufbereitet")
        self.log(f"{len(self.gdf):,} Datensaetze fuer {kreis_value} geladen.")

    def clean_up(self):
        if self.gebref_zip_path.exists():
            self.gebref_zip_path.unlink()

    def clear_output(self):
        self.ensure_output_dir()
        for file_path in self.output_dir.iterdir():
            if file_path.is_file():
                file_path.unlink()
        self.log("Ausgabeverzeichnis wurde geleert.")

    def export_gemeindeliste(self, gdf, landkreis):
        filename = self.output_dir / "__Gemeindeliste.txt"
        filtered_gdf = gdf[gdf["kreis"] == landkreis]
        grouped_sorted_df = (
            filtered_gdf.groupby(["landschl", "regbezschl", "kreisschl", "gmdschl", "gmd"])
            .size()
            .reset_index(name="count")
            .sort_values(by=["landschl", "regbezschl", "kreisschl", "gmdschl", "gmd"])
        )
        with filename.open("w", encoding="utf-8") as handle:
            for _, row in grouped_sorted_df.iterrows():
                handle.write(
                    f"{int(row['landschl']):02d};{row['regbezschl']};{row['kreisschl']};"
                    f"{int(row['gmdschl']):03d};-;{row['gmd']}\n"
                )
        self.log(f"Gemeindeliste gespeichert: {filename.name}")

    def export_strassen_und_hausnummern(self, kreis_value, gdf):
        filtered_gdf = gdf[gdf["kreis"] == kreis_value]
        unique_gmd_values = filtered_gdf["gmd"].unique()
        total = max(1, len(unique_gmd_values))

        for index, gmd_value in enumerate(unique_gmd_values, start=1):
            gmd_filtered_gdf = filtered_gdf[filtered_gdf["gmd"] == gmd_value]
            grouped_streets = (
                gmd_filtered_gdf.groupby(
                    ["landschl", "regbezschl", "kreisschl", "gmdschl", "gmd", "strschl", "str"]
                )
                .size()
                .reset_index(name="count")
                .sort_values(
                    by=["landschl", "regbezschl", "kreisschl", "gmdschl", "gmd", "strschl", "str"]
                )
            )

            base_filename = (
                f"{slugify(kreis_value, allow_unicode=True)}_"
                f"{slugify(gmd_value, allow_unicode=True)}"
            )

            filename = self.output_dir / f"{base_filename}_strassen.txt"
            with filename.open("w", encoding="utf-8") as handle:
                for _, row in grouped_streets.iterrows():
                    handle.write(
                        f"{int(row['landschl']):02d};{row['regbezschl']};{row['kreisschl']};"
                        f"{int(row['gmdschl']):03d};{row['strschl']};0;{row['str']}\n"
                    )

            grouped_numbers = (
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
                .sort_values(
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
            )

            filename_hnr = self.output_dir / f"{base_filename}_hausnummern.txt"
            with filename_hnr.open("w", encoding="utf-8") as handle:
                for _, row in grouped_numbers.iterrows():
                    handle.write(
                        f"{int(row['landschl']):02d};{row['regbezschl']};{row['kreisschl']};"
                        f"{int(row['gmdschl']):03d};{row['strschl']};{row['hnr']};{row['adz']};"
                        f"{row['geometry'].x};{row['geometry'].y};A;00\n"
                    )

            progress = 80 + int((index / total) * 20)
            self.set_progress(progress, f"Exportiere {gmd_value}")
            self.log(f"Dateien fuer {gmd_value} erstellt.")

    def export_kreis(self, kreis_value):
        """Fuehrt den kompletten Export fuer einen Landkreis aus."""
        self.clear_output()
        self.load_kreis_data(kreis_value)
        self.export_gemeindeliste(self.gdf, kreis_value)
        self.export_strassen_und_hausnummern(kreis_value, self.gdf)
        self.clean_up()
        self.gdf = None


class ProcessorSignals(QtCore.QObject):
    log = QtCore.Signal(str)
    progress = QtCore.Signal(int, str)
    prepared = QtCore.Signal(list, str)
    exported = QtCore.Signal(str)
    failed = QtCore.Signal(str)


class ProcessorWorker(QtCore.QRunnable):
    def __init__(self, mode, selected_kreis=None):
        super().__init__()
        self.mode = mode
        self.selected_kreis = selected_kreis
        self.signals = ProcessorSignals()

    @QtCore.Slot()
    def run(self):
        processor = GeoDataProcessor(
            URL,
            log_callback=self.signals.log.emit,
            progress_callback=self.signals.progress.emit,
        )
        try:
            if not processor.download_and_extract():
                self.signals.failed.emit(
                    "Keine Gebäudereferenzdaten verfügbar. Download oder lokale Datei fehlen."
                )
                return

            if self.mode == "prepare":
                grouped_values = processor.load_kreise()
                processor.clean_up()
                self.signals.progress.emit(100, "Bereit")
                self.signals.prepared.emit(grouped_values, str(processor.output_dir))
                return

            if not self.selected_kreis:
                raise ValueError("Es wurde kein Landkreis ausgewählt.")

            processor.export_kreis(self.selected_kreis)
            self.signals.progress.emit(100, "Export abgeschlossen")
            self.signals.exported.emit(str(processor.output_dir))
        except Exception as exc:  # pragma: no cover - GUI Fehlerpfad
            self.signals.failed.emit(str(exc))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread_pool = QtCore.QThreadPool.globalInstance()
        self.kreise = []
        self.selected_kreis = None
        self.output_dir = str(get_runtime_dir() / "output")
        self.setWindowTitle("Cebius-Hausnummerntool")
        self.resize(1180, 760)
        self._build_ui()
        self._apply_style()
        self.append_log("Bereit. Daten können geladen werden.")

    def _build_ui(self):
        central = QtWidgets.QWidget()
        root = QtWidgets.QVBoxLayout(central)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(18)

        hero = QtWidgets.QFrame()
        hero.setObjectName("hero")
        hero_layout = QtWidgets.QVBoxLayout(hero)
        hero_layout.setContentsMargins(22, 22, 22, 22)
        title = QtWidgets.QLabel("Cebius-Hausnummerntool")
        title.setObjectName("title")
        subtitle = QtWidgets.QLabel(
            "Dateibasierte Verarbeitung der NRW-Gebäudereferenzen mit scrollbarer Auswahl statt TUI-Blättern."
        )
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)
        copyright_label = QtWidgets.QLabel("Copyright 2026 by Thilo Berger · GNU GPL v3 or later")
        copyright_label.setObjectName("copyright")
        hero_layout.addWidget(copyright_label)
        root.addWidget(hero)

        content = QtWidgets.QHBoxLayout()
        content.setSpacing(18)
        root.addLayout(content, 1)

        left_panel = QtWidgets.QFrame()
        left_panel.setObjectName("panel")
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(12)

        button_row = QtWidgets.QHBoxLayout()
        self.prepare_button = QtWidgets.QPushButton("Daten laden")
        self.export_button = QtWidgets.QPushButton("Export starten")
        self.export_button.setEnabled(False)
        button_row.addWidget(self.prepare_button)
        button_row.addWidget(self.export_button)
        left_layout.addLayout(button_row)

        self.progress_label = QtWidgets.QLabel("Noch keine Daten geladen.")
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        left_layout.addWidget(self.progress_label)
        left_layout.addWidget(self.progress_bar)

        output_card = QtWidgets.QLabel(f"Ausgabeordner: {self.output_dir}")
        output_card.setObjectName("hint")
        output_card.setWordWrap(True)
        left_layout.addWidget(output_card)

        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Landkreis filtern...")
        left_layout.addWidget(self.search_edit)

        self.kreis_list = QtWidgets.QListWidget()
        self.kreis_list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.kreis_list.setAlternatingRowColors(True)
        left_layout.addWidget(self.kreis_list, 1)

        self.selection_label = QtWidgets.QLabel("Kein Landkreis ausgewählt.")
        self.selection_label.setObjectName("hint")
        self.selection_label.setWordWrap(True)
        left_layout.addWidget(self.selection_label)

        right_panel = QtWidgets.QFrame()
        right_panel.setObjectName("panel")
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(12)

        info_title = QtWidgets.QLabel("Ablauf")
        info_title.setObjectName("sectionTitle")
        right_layout.addWidget(info_title)

        steps = QtWidgets.QLabel(
            "1. Gebäudereferenzen prüfen oder herunterladen.\n"
            "2. Datei komplett einlesen und Landkreise bereitstellen.\n"
            "3. Landkreis in der scrollbaren Liste wählen.\n"
            "4. Gemeindeliste sowie Straßen- und Hausnummern-Dateien erzeugen."
        )
        steps.setWordWrap(True)
        steps.setObjectName("hint")
        right_layout.addWidget(steps)

        log_title = QtWidgets.QLabel("Statusprotokoll")
        log_title.setObjectName("sectionTitle")
        right_layout.addWidget(log_title)

        self.log_view = QtWidgets.QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumBlockCount(1000)
        right_layout.addWidget(self.log_view, 1)

        content.addWidget(left_panel, 3)
        content.addWidget(right_panel, 2)

        self.setCentralWidget(central)

        self.prepare_button.clicked.connect(self.prepare_data)
        self.export_button.clicked.connect(self.export_selected)
        self.search_edit.textChanged.connect(self.filter_kreise)
        self.kreis_list.currentTextChanged.connect(self.update_selection)

    def _apply_style(self):
        self.setStyleSheet(
            """
            QWidget {
                background: #eef2f5;
                color: #162330;
                font-family: "Noto Sans", "DejaVu Sans", sans-serif;
                font-size: 14px;
            }
            QFrame#hero {
                background: #0d3b66;
                border-radius: 22px;
            }
            QLabel#title {
                color: #ebff00;
                background-color: #0d3b66;
                font-size: 30px;
                font-weight: 700;
            }
            QLabel#subtitle {
                color: #ebff00;
                background-color: #0d3b66;
                font-size: 15px;
            }
            QLabel#copyright {
                color: #d8e3ee;
                background-color: #0d3b66;
                font-size: 12px;
                letter-spacing: 0.03em;
            }
            QFrame#panel {
                background: #fbfcfd;
                border: 1px solid #c8d4df;
                border-radius: 18px;
            }
            QLabel#sectionTitle {
                font-size: 18px;
                font-weight: 700;
                color: #12385d;
            }
            QLabel#hint {
                color: #556879;
                line-height: 1.4em;
            }
            QPushButton {
                background: #0d3b66;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 16px;
                font-weight: 700;
            }
            QPushButton:disabled {
                background: #9aabba;
                color: #edf2f6;
            }
            QPushButton:hover:!disabled {
                background: #135287;
            }
            QLineEdit, QListWidget, QPlainTextEdit {
                background: #ffffff;
                border: 1px solid #cdd9e3;
                border-radius: 12px;
                padding: 8px;
            }
            QLineEdit:focus, QListWidget:focus, QPlainTextEdit:focus {
                border: 1px solid #b8922f;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 8px;
            }
            QListWidget::item:hover {
                background: #e7eef5;
            }
            QListWidget::item:selected {
                background: #e0b454;
                color: #142231;
            }
            QProgressBar {
                background: #dde5ec;
                border: none;
                border-radius: 8px;
                text-align: center;
                min-height: 16px;
                color: #18324f;
            }
            QProgressBar::chunk {
                background: #d8a53b;
                border-radius: 8px;
            }
            """
        )

    def append_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_view.appendPlainText(f"[{timestamp}] {message}")
        scrollbar = self.log_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def set_busy(self, busy, label):
        self.prepare_button.setEnabled(not busy)
        self.export_button.setEnabled(not busy and bool(self.selected_kreis))
        self.kreis_list.setEnabled(not busy)
        self.search_edit.setEnabled(not busy)
        self.progress_label.setText(label)

    def prepare_data(self):
        self.progress_bar.setValue(0)
        self.kreis_list.clear()
        self.kreise = []
        self.selected_kreis = None
        self.selection_label.setText("Kein Landkreis ausgewählt.")
        self.set_busy(True, "Daten werden vorbereitet...")
        self.append_log("Datenvorbereitung gestartet.")
        self.run_worker("prepare")

    def export_selected(self):
        if not self.selected_kreis:
            QtWidgets.QMessageBox.information(self, "Landkreis wählen", "Bitte zuerst einen Landkreis auswählen.")
            return
        self.progress_bar.setValue(0)
        self.set_busy(True, f"Export für {self.selected_kreis} gestartet...")
        self.append_log(f"Export für {self.selected_kreis} gestartet.")
        self.run_worker("export", self.selected_kreis)

    def run_worker(self, mode, selected_kreis=None):
        worker = ProcessorWorker(mode, selected_kreis)
        worker.signals.log.connect(self.append_log)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.prepared.connect(self.on_prepared)
        worker.signals.exported.connect(self.on_exported)
        worker.signals.failed.connect(self.on_failed)
        self.thread_pool.start(worker)

    @QtCore.Slot(int, str)
    def update_progress(self, value, text):
        self.progress_bar.setValue(value)
        self.progress_label.setText(text)

    @QtCore.Slot(list, str)
    def on_prepared(self, kreise, output_dir):
        self.kreise = kreise
        self.output_dir = output_dir
        self.filter_kreise(self.search_edit.text())
        self.set_busy(False, "Landkreise geladen.")
        self.append_log(f"{len(kreise)} Landkreise stehen zur Auswahl.")

    @QtCore.Slot(str)
    def on_exported(self, output_dir):
        self.output_dir = output_dir
        self.set_busy(False, "Export abgeschlossen.")
        self.append_log(f"Export abgeschlossen. Dateien liegen in {output_dir}.")
        if not self.open_output_dir(output_dir):
            self.append_log("Hinweis: Der Ausgabeordner konnte nicht automatisch geöffnet werden.")
        QtWidgets.QMessageBox.information(
            self,
            "Export abgeschlossen",
            f"Die Ausgabedateien wurden in\n{output_dir}\nerstellt.",
        )

    @QtCore.Slot(str)
    def on_failed(self, message):
        self.set_busy(False, "Fehler aufgetreten.")
        self.append_log(f"Fehler: {message}")
        QtWidgets.QMessageBox.critical(self, "Fehler", message)

    def open_output_dir(self, output_dir):
        url = QtCore.QUrl.fromLocalFile(output_dir)
        if QtGui.QDesktopServices.openUrl(url):
            return True
        if sys.platform.startswith("win") and hasattr(os, "startfile"):
            os.startfile(output_dir)
            return True
        return False

    def filter_kreise(self, text):
        current = self.selected_kreis
        self.kreis_list.clear()
        needle = text.casefold().strip()
        for kreis in self.kreise:
            if not needle or needle in kreis.casefold():
                self.kreis_list.addItem(kreis)
        if current:
            matches = self.kreis_list.findItems(current, QtCore.Qt.MatchExactly)
            if matches:
                self.kreis_list.setCurrentItem(matches[0])

    def update_selection(self, text):
        self.selected_kreis = text or None
        if self.selected_kreis:
            self.selection_label.setText(f"Ausgewählter Landkreis: {self.selected_kreis}")
        else:
            self.selection_label.setText("Kein Landkreis ausgewählt.")
        self.export_button.setEnabled(bool(self.selected_kreis))


def main():
    parser = argparse.ArgumentParser(description="Cebius-Hausnummerntool")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Startet die GUI kurz im Testmodus und beendet sie automatisch.",
    )
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Cebius-Hausnummerntool")
    window = MainWindow()
    window.show()
    if args.smoke_test:
        QtCore.QTimer.singleShot(1200, app.quit)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
