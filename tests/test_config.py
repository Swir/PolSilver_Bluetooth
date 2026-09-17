from polsilver.config import Settings


def test_settings_are_clamped_and_roundtrip(tmp_path):
    path = tmp_path / "settings.json"
    settings = Settings(language="pl", scan_seconds=99, connect_timeout=1)
    settings.save(path)
    loaded = Settings.load(path)
    assert loaded.language == "pl"
    assert loaded.scan_seconds == 20.0
    assert loaded.connect_timeout == 3.0
