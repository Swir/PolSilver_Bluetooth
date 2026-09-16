from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def rssi_quality(rssi: int | None) -> str:
    if rssi is None:
        return "unknown"
    if rssi >= -55:
        return "excellent"
    if rssi >= -67:
        return "good"
    if rssi >= -75:
        return "fair"
    return "weak"


def normalize_uuid(value: str) -> str:
    return value.strip().lower()


@dataclass(slots=True)
class DeviceSnapshot:
    address: str
    name: str = "Unknown"
    rssi: int | None = None
    service_uuids: list[str] = field(default_factory=list)
    manufacturer_ids: list[int] = field(default_factory=list)
    connectable: bool | None = None
    seen_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def signal_quality(self) -> str:
        return rssi_quality(self.rssi)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["signal_quality"] = self.signal_quality
        return data


@dataclass(slots=True)
class DeviceInspection:
    address: str
    connected: bool
    service_uuids: list[str] = field(default_factory=list)
    characteristic_uuids: list[str] = field(default_factory=list)
    battery_percent: int | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
