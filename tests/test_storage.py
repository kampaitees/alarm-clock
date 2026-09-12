from pathlib import Path

from alarm_clock.models import Alarm
from alarm_clock.storage import JsonAlarmStorage


def test_storage_round_trip(tmp_path: Path) -> None:
    storage = JsonAlarmStorage(tmp_path / "alarms.json")
    alarms = [Alarm("abc123", "08:00", "Morning", recurring=True)]
    storage.save(alarms)
    loaded = storage.load()
    assert loaded == alarms
