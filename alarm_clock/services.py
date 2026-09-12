from datetime import datetime, timedelta
from uuid import uuid4

from .models import Alarm
from .scheduler import AlarmScheduler, Clock
from .storage import JsonAlarmStorage


class AlarmService:
    def __init__(self, storage: JsonAlarmStorage, clock: Clock | None = None) -> None:
        self.storage = storage
        self.scheduler = AlarmScheduler(clock)

    def list_alarms(self) -> list[Alarm]:
        return self.storage.load()

    def create(self, alarm_time: str, label: str, recurring: bool = False) -> Alarm:
        alarm = Alarm(
            id=uuid4().hex[:6],
            time=alarm_time,
            label=label.strip(),
            recurring=recurring,
            enabled=True,
        )
        alarm.validate()
        alarms = self.storage.load()
        alarms.append(alarm)
        self.storage.save(alarms)
        return alarm

    def cancel(self, alarm_id: str) -> bool:
        alarms = self.storage.load()
        for alarm in alarms:
            if alarm.id == alarm_id:
                alarm.enabled = False
                self.storage.save(alarms)
                return True
        return False

    def delete(self, alarm_id: str) -> bool:
        alarms = self.storage.load()
        new_alarms = [a for a in alarms if a.id != alarm_id]
        if len(new_alarms) == len(alarms):
            return False
        self.storage.save(new_alarms)
        return True

    def snooze(self, alarm: Alarm, minutes: int = 5) -> Alarm:
        now = self.scheduler.clock.now()
        target = now + timedelta(minutes=minutes)
        snoozed = Alarm(
            id=uuid4().hex[:6],
            time=target.strftime("%H:%M"),
            label=f"Snooze: {alarm.label}",
            recurring=False,
            enabled=True,
        )
        alarms = self.storage.load()
        alarms.append(snoozed)
        self.storage.save(alarms)
        return snoozed

    def mark_fired(self, alarm: Alarm) -> None:
        alarms = self.storage.load()
        for current in alarms:
            if current.id == alarm.id:
                if current.recurring:
                    # Daily alarms stay enabled; runtime keeps track of the fired minute.
                    return
                current.enabled = False
                break
        self.storage.save(alarms)
