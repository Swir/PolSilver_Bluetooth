from __future__ import annotations

import csv
import json
from pathlib import Path
from collections.abc import Iterable

from .models import DeviceSnapshot


def export_json(path: Path, devices: Iterable[DeviceSnapshot]) -> Path:
    rows = [device.to_dict() for device in devices]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def export_csv(path: Path, devices: Iterable[DeviceSnapshot]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["name", "address", "rssi", "signal_quality", "service_uuids", "manufacturer_ids", "seen_at"])
        for device in devices:
            writer.writerow([
                device.name,
                device.address,
                "" if device.rssi is None else device.rssi,
                device.signal_quality,
                ";".join(device.service_uuids),
                ";".join(str(value) for value in device.manufacturer_ids),
                device.seen_at,
            ])
    return path
