from __future__ import annotations

from dataclasses import dataclass
import platform
import shutil
import subprocess


@dataclass(frozen=True, slots=True)
class DiagnosticCommand:
    label: str
    argv: tuple[str, ...]


def diagnostic_commands(system: str | None = None) -> list[DiagnosticCommand]:
    """Return read-only commands for the local Bluetooth adapter only."""
    current = (system or platform.system()).lower()
    if current == "windows":
        return [
            DiagnosticCommand(
                "Bluetooth PnP devices",
                (
                    "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                    "Get-PnpDevice -Class Bluetooth | Select-Object Status,Class,FriendlyName,InstanceId | Format-Table -AutoSize",
                ),
            ),
            DiagnosticCommand(
                "Bluetooth service",
                (
                    "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                    "Get-Service bthserv | Select-Object Status,StartType,Name | Format-Table -AutoSize",
                ),
            ),
            DiagnosticCommand(
                "Recent Bluetooth system events",
                (
                    "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                    "Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='BTHUSB'} -MaxEvents 40 -ErrorAction SilentlyContinue | Select-Object TimeCreated,Id,LevelDisplayName,Message | Format-List",
                ),
            ),
        ]
    if current == "linux":
        commands: list[DiagnosticCommand] = []
        if shutil.which("bluetoothctl"):
            commands.extend(
                [
                    DiagnosticCommand("Controller status", ("bluetoothctl", "show")),
                    DiagnosticCommand("Paired devices", ("bluetoothctl", "devices", "Paired")),
                    DiagnosticCommand("Connected devices", ("bluetoothctl", "devices", "Connected")),
                ]
            )
        if shutil.which("rfkill"):
            commands.append(DiagnosticCommand("RFKill status", ("rfkill", "list", "bluetooth")))
        if shutil.which("systemctl"):
            commands.append(DiagnosticCommand("Bluetooth service", ("systemctl", "--no-pager", "--full", "status", "bluetooth")))
        if shutil.which("journalctl"):
            commands.append(
                DiagnosticCommand(
                    "Recent Bluetooth connection history",
                    ("journalctl", "--no-pager", "-u", "bluetooth", "-n", "200"),
                )
            )
        return commands
    return []


def run_local_diagnostics(system: str | None = None, timeout: float = 8.0) -> str:
    reports: list[str] = []
    for command in diagnostic_commands(system):
        reports.append(f"=== {command.label} ===")
        try:
            completed = subprocess.run(
                list(command.argv),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                shell=False,
            )
            output = (completed.stdout or completed.stderr or "(no output)").strip()
            reports.append(output)
            reports.append(f"exit code: {completed.returncode}")
        except (OSError, subprocess.TimeoutExpired) as exc:
            reports.append(f"unavailable: {exc}")
    if not reports:
        return "No read-only adapter diagnostics are defined for this operating system."
    return "\n".join(reports)


def launch_wireshark() -> str:
    """Launch an installed local Wireshark GUI without configuring or starting a capture."""
    executable = shutil.which("wireshark") or shutil.which("wireshark.exe")
    if not executable:
        return "Wireshark was not found in PATH."
    try:
        subprocess.Popen([executable], shell=False)
    except OSError as exc:
        return f"Could not launch Wireshark: {exc}"
    return "Wireshark launched. Start captures only on interfaces/traffic you are authorized to inspect."
