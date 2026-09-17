from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .ble import discover_devices, inspect_device, pair_device
from .config import Settings
from .export import export_csv, export_json
from .i18n import tr
from .models import DeviceInspection, DeviceSnapshot
from .system import launch_wireshark, run_local_diagnostics


def resource_path(*parts: str) -> Path:
    """Resolve resources in source checkouts and PyInstaller one-file builds."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    root = Path(bundle_root) if bundle_root else Path(__file__).resolve().parents[2]
    return root.joinpath(*parts)


def application_icon() -> QIcon:
    for name in ("polsilver.png", "polsilver.ico", "polsilver.svg"):
        candidate = resource_path("assets", name)
        if candidate.exists():
            return QIcon(str(candidate))
    return QIcon()


class AsyncWorker(QThread):
    result = Signal(object)
    error = Signal(str)

    def __init__(self, factory: Callable[[], object], parent=None):
        super().__init__(parent)
        self._factory = factory

    def run(self) -> None:
        try:
            value = self._factory()
            if hasattr(value, "__await__"):
                value = asyncio.run(value)
            self.result.emit(value)
        except Exception as exc:  # GUI boundary
            self.error.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings.load()
        self.language = self.settings.resolved_language
        self.devices: list[DeviceSnapshot] = []
        self.inspections: dict[str, DeviceInspection] = {}
        self._workers: set[QThread] = set()
        self._build_ui()
        self._apply_language()

    def _build_ui(self) -> None:
        self.setMinimumSize(980, 640)
        self.resize(1180, 760)
        self.setWindowIcon(application_icon())

        root = QWidget(self)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(18, 18, 18, 12)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        self.title = QLabel()
        self.title.setObjectName("Title")
        self.subtitle = QLabel()
        self.subtitle.setObjectName("Subtitle")
        title_box.addWidget(self.title)
        title_box.addWidget(self.subtitle)
        header.addLayout(title_box, 1)
        self.language_combo = QComboBox()
        self.language_combo.addItem("Auto", "auto")
        self.language_combo.addItem("Polski", "pl")
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Norsk", "no")
        index = self.language_combo.findData(self.settings.language)
        self.language_combo.setCurrentIndex(max(index, 0))
        self.language_combo.currentIndexChanged.connect(self._language_changed)
        header.addWidget(self.language_combo)
        layout.addLayout(header)

        primary_controls = QHBoxLayout()
        self.scan_button = QPushButton()
        self.inspect_button = QPushButton()
        self.pair_button = QPushButton()
        self.adapter_button = QPushButton()
        self.export_button = QPushButton()
        for button in (
            self.scan_button,
            self.inspect_button,
            self.pair_button,
            self.adapter_button,
            self.export_button,
        ):
            primary_controls.addWidget(button)
        primary_controls.addStretch(1)
        layout.addLayout(primary_controls)

        secondary_controls = QHBoxLayout()
        self.wireshark_button = QPushButton()
        self.save_log_button = QPushButton()
        self.clear_button = QPushButton()
        for button in (self.wireshark_button, self.save_log_button, self.clear_button):
            secondary_controls.addWidget(button)
        secondary_controls.addStretch(1)
        layout.addLayout(secondary_controls)

        splitter = QSplitter(Qt.Horizontal)
        self.table = QTableWidget(0, 5)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemSelectionChanged.connect(self._render_selected)
        self.table.doubleClicked.connect(lambda _index: self.inspect_selected())
        splitter.addWidget(self.table)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        self.details_label = QLabel()
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        self.log_label = QLabel()
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        right_layout.addWidget(self.details_label)
        right_layout.addWidget(self.details, 1)
        right_layout.addWidget(self.log_label)
        right_layout.addWidget(self.log, 1)
        splitter.addWidget(right)
        splitter.setSizes([620, 520])
        layout.addWidget(splitter, 1)

        self.notice = QLabel()
        self.notice.setWordWrap(True)
        self.notice.setObjectName("Notice")
        layout.addWidget(self.notice)

        self.footer = QLabel('<a href="https://github.com/Swir">by Swir • github.com/Swir</a>')
        self.footer.setOpenExternalLinks(True)
        self.footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.footer)

        self.setCentralWidget(root)
        self.setStyleSheet(
            "QMainWindow,QWidget{background:#07111f;color:#dbeafe;}"
            "#Title{font-size:26px;font-weight:700;color:#60a5fa;}"
            "#Subtitle{color:#93c5fd;font-size:13px;}"
            "#Notice{background:#0b1e35;border:1px solid #1d4ed8;border-radius:8px;padding:8px;color:#bfdbfe;}"
            "QPushButton{background:#0d2b4d;border:1px solid #2563eb;border-radius:7px;padding:9px 13px;font-weight:600;}"
            "QPushButton:hover{background:#123b68;} QPushButton:disabled{color:#64748b;border-color:#334155;}"
            "QTableWidget,QTextEdit,QComboBox{background:#081827;border:1px solid #1e3a5f;border-radius:7px;}"
            "QHeaderView::section{background:#0d2b4d;color:#dbeafe;padding:6px;border:0;}"
        )

        self.scan_button.clicked.connect(self.scan)
        self.inspect_button.clicked.connect(self.inspect_selected)
        self.pair_button.clicked.connect(self.pair_selected)
        self.adapter_button.clicked.connect(self.adapter_report)
        self.export_button.clicked.connect(self.export_snapshot)
        self.wireshark_button.clicked.connect(self.open_wireshark)
        self.save_log_button.clicked.connect(self.save_log)
        self.clear_button.clicked.connect(self.log.clear)

    def _apply_language(self) -> None:
        lang = self.language
        self.setWindowTitle(tr(lang, "app"))
        self.title.setText(tr(lang, "app"))
        self.subtitle.setText(tr(lang, "subtitle"))
        self.scan_button.setText(tr(lang, "scan"))
        self.inspect_button.setText(tr(lang, "inspect"))
        self.pair_button.setText(tr(lang, "pair"))
        self.adapter_button.setText(tr(lang, "adapter"))
        self.export_button.setText(tr(lang, "export"))
        self.wireshark_button.setText(tr(lang, "wireshark"))
        self.save_log_button.setText(tr(lang, "save_log"))
        self.clear_button.setText(tr(lang, "clear"))
        self.details_label.setText(tr(lang, "details"))
        self.log_label.setText(tr(lang, "log"))
        self.notice.setText(tr(lang, "authorized"))
        self.table.setHorizontalHeaderLabels([
            tr(lang, "name"), tr(lang, "address"), tr(lang, "rssi"), tr(lang, "quality"), tr(lang, "services")
        ])
        self._render_selected()

    def _language_changed(self) -> None:
        self.settings.language = str(self.language_combo.currentData())
        self.settings.save()
        self.language = self.settings.resolved_language
        self._apply_language()

    def _append_log(self, message: str) -> None:
        self.log.append(message)

    def _track(self, worker: QThread) -> None:
        self._workers.add(worker)
        worker.finished.connect(lambda: self._workers.discard(worker))
        worker.start()

    def _busy(self, busy: bool) -> None:
        self.scan_button.setDisabled(busy)
        self.inspect_button.setDisabled(busy)
        self.pair_button.setDisabled(busy)
        self.adapter_button.setDisabled(busy)

    def scan(self) -> None:
        self._busy(True)
        self._append_log(tr(self.language, "scan_started"))
        worker = AsyncWorker(lambda: discover_devices(self.settings.scan_seconds), self)
        worker.result.connect(self._scan_done)
        worker.error.connect(lambda error: self._append_log(tr(self.language, "scan_error", error=error)))
        worker.finished.connect(lambda: self._busy(False))
        self._track(worker)

    def _scan_done(self, result: object) -> None:
        self.devices = list(result or [])
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.devices))
        for row, device in enumerate(self.devices):
            values = [
                device.name,
                device.address,
                "" if device.rssi is None else str(device.rssi),
                device.signal_quality,
                str(len(device.service_uuids)),
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, device.address)
                self.table.setItem(row, column, item)
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self._append_log(tr(self.language, "scan_done", count=len(self.devices)))
        if self.devices:
            self.table.selectRow(0)

    def _selected_device(self) -> DeviceSnapshot | None:
        row = self.table.currentRow()
        if row < 0 or not self.table.item(row, 0):
            return None
        address = self.table.item(row, 0).data(Qt.UserRole)
        return next((device for device in self.devices if device.address == address), None)

    def inspect_selected(self) -> None:
        device = self._selected_device()
        if not device:
            self._append_log(tr(self.language, "select"))
            return
        answer = QMessageBox.question(
            self,
            tr(self.language, "app"),
            tr(self.language, "authorized"),
            QMessageBox.Yes | QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        self._busy(True)
        self._append_log(tr(self.language, "inspect_started", address=device.address))
        worker = AsyncWorker(lambda: inspect_device(device.address, self.settings.connect_timeout), self)
        worker.result.connect(self._inspection_done)
        worker.error.connect(lambda error: self._append_log(tr(self.language, "inspect_error", error=error)))
        worker.finished.connect(lambda: self._busy(False))
        self._track(worker)

    def _inspection_done(self, result: object) -> None:
        if isinstance(result, DeviceInspection):
            self.inspections[result.address] = result
        self._append_log(tr(self.language, "inspect_done"))
        self._render_selected()

    def pair_selected(self) -> None:
        device = self._selected_device()
        if not device:
            self._append_log(tr(self.language, "select"))
            return
        answer = QMessageBox.question(
            self,
            tr(self.language, "pair"),
            tr(self.language, "pair_confirm", name=device.name, address=device.address),
            QMessageBox.Yes | QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        self._busy(True)
        self._append_log(tr(self.language, "pair_started", address=device.address))
        worker = AsyncWorker(lambda: pair_device(device.address, max(self.settings.connect_timeout, 20.0)), self)
        worker.result.connect(lambda value: self._append_log(tr(self.language, "pair_done" if value else "pair_not_confirmed")))
        worker.error.connect(lambda error: self._append_log(tr(self.language, "pair_error", error=error)))
        worker.finished.connect(lambda: self._busy(False))
        self._track(worker)

    def adapter_report(self) -> None:
        self._busy(True)
        worker = AsyncWorker(run_local_diagnostics, self)
        worker.result.connect(lambda value: self._append_log(str(value)))
        worker.error.connect(lambda error: self._append_log(error))
        worker.finished.connect(lambda: self._busy(False))
        self._track(worker)

    def open_wireshark(self) -> None:
        self._append_log(launch_wireshark())

    def save_log(self) -> None:
        path, _selected = QFileDialog.getSaveFileName(
            self,
            tr(self.language, "save_log"),
            "polsilver-log.txt",
            "Text (*.txt);;All files (*)",
        )
        if not path:
            return
        target = Path(path)
        try:
            target.write_text(self.log.toPlainText(), encoding="utf-8")
        except OSError as exc:
            self._append_log(tr(self.language, "save_log_error", error=exc))
            return
        self._append_log(tr(self.language, "saved", path=target))

    def export_snapshot(self) -> None:
        if not self.devices:
            self._append_log(tr(self.language, "select"))
            return
        path, selected = QFileDialog.getSaveFileName(
            self,
            tr(self.language, "save"),
            "polsilver-scan.json",
            "JSON (*.json);;CSV (*.csv)",
        )
        if not path:
            return
        target = Path(path)
        if selected.startswith("CSV") or target.suffix.lower() == ".csv":
            export_csv(target.with_suffix(".csv"), self.devices)
            target = target.with_suffix(".csv")
        else:
            export_json(target.with_suffix(".json"), self.devices)
            target = target.with_suffix(".json")
        self._append_log(tr(self.language, "saved", path=target))

    def _render_selected(self) -> None:
        device = self._selected_device()
        if not device:
            self.details.clear()
            return
        payload = device.to_dict()
        inspection = self.inspections.get(device.address)
        if inspection:
            payload["inspection"] = inspection.to_dict()
        self.details.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PolSilver Bluetooth LE diagnostics")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Initialize the real Qt window and exit for packaged-build verification",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    app = QApplication(sys.argv[:1])
    app.setApplicationName("PolSilver Bluetooth")
    app.setOrganizationName("Swir")
    app.setWindowIcon(application_icon())
    window = MainWindow()
    if args.smoke_test:
        window.show()
        app.processEvents()
        window.close()
        return 0
    window.show()
    return app.exec()
