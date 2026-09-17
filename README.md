<div align="center">

<img src="assets/polsilver.svg" alt="PolSilver Bluetooth icon" width="128" height="128">

# PolSilver Bluetooth 2.1

### Cross-platform Bluetooth Low Energy diagnostics for devices you own, administer, or have explicit permission to inspect

**Python 3.10–3.14 • PySide6 / Qt 6 • Bleak • Windows / Linux**

</div>

---

## Regression audit result

PolSilver Bluetooth 2.1 was compared against both legacy implementations (`run.py` and `GUI Ver,py`). The modern modular application is retained, while useful non-destructive features that disappeared during modernization have been restored or replaced with safer equivalents.

### Restored / improved

- bounded nearby BLE discovery
- RSSI signal quality and advertisement metadata
- authorized GATT inspection and standard battery reading
- **OS-backed pairing** for one explicitly selected device, with confirmation before the action
- **paired-device and connected-device inventory** on Linux via read-only `bluetoothctl` commands
- **recent Bluetooth connection/history diagnostics** on Linux and Windows where the OS exposes them
- **Wireshark launcher** when Wireshark is already installed; PolSilver does not automatically choose a capture interface or start an interception workflow
- **Save diagnostics log** to a text file
- JSON and CSV scan export
- double-click a discovered device to open the authorized GATT inspection flow
- custom PolSilver icon shown in this README, in the source GUI and in the packaged Windows EXE
- PL / EN / NO interface with automatic system-language selection and manual switch

### Intentionally not restored

The old versions also exposed actions that are inappropriate for a safe diagnostics application. Version 2.1 therefore does **not** restore automated MITM/Bettercap attacks, "unauthorized connection" testing, forced sniffing, destructive Bluetooth reset, firmware/package modification, forced visibility changes, or other intrusive operations. These omissions are deliberate rather than regressions.

---

## Main features

- Windows and Linux desktop application
- Python 3.10–3.14
- responsive PySide6 / Qt 6 dark-blue UI
- bounded BLE discovery (1–20 seconds)
- RSSI quality classification
- service UUID and manufacturer advertisement metadata
- explicit user-confirmed GATT inspection for authorized devices
- standard battery characteristic reading when exposed by the device
- explicit user-confirmed OS pairing request
- read-only local Bluetooth adapter diagnostics
- Linux paired / connected device inventory and recent BlueZ service history
- Windows Bluetooth PnP, service and recent BTHUSB event diagnostics
- optional local Wireshark launcher
- JSON / CSV exports and text diagnostic-log export
- settings stored in the user profile, not in the repository
- own application icon and `by Swir` footer
- automated tests, packaged-GUI smoke test, Windows EXE, portable ZIP and SHA256 checksums

---

## Install from source

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
python -m polsilver
```

Linux normally requires BlueZ and permission to access the local Bluetooth adapter. Windows uses Bleak's WinRT backend.

---

## Typical workflow

1. Start **Scan nearby BLE**.
2. Select a device from the result table.
3. Use **Inspect selected device** only if you own/administer it or have permission to test it.
4. Use **Pair selected device** only when you intend to pair that authorized device; PolSilver asks for confirmation first and the operating system still controls the pairing procedure.
5. Use **Local adapter report** for read-only operating-system diagnostics.
6. Export a scan to JSON/CSV or save the diagnostics log as text when needed.
7. **Open Wireshark** only launches an already installed Wireshark application. Capture only traffic/interfaces you are authorized to inspect.

---

## Development and tests

```bash
pip install -e ".[dev]"
pytest
python -m polsilver --smoke-test
```

The CI matrix tests Python **3.10, 3.11, 3.12, 3.13 and 3.14**. Windows CI initializes the real Qt main window. Release CI additionally builds the one-file EXE and runs that packaged GUI in smoke-test mode before publishing anything.

---

## Windows releases

A numbered release publishes:

- `PolSilverBluetooth.exe`
- `PolSilverBluetooth.exe.sha256`
- `PolSilver-Bluetooth-vX.Y.Z-Windows-x64.zip`
- `PolSilver-Bluetooth-vX.Y.Z-Windows-x64.zip.sha256`

The portable package also contains README, CHANGELOG, SECURITY documentation and the project icon. The generated PNG icon is bundled inside the one-file EXE so the running packaged window uses the same PolSilver branding as the repository.

---

## Project layout

```text
src/polsilver/
  app.py          # Qt GUI, pairing confirmation, export/log actions
  ble.py          # BLE discovery, authorized GATT inspection and pairing
  system.py       # read-only local adapter/history diagnostics + Wireshark launcher
  models.py       # diagnostic models
  config.py       # per-user settings
  export.py       # JSON/CSV exports
  i18n.py         # PL/EN/NO translations
assets/
  polsilver.svg   # source icon displayed in this README
  polsilver.png   # generated for packaged runtime icon
  polsilver.ico   # generated Windows executable icon
tests/
tools/build_icon.py
.github/workflows/
```

---

## Responsible use

Bluetooth identifiers and advertisements can be privacy-sensitive. Do not collect, publish or retain scans of third-party devices without a legitimate reason and appropriate permission. Pairing and connection inspection must be used only with devices you own, administer, or have explicit authorization to test.

See [`SECURITY.md`](SECURITY.md) for the project's safety boundary.

---

**by Swir** — https://github.com/Swir
