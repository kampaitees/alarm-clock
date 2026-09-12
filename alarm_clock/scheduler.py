from datetime import date, datetime, timedelta
from typing import Protocol

from .models import Alarm


class Clock(Protocol):
    def now(self) -> datetime:
        ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now()


def next_occurrence(alarm: Alarm, now: datetime) -> datetime:
    """Return the next datetime at which an enabled alarm should fire."""
    alarm.validate()
    target = alarm.parsed_time()
    candidate = datetime.combine(now.date(), target)

    if alarm.recurring:
        if candidate < now:
            candidate += timedelta(days=1)
        return candidate

    # A one-shot alarm is interpreted as today's alarm when still upcoming.
    return candidate


class AlarmScheduler:
    """Evaluate alarms against an injected clock and trigger due alarms."""

    def __init__(self, clock: Clock | None = None) -> None:
        self.clock = clock or SystemClock()

    def due(self, alarms: list[Alarm]) -> list[Alarm]:
        now = self.clock.now()
        due_alarms: list[Alarm] = []
        for alarm in alarms:
            if not alarm.enabled:
                continue
            if alarm.recurring:
                # A recurring alarm is due when its HH:MM matches the current
                # local minute. Ignore seconds so the alarm can fire during the
                # whole minute rather than only at exactly second 0.
                target = alarm.parsed_time()
                if target.hour == now.hour and target.minute == now.minute:
                    due_alarms.append(alarm)
            else:
                occurrence = next_occurrence(alarm, now)
                if occurrence <= now and occurrence.date() == now.date():
                    due_alarms.append(alarm)
        return due_alarms


def next_daily_time(alarm: Alarm, day: date) -> datetime:
    """Useful deterministic helper for tests and callers that need a date-specific occurrence."""
    return datetime.combine(day, alarm.parsed_time())
