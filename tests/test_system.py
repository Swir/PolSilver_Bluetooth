from polsilver import system as system_module
from polsilver.system import diagnostic_commands


def test_windows_diagnostics_are_read_only():
    commands = diagnostic_commands("windows")
    joined = " ".join(" ".join(cmd.argv).lower() for cmd in commands)
    assert "get-pnpdevice" in joined
    assert "get-service" in joined
    assert "get-winevent" in joined
    for forbidden in (
        "remove-",
        "disable-",
        "stop-service",
        "restart-service",
        "restart-computer",
        "stop-computer",
        "format.com",
        "format.exe",
        "shutdown.exe",
        "bettercap",
    ):
        assert forbidden not in joined


def test_linux_audit_restores_safe_inventory_and_history(monkeypatch):
    monkeypatch.setattr(system_module.shutil, "which", lambda name: f"/usr/bin/{name}")
    commands = diagnostic_commands("linux")
    joined = " ".join(" ".join(cmd.argv).lower() for cmd in commands)

    assert "bluetoothctl devices paired" in joined
    assert "bluetoothctl devices connected" in joined
    assert "journalctl --no-pager -u bluetooth -n 200" in joined
    assert "rfkill list bluetooth" in joined

    for forbidden in (
        "bettercap",
        "btmon",
        "rfkill block",
        "rfkill unblock",
        "systemctl restart",
        "hciconfig hci0 piscan",
        "apt-get",
    ):
        assert forbidden not in joined


def test_wireshark_launcher_does_not_build_capture_arguments(monkeypatch):
    calls = []
    monkeypatch.setattr(system_module.shutil, "which", lambda name: "C:/Tools/Wireshark/wireshark.exe" if "wireshark" in name else None)
    monkeypatch.setattr(system_module.subprocess, "Popen", lambda argv, shell=False: calls.append((argv, shell)))

    result = system_module.launch_wireshark()

    assert calls == [(["C:/Tools/Wireshark/wireshark.exe"], False)]
    assert "launched" in result.lower()
