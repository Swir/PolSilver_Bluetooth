from __future__ import annotations

from collections.abc import Callable
from typing import Any

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

from .models import DeviceInspection, DeviceSnapshot, normalize_uuid

BATTERY_LEVEL_UUID = "00002a19-0000-1000-8000-00805f9b34fb"


async def discover_devices(timeout: float = 5.0) -> list[DeviceSnapshot]:
    """Discover nearby BLE advertisements without connecting to devices."""
    timeout = min(max(float(timeout), 1.0), 20.0)
    discovered = await BleakScanner.discover(timeout=timeout, return_adv=True)
    snapshots: list[DeviceSnapshot] = []

    if isinstance(discovered, dict):
        items = discovered.values()
        for device, advertisement in items:
            snapshots.append(_snapshot_from_advertisement(device, advertisement))
    else:  # compatibility with older/custom Bleak backends
        for device in discovered:
            snapshots.append(
                DeviceSnapshot(
                    address=str(getattr(device, "address", "")),
                    name=str(getattr(device, "name", None) or "Unknown"),
                    rssi=getattr(device, "rssi", None),
                )
            )

    snapshots.sort(key=lambda item: (item.rssi is None, -(item.rssi or -999), item.name.lower()))
    return snapshots


def _snapshot_from_advertisement(device: Any, advertisement: Any) -> DeviceSnapshot:
    name = getattr(advertisement, "local_name", None) or getattr(device, "name", None) or "Unknown"
    uuids = [normalize_uuid(value) for value in (getattr(advertisement, "service_uuids", None) or [])]
    manufacturer = getattr(advertisement, "manufacturer_data", None) or {}
    return DeviceSnapshot(
        address=str(getattr(device, "address", "")),
        name=str(name),
        rssi=getattr(advertisement, "rssi", None),
        service_uuids=sorted(set(uuids)),
        manufacturer_ids=sorted(int(key) for key in manufacturer.keys()),
    )


async def inspect_device(address: str, timeout: float = 12.0) -> DeviceInspection:
    """Connect to a selected, authorized device and enumerate standard GATT metadata."""
    address = address.strip()
    if not address:
        raise ValueError("device address is required")
    timeout = min(max(float(timeout), 3.0), 30.0)
    notes: list[str] = []
    service_uuids: list[str] = []
    characteristic_uuids: list[str] = []
    battery: int | None = None

    try:
        async with BleakClient(address, timeout=timeout) as client:
            services = client.services
            for service in services:
                service_uuids.append(normalize_uuid(service.uuid))
                for characteristic in service.characteristics:
                    characteristic_uuids.append(normalize_uuid(characteristic.uuid))

            if BATTERY_LEVEL_UUID in characteristic_uuids:
                try:
                    raw = await client.read_gatt_char(BATTERY_LEVEL_UUID)
                    if raw:
                        battery = max(0, min(100, int(raw[0])))
                except (BleakError, OSError, PermissionError) as exc:
                    notes.append(f"Battery characteristic present but not readable: {exc}")

            return DeviceInspection(
                address=address,
                connected=bool(client.is_connected),
                service_uuids=sorted(set(service_uuids)),
                characteristic_uuids=sorted(set(characteristic_uuids)),
                battery_percent=battery,
                notes=notes,
            )
    except BleakError as exc:
        raise RuntimeError(f"BLE connection failed: {exc}") from exc
