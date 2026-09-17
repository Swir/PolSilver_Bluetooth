from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import locale
import os
from pathlib import Path


def config_dir() -> Path:
    if os.name == "nt":
        return Path(os.environ.get("APPDATA", Path.home())) / "PolSilverBluetooth"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "polsilver-bluetooth"


def detect_language() -> str:
    value = (locale.getlocale()[0] or os.environ.get("LANG", "en")).lower()
    if value.startswith("pl"):
        return "pl"
    if value.startswith("no") or value.startswith("nb") or value.startswith("nn"):
        return "no"
    return "en"


@dataclass(slots=True)
class Settings:
    language: str = "auto"
    scan_seconds: float = 5.0
    connect_timeout: float = 12.0
    remember_window: bool = True

    @property
    def resolved_language(self) -> str:
        return detect_language() if self.language == "auto" else self.language

    def validate(self) -> None:
        if self.language not in {"auto", "en", "pl", "no"}:
            self.language = "auto"
        self.scan_seconds = min(max(float(self.scan_seconds), 1.0), 20.0)
        self.connect_timeout = min(max(float(self.connect_timeout), 3.0), 30.0)

    def save(self, path: Path | None = None) -> Path:
        self.validate()
        target = path or config_dir() / "settings.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
        return target

    @classmethod
    def load(cls, path: Path | None = None) -> "Settings":
        target = path or config_dir() / "settings.json"
        data: dict = {}
        if target.exists():
            try:
                data = json.loads(target.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                data = {}
        known = set(cls.__dataclass_fields__)
        settings = cls(**{key: value for key, value in data.items() if key in known})
        settings.validate()
        return settings
