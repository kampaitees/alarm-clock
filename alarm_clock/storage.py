import json
from pathlib import Path
from typing import Iterable

from .models import Alarm


class JsonAlarmStorage:
    """Small file-backed repository; intentionally avoids database infrastructure."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[Alarm]:
        if not self.path.exists():
            return []

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Could not parse alarm file: {self.path}") from exc

        if not isinstance(raw, list):
            raise RuntimeError("Alarm storage must contain a JSON array")

        return [Alarm.from_dict(item) for item in raw]

    def save(self, alarms: Iterable[Alarm]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [alarm.to_dict() for alarm in alarms]
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temp_path.replace(self.path)
