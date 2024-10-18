# Bluetooth Security Tool

**English / Polski**

Bluetooth Security Tool is a cross-platform tool built with Python, designed to test the security of Bluetooth Low Energy (BLE) devices. It provides various functions such as scanning for BLE devices, testing signal strength, pairing, checking battery levels, and even more advanced operations like sniffing and MITM attacks (Linux only).

Bluetooth Security Tool to wieloplatformowe narzędzie stworzone w Pythonie, przeznaczone do testowania bezpieczeństwa urządzeń Bluetooth Low Energy (BLE). Oferuje różne funkcje, takie jak skanowanie urządzeń BLE, testowanie siły sygnału, parowanie, sprawdzanie poziomu baterii oraz bardziej zaawansowane operacje, takie jak sniffing i ataki MITM (dostępne tylko na Linuxie).

---

## Features / Funkcje:

1. **Scanning for Bluetooth (BLE) devices / Skanowanie urządzeń Bluetooth (BLE)**: Discovers all nearby BLE devices / Odkrywa wszystkie pobliskie urządzenia BLE.
2. **RSSI signal strength test / Test siły sygnału RSSI**: Displays the signal strength (RSSI) for each BLE device / Wyświetla siłę sygnału (RSSI) dla każdego urządzenia BLE.
3. **Check Bluetooth version (BLE) / Sprawdzanie wersji Bluetooth (BLE)**: Displays the Bluetooth protocol version and available services for a specific BLE device / Wyświetla wersję protokołu Bluetooth i dostępne usługi dla wybranego urządzenia BLE.
4. **Attempt connection without authorization (BLE) / Próba połączenia bez autoryzacji (BLE)**: Attempts to connect to a BLE device without pairing / Próbuje połączyć się z urządzeniem BLE bez parowania.
5. **Pair BLE device / Parowanie urządzenia BLE**: Pairs the BLE device with the computer / Paruje urządzenie BLE z komputerem.
6. **Test device power class (Linux only) / Test klasy mocy urządzenia (Tylko Linux)**: Displays the device power class (available only on Linux) / Wyświetla klasę mocy urządzenia (dostępne tylko na Linuxie).
7. **Test vulnerability to sniffing (Linux only) / Test podatności na sniffing (Tylko Linux)**: Uses `btmon` to monitor Bluetooth packets / Używa `btmon` do monitorowania pakietów Bluetooth.
8. **Attempt MITM attack (Linux only) / Próba ataku MITM (Tylko Linux)**: Launches the `Bettercap` tool to attempt a Man-in-the-Middle (MITM) attack on Bluetooth connections / Uruchamia narzędzie `Bettercap`, aby przeprowadzić atak Man-in-the-Middle (MITM) na połączenia Bluetooth.
9. **Test encryption with Wireshark / Test szyfrowania przy użyciu Wireshark**: Launches Wireshark to capture and analyze Bluetooth traffic (available on both Linux and Windows) / Uruchamia Wireshark do przechwytywania i analizy ruchu Bluetooth (dostępne na Linux i Windows).
10. **Disconnect BLE device / Odłączenie urządzenia BLE**: Disconnects a connected BLE device / Odłącza podłączone urządzenie BLE.
11. **Restart Bluetooth interface (Linux only) / Restartowanie interfejsu Bluetooth (Tylko Linux)**: Restarts the Bluetooth interface on Linux / Restartuje interfejs Bluetooth na Linuxie.
12. **Check Bluetooth connection history (Linux only) / Sprawdzanie historii połączeń Bluetooth (Tylko Linux)**: Lists all previously connected Bluetooth devices / Wyświetla listę wcześniej połączonych urządzeń Bluetooth.
13. **Check pairing security / Sprawdzenie zabezpieczeń parowania**: Verifies if a BLE device is paired with the computer / Weryfikuje, czy urządzenie BLE jest sparowane z komputerem.
14. **Toggle Bluetooth visibility (Linux only) / Przełączanie trybu widoczności Bluetooth (Tylko Linux)**: Enables or disables Bluetooth visibility / Włącza lub wyłącza widoczność Bluetooth.
15. **Show paired devices (Linux only) / Wyświetlenie listy sparowanych urządzeń (Tylko Linux)**: Lists all paired Bluetooth devices / Wyświetla listę sparowanych urządzeń Bluetooth.
16. **Reset Bluetooth settings / Resetowanie ustawień Bluetooth**: Resets Bluetooth settings (Linux/Windows) / Resetuje ustawienia Bluetooth (Linux/Windows).
17. **Check BLE device battery level / Sprawdzanie poziomu baterii urządzenia BLE**: Retrieves and displays the battery level of a BLE device / Wyświetla poziom baterii urządzenia BLE.
18. **Update Bluetooth firmware (Linux only) / Aktualizacja oprogramowania Bluetooth (Tylko Linux)**: Automatically updates the Bluetooth firmware / Automatyczna aktualizacja oprogramowania Bluetooth.

---

## Requirements / Wymagania:

### Windows:
- Python 3.7+
- [Bleak](https://pypi.org/project/bleak/) (`pip install bleak`)
- [Colorama](https://pypi.org/project/colorama/) (`pip install colorama`)
- [Wireshark](https://www.wireshark.org/) (optional for packet sniffing and encryption analysis / opcjonalnie do analizy ruchu i szyfrowania)

### Linux:
- Python 3.7+
- [Bleak](https://pypi.org/project/bleak/) (`pip install bleak`)
- [Colorama](https://pypi.org/project/colorama/) (`pip install colorama`)
- Wireshark (optional for packet sniffing and encryption analysis / opcjonalnie do analizy ruchu i szyfrowania)
- `btmon`, `hciconfig`, `bluez`, `Bettercap`

---

## Installation / Instalacja:

1. Clone the repository / Sklonuj repozytorium:
    ```bash
    git clone https://github.com/your-username/bluetooth-security-tool.git
    cd bluetooth-security-tool
    ```

2. Install the required dependencies / Zainstaluj wymagane zależności:
    ```bash
    pip install bleak colorama
    ```

3. On **Linux**, install additional Bluetooth tools / Na **Linux** zainstaluj dodatkowe narzędzia Bluetooth:
    ```bash
    sudo apt-get install wireshark bluez bettercap
    ```

4. On **Windows**, download and install Wireshark from [here](https://www.wireshark.org/) / Na **Windows** pobierz i zainstaluj Wireshark z [tutaj](https://www.wireshark.org/).

---

## Usage / Użycie:

1. Run the program / Uruchom program:
    ```bash
    python bluetooth_security_tool.py
    ```

2. The menu will appear. Choose one of the options to test Bluetooth security on your devices / Pojawi się menu. Wybierz jedną z opcji, aby przetestować bezpieczeństwo Bluetooth na urządzeniach.

Example of the menu / Przykład menu:
```bash
--- Bluetooth Security Tool ---
1. Scan for Bluetooth (BLE) devices / Skanowanie urządzeń Bluetooth (BLE)
2. Test RSSI signal strength / Test siły sygnału RSSI
3. Check Bluetooth version (BLE) / Sprawdzanie wersji Bluetooth (BLE)
4. Attempt connection without authorization (BLE) / Próba połączenia bez autoryzacji (BLE)
5. Pair BLE device / Parowanie urządzenia BLE
6. Test device power class (Linux only) / Test klasy mocy urządzenia (Tylko Linux)
7. Test vulnerability to sniffing (Linux only) / Test podatności na sniffing (Tylko Linux)
8. Attempt MITM attack (Linux only) / Próba ataku MITM (Tylko Linux)
9. Test encryption with Wireshark / Test szyfrowania przy użyciu Wireshark
10. Disconnect BLE device / Odłączenie urządzenia BLE
11. Restart Bluetooth interface (Linux only) / Restartowanie interfejsu Bluetooth (Tylko Linux)
12. Check Bluetooth connection history (Linux only) / Sprawdzanie historii połączeń Bluetooth (Tylko Linux)
13. Check pairing security / Sprawdzenie zabezpieczeń parowania
14. Toggle Bluetooth visibility (Linux only) / Przełączanie trybu widoczności Bluetooth (Tylko Linux)
15. Show paired devices (Linux only) / Wyświetlenie listy sparowanych urządzeń (Tylko Linux)
16. Reset Bluetooth settings / Resetowanie ustawień Bluetooth
17. Check BLE device battery level / Sprawdzanie poziomu baterii urządzenia BLE
18. Update Bluetooth firmware (Linux only) / Aktualizacja oprogramowania Bluetooth (Tylko Linux)
0. Exit / Wyjście
