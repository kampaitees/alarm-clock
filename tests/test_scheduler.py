from datetime import datetime

from alarm_clock.models import Alarm
from alarm_clock.scheduler import AlarmScheduler, next_occurrence


class FakeClock:
    def __init__(self, current: datetime) -> None:
        self.current = current

    def now(self) -> datetime:
        return self.current


def test_future_daily_alarm_is_due_at_its_minute() -> None:
    alarm = Alarm("a1", "14:30", "Meeting", recurring=True)
    clock = FakeClock(datetime(2026, 9, 12, 14, 30, 10))
    assert alarm in AlarmScheduler(clock).due([alarm])


def test_daily_alarm_rolls_to_tomorrow_after_time_passes() -> None:
    alarm = Alarm("a1", "08:00", "Morning", recurring=True)
    now = datetime(2026, 9, 12, 9, 0)
    occurrence = next_occurrence(alarm, now)
    assert occurrence == datetime(2026, 9, 13, 8, 0)


def test_one_time_alarm_is_due_after_its_time() -> None:
    alarm = Alarm("a1", "08:00", "Wake", recurring=False)
    clock = FakeClock(datetime(2026, 9, 12, 8, 5))
    assert alarm in AlarmScheduler(clock).due([alarm])


def test_disabled_alarm_is_not_due() -> None:
    alarm = Alarm("a1", "08:00", "Wake", enabled=False)
    clock = FakeClock(datetime(2026, 9, 12, 8, 5))
    assert AlarmScheduler(clock).due([alarm]) == []
