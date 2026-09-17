# PolSilver Bluetooth 2

Modern cross-platform **Bluetooth Low Energy diagnostics** for devices you own, administer, or have explicit permission to inspect.

PolSilver Bluetooth 2 replaces the old duplicated console/GUI scripts with one maintainable PySide6 application. It focuses on passive BLE discovery, signal quality, standard GATT metadata, battery reporting when exposed by the device, local adapter diagnostics and exportable snapshots.

## Highlights

- Windows and Linux desktop application
- Python 3.10–3.14
- PySide6 / Qt 6 dark-blue UI
- automatic Polish / English / Norwegian interface with manual switch
- bounded BLE discovery (1–20 seconds)
- RSSI quality classification
- service/manufacturer advertisement metadata
- explicit, user-confirmed connection inspection for authorized devices
- GATT service/characteristic enumeration and standard battery characteristic reading
- read-only local Bluetooth adapter diagnostics
- JSON and CSV exports
- settings stored in the user profile, not in the repository
- custom PolSilver Bluetooth icon
- automated tests, Windows EXE, portable ZIP and SHA256 checksums

## Safety model

Version 2 intentionally removes the legacy one-click MITM/Bettercap path, unauthorised-connection wording, Bluetooth reset/firmware operations and other intrusive actions. Connection inspection is presented only for a device you own, administer, or are authorized to test. Local system diagnostics are read-only.

## Install from source

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
python -m polsilver
```

Linux may require BlueZ and permission to access the Bluetooth adapter. Windows uses the WinRT Bluetooth backend provided through Bleak.

## Development

```bash
pip install -e ".[dev]"
pytest
```

The CI matrix tests Python 3.10, 3.11, 3.12, 3.13 and 3.14. A Windows job also initializes the Qt application in smoke-test mode.

## Releases

Numbered releases publish:

- `PolSilverBluetooth.exe`
- portable Windows x64 ZIP
- SHA256 for the EXE and ZIP

The release workflow runs the unit tests and a packaged EXE smoke test before publishing.

## Project layout

```text
src/polsilver/       application, BLE diagnostics, settings, exports and UI
assets/              application artwork
resources/           optional future static resources
tests/               automated tests
tools/               release/icon tooling
.github/workflows/   CI and Windows release automation
```

## Responsible use

Bluetooth identifiers and advertisements can be privacy-sensitive. Do not collect, publish or retain scans of third-party devices without a legitimate reason and appropriate permission.

---

**by Swir** — https://github.com/Swir
