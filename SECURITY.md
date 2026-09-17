# Security and responsible use

PolSilver Bluetooth is a local diagnostics utility. Use it only with Bluetooth devices you own, administer, or have explicit authorization to inspect or pair.

Version 2.1 limits active BLE functionality to bounded discovery plus explicit user-confirmed actions on one selected device. It does not automate credential bypass, MITM interception, destructive adapter changes or public/large-scale scanning.

## Active actions

- **Inspect selected device** connects to one selected BLE device to enumerate GATT metadata and read the standard battery characteristic when exposed. A confirmation dialog reminds the user of the authorization requirement.
- **Pair selected device** invokes the operating system's normal BLE pairing flow for one selected device and requires explicit confirmation in PolSilver first. The OS remains responsible for any PIN/passkey/consent interaction.
- **Open Wireshark** only launches an already installed local Wireshark application. PolSilver does not select an interface, start a capture, inject packets or configure interception.

## Read-only diagnostics

Local adapter reports use fixed read-only commands to inspect Bluetooth device/service state and recent local Bluetooth events. Linux paired/connected inventories and service history are read-only. Windows PnP/service/event queries do not modify devices or services.

## Intentionally unsupported legacy actions

The regression audit does not restore the old MITM/Bettercap workflow, "unauthorized connection" testing, forced sniffing, destructive reset/firmware actions, forced visibility changes or other intrusive operations.

## Privacy

Nearby BLE advertisements and hardware identifiers can be privacy-sensitive. Do not collect, publish or retain third-party device identifiers without a legitimate reason and appropriate permission. Saved JSON/CSV/log files remain under the user's control and should be protected accordingly.

## Reporting a vulnerability

Please avoid posting secrets, device identifiers or sensitive captures in a public issue. Describe the affected component and reproduction steps with sanitized data.
