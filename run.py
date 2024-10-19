import asyncio
from bleak import BleakScanner, BleakClient, BleakError
from colorama import Fore, init
import subprocess
import platform

# ASCII Art for PolSilver
def display_ascii_art():
    print(f"{Fore.CYAN}")
    print(r"""
      ___           ___           ___       ___                       ___       ___           ___           ___     
     /\  \         /\  \         /\__\     /\  \          ___        /\__\     /\__\         /\  \         /\  \    
    /::\  \       /::\  \       /:/  /    /::\  \        /\  \      /:/  /    /:/  /        /::\  \       /::\  \   
   /:/\:\  \     /:/\:\  \     /:/  /    /:/\ \  \       \:\  \    /:/  /    /:/  /        /:/\:\  \     /:/\:\  \  
  /::\~\:\  \   /:/  \:\  \   /:/  /    _\:\~\ \  \      /::\__\  /:/  /    /:/__/  ___   /::\~\:\  \   /::\~\:\  \ 
 /:/\:\ \:\__\ /:/__/ \:\__\ /:/__/    /\ \:\ \ \__\  __/:/\/__/ /:/__/     |:|  | /\__\ /:/\:\ \:\__\ /:/\:\ \:\__\
 \/__\:\/:/  / \:\  \ /:/  / \:\  \    \:\ \:\ \/__/ /\/:/  /    \:\  \     |:|  |/:/  / \:\~\:\ \/__/ \/_|::\/:/  /
      \::/  /   \:\  /:/  /   \:\  \    \:\ \:\__\   \::/__/      \:\  \    |:|__/:/  /   \:\ \:\__\      |:|::/  / 
       \/__/     \:\/:/  /     \:\  \    \:\/:/  /    \:\__\       \:\  \    \::::/__/     \:\ \/__/      |:|\/__/  
                  \::/  /       \:\__\    \::/  /      \/__/        \:\__\    ~~~~          \:\__\        |:|  |    
                   \/__/         \/__/     \/__/                     \/__/                   \/__/         \|__| 
                                   
    """)

# Inicjalizacja kolorów terminala
init(autoreset=True)

# Wykrywanie systemu operacyjnego
is_linux = platform.system().lower() == "linux"
is_windows = platform.system().lower() == "windows"

# Funkcja wyświetlająca menu
def menu():
    print(f"\n{Fore.CYAN}--- PolSilver Bluetooth Security Tool by Swir ---")
    print(f"{Fore.GREEN}1. Skanowanie urządzeń Bluetooth (BLE)")
    print(f"{Fore.GREEN}2. Test siły sygnału (RSSI) dla wszystkich urządzeń BLE")
    print(f"{Fore.GREEN}3. Sprawdzenie wersji protokołu Bluetooth (BLE)")
    print(f"{Fore.GREEN}4. Próba nawiązania połączenia bez autoryzacji (BLE)")
    print(f"{Fore.GREEN}5. Sparowanie urządzenia (BLE)")
    print(f"{Fore.GREEN}6. Test mocy urządzenia (Tylko Linux)")
    print(f"{Fore.GREEN}7. Test podatności na sniffing (Tylko Linux)")
    print(f"{Fore.GREEN}8. Próba ataku MITM (Tylko Linux)")
    print(f"{Fore.GREEN}9. Test szyfrowania połączenia (Wireshark)")
    print(f"{Fore.GREEN}10. Odłączenie urządzenia BLE")
    print(f"{Fore.GREEN}11. Restartowanie interfejsu Bluetooth (Tylko Linux)")
    print(f"{Fore.GREEN}12. Sprawdzanie historii połączeń Bluetooth (Tylko Linux)")
    print(f"{Fore.GREEN}13. Sprawdzenie zabezpieczeń parowania")
    print(f"{Fore.GREEN}14. Tryb widoczności Bluetooth (Tylko Linux)")
    print(f"{Fore.GREEN}15. Wyświetlenie listy sparowanych urządzeń (Tylko Linux)")
    print(f"{Fore.GREEN}16. Resetowanie ustawień Bluetooth (Tylko Linux)")
    print(f"{Fore.GREEN}17. Sprawdzanie poziomu baterii urządzenia (BLE)")
    print(f"{Fore.GREEN}18. Aktualizacja oprogramowania Bluetooth (Tylko Linux)")
    print(f"{Fore.RED}0. Wyjście")
    choice = input(f"{Fore.CYAN}Wybierz opcję: ")
    return choice

# Funkcja do obsługi błędów wywołania procesów systemowych
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Błąd podczas wywołania komendy: {e}")
        return None

# Funkcja do uruchamiania Wireshark
def start_wireshark():
    print(f"{Fore.CYAN}Uruchamiam Wireshark do przechwytywania pakietów...")
    try:
        if is_linux or is_windows:
            run_command(['wireshark'])
        else:
            print(f"{Fore.RED}Wireshark nie został znaleziony.")
    except Exception as e:
        print(f"{Fore.RED}Błąd podczas uruchamiania Wireshark: {e}")

# Funkcja do skanowania urządzeń BLE
async def scan_for_devices():
    print(f"\n{Fore.CYAN}Skanowanie urządzeń Bluetooth...")
    try:
        devices = await BleakScanner.discover()
        if devices:
            print(f"{Fore.GREEN}Znalezione urządzenia:")
            for device in devices:
                name = device.name if device.name else f"{Fore.YELLOW}Brak nazwy (None)"
                print(f"Urządzenie: {name}, Adres MAC: {device.address}")
        else:
            print(f"{Fore.RED}Brak urządzeń Bluetooth w zasięgu.")
    except Exception as e:
        print(f"{Fore.RED}Błąd podczas skanowania urządzeń: {e}")

# Funkcja do testowania siły sygnału (RSSI)
async def test_signal_strength_all():
    print(f"\n{Fore.CYAN}Skanowanie urządzeń Bluetooth w celu pomiaru siły sygnału (RSSI)...")
    try:
        devices = await BleakScanner.discover()
        if devices:
            print(f"{Fore.GREEN}Urządzenia i ich siła sygnału (RSSI):")
            for device in devices:
                name = device.name if device.name else f"{Fore.YELLOW}Brak nazwy (None)"
                rssi = device.rssi if device.rssi is not None else f"{Fore.RED}Brak danych RSSI"
                print(f"Urządzenie: {name}, Adres MAC: {device.address}, RSSI: {rssi} dBm")
        else:
            print(f"{Fore.RED}Brak urządzeń Bluetooth w zasięgu.")
    except Exception as e:
        print(f"{Fore.RED}Błąd podczas testowania RSSI: {e}")

# Funkcja do sprawdzenia wersji protokołu Bluetooth (BLE)
async def check_bluetooth_version():
    address = input(f"{Fore.CYAN}Podaj adres MAC urządzenia: ")
    print(f"{Fore.CYAN}Skanowanie urządzeń w pobliżu...")
    try:
        devices = await BleakScanner.discover()
        device_found = False
        for device in devices:
            if device.address == address:
                device_found = True
                break
        if not device_found:
            print(f"{Fore.RED}Urządzenie z adresem {address} nie zostało znalezione. Upewnij się, że jest w zasięgu.")
            return
        async with BleakClient(address, timeout=15.0) as client:
            services = await client.get_services()
            print(f"{Fore.GREEN}Wersja protokołu Bluetooth dla urządzenia {address}: BLE")
    except BleakError as e:
        print(f"{Fore.RED}Błąd połączenia: {e}")
    except Exception as e:
        print(f"{Fore.RED}Błąd podczas sprawdzania wersji Bluetooth: {e}")

# Funkcja do próby nawiązania połączenia bez autoryzacji
async def attempt_unauthorized_connection():
    address = input(f"{Fore.CYAN}Podaj adres MAC urządzenia: ")
    try:
        async with BleakClient(address, timeout=15.0) as client:
            await client.connect()
            print(f"{Fore.GREEN}Połączenie nawiązane z {address}")
            await client.disconnect()
    except BleakError as e:
        print(f"{Fore.RED}Błąd podczas nawiązywania połączenia: {e}")
    except Exception as e:
        print(f"{Fore.RED}Błąd: {e}")

# Funkcja do sparowania urządzenia BLE
async def pair_device():
    address = input(f"{Fore.CYAN}Podaj adres MAC urządzenia: ")
    try:
        async with BleakClient(address) as client:
            await client.pair()
            print(f"{Fore.GREEN}Sparowanie z urządzeniem {address} zakończone sukcesem.")
    except BleakError as e:
        print(f"{Fore.RED}Błąd podczas parowania: {e}")
    except Exception as e:
        print(f"{Fore.RED}Błąd: {e}")

# Funkcja do sniffingu z użyciem btmon (Linux only)
def test_sniffing():
    if is_linux:
        print(f"{Fore.CYAN}Uruchamiam btmon do monitorowania pakietów Bluetooth...")
        result = run_command(['btmon'])
        if result:
            print(result)
    else:
        print(f"{Fore.RED}Opcja dostępna tylko na Linux.")

# Funkcja do ataku MITM
def mitm_attack():
    if is_linux:
        print(f"{Fore.CYAN}Uruchamiam Bettercap do ataku MITM...")
        result = run_command(['sudo', 'bettercap', '-X'])
        if result:
            print(result)
    else:
        print(f"{Fore.RED}Opcja dostępna tylko na Linux.")

# Funkcja do odłączenia urządzenia BLE
async def disconnect_device():
    address = input(f"{Fore.CYAN}Podaj adres MAC urządzenia do odłączenia: ")
    try:
        async with BleakClient(address) as client:
            await client.disconnect()
            print(f"{Fore.GREEN}Urządzenie {address} zostało odłączone.")
    except BleakError as e:
        print(f"{Fore.RED}Błąd podczas odłączania urządzenia: {e}")
    except Exception as e:
        print(f"{Fore.RED}Błąd: {e}")

# Funkcja do restartowania interfejsu Bluetooth (Linux only)
def restart_bluetooth():
    if is_linux:
        print(f"{Fore.CYAN}Restartowanie interfejsu Bluetooth...")
        result = run_command(['sudo', 'systemctl', 'restart', 'bluetooth'])
        if result:
            print(result)
    else:
        print(f"{Fore.RED}Opcja dostępna tylko na Linux.")

# Funkcja do sprawdzania historii połączeń Bluetooth (Linux only)
def check_bluetooth_history():
    if is_linux:
        print(f"{Fore.CYAN}Wyświetlanie historii połączeń Bluetooth...")
        result = run_command(['sudo', 'journalctl', '-u', 'bluetooth'])
        if result:
            print(result)
    else:
        print(f"{Fore.RED}Opcja dostępna tylko na Linux.")

# Funkcja do sprawdzenia zabezpieczeń parowania
async def check_pairing_security():
    address = input(f"{Fore.CYAN}Podaj adres MAC urządzenia do sprawdzenia parowania: ")
    try:
        async with BleakClient(address) as client:
            paired = await client.is_paired()
            if paired:
                print(f"{Fore.GREEN}Urządzenie {address} jest sparowane.")
            else:
                print(f"{Fore.YELLOW}Urządzenie {address} nie jest sparowane.")
    except BleakError as e:
        print(f"{Fore.RED}Błąd podczas sprawdzania parowania: {e}")
    except Exception as e:
        print(f"{Fore.RED}Błąd: {e}")

# Funkcja do przełączania trybu widoczności Bluetooth (Linux only)
def toggle_bluetooth_visibility():
    if is_linux:
        print(f"{Fore.CYAN}Przełączanie trybu widoczności Bluetooth...")
        run_command(['sudo', 'hciconfig', 'hci0', 'piscan'])
        print(f"{Fore.GREEN}Widoczność Bluetooth została włączona.")
    else:
        print(f"{Fore.RED}Opcja dostępna tylko na Linux.")

# Funkcja do resetowania ustawień Bluetooth (Linux only)
def reset_bluetooth_settings():
    if is_linux:
        print(f"{Fore.CYAN}Resetowanie ustawień Bluetooth...")
        result = run_command(['sudo', 'rfkill', 'block', 'bluetooth'])
        run_command(['sudo', 'rfkill', 'unblock', 'bluetooth'])
        if result:
            print(f"{Fore.GREEN}Ustawienia Bluetooth zostały zresetowane.")
    else:
        print(f"{Fore.RED}Opcja dostępna tylko na Linux.")

# Funkcja do aktualizacji oprogramowania Bluetooth (Linux only)
def update_bluetooth_firmware():
    if is_linux:
        print(f"{Fore.CYAN}Aktualizacja oprogramowania Bluetooth...")
        result = run_command(['sudo', 'apt-get', 'install', '--only-upgrade', 'bluez'])
        if result:
            print(result)
    else:
        print(f"{Fore.RED}Opcja dostępna tylko na Linux.")

# Funkcja do sprawdzania poziomu baterii urządzeń BLE
async def check_battery_level():
    address = input(f"{Fore.CYAN}Podaj adres MAC urządzenia: ")
    try:
        async with BleakClient(address, timeout=15.0) as client:
            battery_level = await client.read_gatt_char("00002a19-0000-1000-8000-00805f9b34fb")
            print(f"{Fore.GREEN}Poziom baterii urządzenia {address}: {int(battery_level[0])}%")
    except BleakError as e:
        print(f"{Fore.RED}Błąd podczas odczytu poziomu baterii: {e}")
    except Exception as e:
        print(f"{Fore.RED}Błąd: {e}")

# Główna pętla programu
if __name__ == "__main__":
    display_ascii_art()  # Wyświetl ASCII art na początku
    while True:
        choice = menu()
        
        # Opcje dostępne zarówno na Windows, jak i Linux
        if choice == '1':
            asyncio.run(scan_for_devices())
        elif choice == '2':
            asyncio.run(test_signal_strength_all())
        elif choice == '3':
            asyncio.run(check_bluetooth_version())
        elif choice == '4':
            asyncio.run(attempt_unauthorized_connection())
        elif choice == '5':
            asyncio.run(pair_device())
        elif choice == '9':
            start_wireshark()
        elif choice == '10':
            asyncio.run(disconnect_device())
        
        # Opcje dostępne tylko na Linux
        elif choice == '6':
            if is_linux:
                restart_bluetooth()
            else:
                print(f"{Fore.RED}Opcja dostępna tylko na Linux.")
        elif choice == '7':
            if is_linux:
                test_sniffing()
            else:
                print(f"{Fore.RED}Opcja dostępna tylko na Linux.")
        elif choice == '8':
            mitm_attack()
        elif choice == '11':
            if is_linux:
                restart_bluetooth()
            else:
                print(f"{Fore.RED}Opcja dostępna tylko na Linux.")
        elif choice == '12':
            check_bluetooth_history()
        elif choice == '13':
            asyncio.run(check_pairing_security())
        elif choice == '14':
            toggle_bluetooth_visibility()
        elif choice == '15':
            print(f"{Fore.YELLOW}Wyświetlenie listy sparowanych urządzeń - w trakcie rozwoju.")
        elif choice == '16':
            reset_bluetooth_settings()
        elif choice == '17':
            asyncio.run(check_battery_level())
        elif choice == '18':
            update_bluetooth_firmware()
        
        # Wyjście
        elif choice == '0':
            print(f"{Fore.GREEN}Zamykanie programu...")
            break
        
        # Nieprawidłowy wybór
        else:
            print(f"{Fore.RED}Nieprawidłowy wybór.")
