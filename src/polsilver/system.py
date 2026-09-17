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
        ]
    if current == "linux":
        commands = []
        if shutil.which("bluetoothctl"):
            commands.append(DiagnosticCommand("Controller status", ("bluetoothctl", "show")))
        if shutil.which("rfkill"):
            commands.append(DiagnosticCommand("RFKill status", ("rfkill", "list", "bluetooth")))
        if shutil.which("systemctl"):
            commands.append(DiagnosticCommand("Bluetooth service", ("systemctl", "--no-pager", "--full", "status", "bluetooth")))
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
