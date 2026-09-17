# Changelog

## 2.1.0 - 2026-09-17

### Restored after regression audit
- Explicit OS-backed pairing for one selected, authorized BLE device, protected by a confirmation dialog.
- Read-only paired/connected device inventory on Linux where BlueZ `bluetoothctl` exposes it.
- Recent Bluetooth service/connection history diagnostics using read-only OS logs on Linux and Windows.
- Local Wireshark launcher when Wireshark is already installed; no automatic capture/interception workflow is started.
- Diagnostics-log export to a text file.

### Improved
- The Windows packaged app now bundles the generated runtime icon, not only executable metadata icon resources.
- Packaged smoke testing constructs and briefly shows the real main window so GUI/resource regressions are detected before release.
- Double-clicking a scan result opens the same authorized GATT inspection path.
- README now displays the project icon and documents which legacy functions were safely restored versus intentionally omitted.

### Intentionally omitted
- MITM/Bettercap automation.
- "Unauthorized connection" testing.
- Forced sniffing/capture automation.
- Destructive Bluetooth reset or firmware/package modification.
- Forced visibility/restart actions.

## 2.0.0 - 2026-09-17

### Added
- modular `src/polsilver` architecture
- PySide6 dark-blue desktop UI
- PL/EN/NO localization with system-language detection
- bounded BLE discovery and RSSI quality classification
- authorized GATT inspection and standard battery characteristic reading
- read-only Windows/Linux adapter diagnostics
- JSON/CSV export and user-profile settings
- custom SVG/PNG/ICO branding pipeline
- Python 3.10–3.14 CI and Windows smoke test
- Windows EXE, portable ZIP and SHA256 release pipeline

### Changed
- consolidated the former console and GUI variants into one application
- moved runtime configuration outside the repository/application directory

### Removed
- legacy MITM/Bettercap action
- intrusive Bluetooth reset/firmware management actions
- ambiguous “unauthorized connection” workflow
- duplicate `GUI Ver,py` implementation
