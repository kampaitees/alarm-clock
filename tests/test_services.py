from pathlib import Path

from alarm_clock.services import AlarmService
from alarm_clock.storage import JsonAlarmStorage


def test_create_and_cancel(tmp_path: Path) -> None:
    service = AlarmService(JsonAlarmStorage(tmp_path / "alarms.json"))
    alarm = service.create("16:00", "Test")
    assert service.cancel(alarm.id) is True
    assert service.list_alarms()[0].enabled is False
