# Changelog

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
