<div align="center">

# 🛡️ PolSilver Bluetooth Security Tool

**Cross-platform BLE diagnostics & authorized security testing**  
**Wieloplatformowa diagnostyka BLE i autoryzowane testy bezpieczeństwa**

![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?logo=python&logoColor=white)
![BLE](https://img.shields.io/badge/Bluetooth-BLE-0082FC?logo=bluetooth&logoColor=white)
![Platforms](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

</div>

---

## 🇵🇱 Polski

**PolSilver Bluetooth Security Tool** to napisany w Pythonie zestaw narzędzi do diagnostyki urządzeń Bluetooth Low Energy oraz testów bezpieczeństwa wykonywanych we własnym środowisku lub za zgodą właściciela urządzenia.

### 🔎 Najważniejsze możliwości
- wykrywanie pobliskich urządzeń BLE
- odczyt i porównywanie siły sygnału RSSI
- przegląd usług udostępnianych przez urządzenia BLE
- sprawdzanie stanu połączenia i parowania
- odczyt poziomu baterii, gdy urządzenie udostępnia odpowiednią usługę
- rozłączanie obsługiwanych połączeń
- funkcje administracyjne Bluetooth zależne od systemu
- integracja z systemowymi narzędziami diagnostycznymi na Linuxie
- integracja z Wiresharkiem do analizy ruchu we własnym środowisku testowym
- wersja konsolowa i GUI

### 🚀 Instalacja
```bash
git clone https://github.com/Swir/PolSilver_Bluetooth.git
cd PolSilver_Bluetooth
pip install bleak colorama
```

### ▶️ Uruchomienie
Wersja konsolowa:
```bash
python run.py
```

W repozytorium znajduje się również wariant GUI w pliku `GUI Ver,py`.

### 🐧 Linux
Niektóre funkcje korzystają z narzędzi dostępnych w systemach Linux, takich jak stos BlueZ i narzędzia diagnostyczne Bluetooth. Ich dostępność zależy od dystrybucji, adaptera oraz uprawnień użytkownika.

### ⚠️ Bezpieczeństwo i legalne użycie
Projekt jest przeznaczony do **diagnostyki, nauki oraz autoryzowanych testów bezpieczeństwa**. Korzystaj z funkcji analizy i testowania połączeń wyłącznie na urządzeniach, które należą do Ciebie lub dla których masz wyraźną zgodę właściciela. Niektóre operacje mogą rozłączyć urządzenie albo zmienić konfigurację lokalnego interfejsu Bluetooth.

---

## 🇬🇧 English

**PolSilver Bluetooth Security Tool** is a Python toolkit for Bluetooth Low Energy diagnostics and security testing in your own environment or on devices you have explicit permission to test.

### 🔎 Main capabilities
- nearby BLE device discovery
- RSSI signal-strength inspection
- BLE service inspection
- connection and pairing-status checks
- battery-level reading when supported by the device
- supported connection management
- platform-dependent Bluetooth administration
- integration with Linux Bluetooth diagnostic utilities
- Wireshark integration for analysis in an authorized test environment
- console and GUI variants

### 🚀 Installation
```bash
git clone https://github.com/Swir/PolSilver_Bluetooth.git
cd PolSilver_Bluetooth
pip install bleak colorama
```

### ▶️ Run
Console version:
```bash
python run.py
```

A GUI variant is also included as `GUI Ver,py`.

### 🐧 Linux
Some functionality relies on Linux Bluetooth tooling such as the BlueZ stack and diagnostic utilities. Availability depends on the distribution, Bluetooth adapter and user privileges.

### ⚠️ Security & authorized use
This project is intended for **diagnostics, education and authorized security testing**. Analyze or test Bluetooth connections only on devices you own or have explicit permission to assess. Some operations can disconnect devices or modify the local Bluetooth interface configuration.

---

## 👤 Author / Autor
Developed and maintained by **Swir**.
