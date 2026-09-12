from dataclasses import asdict, dataclass
from datetime import datetime, time
from typing import Any


TIME_FORMAT = "%H:%M"


@dataclass
class Alarm:
    id: str
    time: str
    label: str
    recurring: bool = False
    enabled: bool = True

    def validate(self) -> None:
        try:
            datetime.strptime(self.time, TIME_FORMAT)
        except ValueError as exc:
            raise ValueError("Alarm time must use HH:MM format, e.g. 08:30") from exc

        if not self.label.strip():
            raise ValueError("Alarm label cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Alarm":
        alarm = cls(
            id=str(data["id"]),
            time=str(data["time"]),
            label=str(data["label"]),
            recurring=bool(data.get("recurring", False)),
            enabled=bool(data.get("enabled", True)),
        )
        alarm.validate()
        return alarm

    def parsed_time(self) -> time:
        return datetime.strptime(self.time, TIME_FORMAT).time()
