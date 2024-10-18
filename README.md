# PolSilver Bluetooth Security Tool  by Swir

**Bluetooth Security Tool** to wieloplatformowe narzędzie do testowania bezpieczeństwa urządzeń Bluetooth, oparte na **Python**. Narzędzie umożliwia przeprowadzanie różnych testów związanych z Bluetooth Low Energy (BLE), takich jak skanowanie urządzeń, testowanie siły sygnału (RSSI), próby połączeń, sniffing i analiza szyfrowania. 

### Funkcje:

1. **Skanowanie urządzeń Bluetooth (BLE)** – skanuje wszystkie urządzenia BLE w zasięgu.
2. **Test siły sygnału (RSSI)** – wyświetla siłę sygnału RSSI dla wszystkich urządzeń BLE.
3. **Sprawdzenie wersji protokołu Bluetooth (BLE)** – pokazuje dostępne usługi BLE dla wybranego urządzenia.
4. **Próba nawiązania połączenia bez autoryzacji (BLE)** – testuje możliwość połączenia się z urządzeniem BLE bez wcześniejszego sparowania.
5. **Sparowanie urządzenia (BLE)** – paruje urządzenie BLE z komputerem.
6. **Test mocy urządzenia (Tylko Linux)** – wyświetla klasę urządzenia Bluetooth przy użyciu narzędzia `hciconfig`.
7. **Test podatności na sniffing (Tylko Linux)** – uruchamia `btmon` do monitorowania pakietów Bluetooth.
8. **Próba ataku MITM (Tylko Linux)** – uruchamia narzędzie `Bettercap`, które przeprowadza atak Man-in-the-Middle (MITM) na połączenia Bluetooth.
9. **Test szyfrowania połączenia (Tylko Linux)** – uruchamia Wireshark do przechwytywania i analizy pakietów Bluetooth.
10. **Test szyfrowania połączenia (Wireshark)** – dostępny na Linux i Windows, uruchamia Wireshark do analizy szyfrowania połączeń Bluetooth.

### Wymagania:

#### Windows:
- Python 3.7+
- Biblioteka **Bleak** (`pip install bleak`)
- **Wireshark** (dla testów sniffingu i szyfrowania połączeń)

#### Linux:
- Python 3.7+
- Biblioteka **Bleak** (`pip install bleak`)
- **Wireshark**
- **Bettercap** (dla ataku MITM)
- **btmon** (do sniffingu)
- **hciconfig** (do testu klasy urządzenia)

### Instalacja:

1. Sklonuj repozytorium:
    ```bash
    git clone https://github.com/your-username/PolSilver_Bluetooth.git
    cd bluetooth-security-tool
    ```

2. Zainstaluj wymagane zależności:
    ```bash
    pip install bleak
    ```

3. Zainstaluj **Wireshark**:
    - **Windows**: Pobierz i zainstaluj Wireshark z oficjalnej strony: [Wireshark](https://www.wireshark.org/)
    - **Linux**: Zainstaluj Wireshark za pomocą menedżera pakietów:
      ```bash
      sudo apt-get install wireshark
      ```

4. (Opcjonalnie dla Linux) Zainstaluj dodatkowe narzędzia:
    ```bash
    sudo apt-get install bettercap bluez
    ```

### Użycie:

1. Uruchom program:
    ```bash
    python bluetooth_security_tool.py
    ```

2. Wybierz opcję z menu, aby przeprowadzić test Bluetooth.

    - Funkcje takie jak **skanowanie urządzeń**, **testy RSSI**, oraz **sprawdzanie wersji protokołu BLE** są dostępne na obu systemach.
    - Opcje związane z sniffingiem, atakiem MITM i testem klasy urządzenia są dostępne tylko na **Linux**.
    - Wireshark może być używany zarówno na **Windows**, jak i **Linux** do analizy szyfrowania połączeń.
    - Uwagi:

    Niektóre opcje są dostępne tylko na Linux, ale wszystkie są wyświetlane w menu. Program powiadomi Cię, jeśli próbujesz uruchomić funkcję, która jest dostępna tylko na Linux, a Ty używasz Windows.
    Aby przechwytywać pakiety Bluetooth przy użyciu Wireshark, konieczne jest skonfigurowanie odpowiednich interfejsów na systemie.

### Przykład:

```bash
--- PolSilver Bluetooth Security Tool  by Swir ---
1. Skanowanie urządzeń Bluetooth (BLE)
2. Test siły sygnału (RSSI) dla wszystkich urządzeń BLE
3. Sprawdzenie wersji protokołu Bluetooth (BLE)
4. Próba nawiązania połączenia bez autoryzacji (BLE)
5. Sparowanie urządzenia (BLE)
6. Test mocy urządzenia (Tylko Linux)
7. Test podatności na sniffing (Tylko Linux)
8. Próba ataku MITM (Tylko Linux)
9. Test szyfrowania połączenia (Tylko Linux)
10. Test szyfrowania połączenia (Wireshark)
0. Wyjście
Wybierz opcję: 
Uwagi:

Uwagi:
