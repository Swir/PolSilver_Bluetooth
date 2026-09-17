from polsilver.system import diagnostic_commands


def test_windows_diagnostics_are_read_only():
    commands = diagnostic_commands("windows")
    joined = " ".join(" ".join(cmd.argv).lower() for cmd in commands)
    assert "get-pnpdevice" in joined
    assert "get-service" in joined
    for forbidden in ("remove-", "disable-", "stop-service", "format", "shutdown"):
        assert forbidden not in joined
