import argparse
import time as time_module
from pathlib import Path

from .services import AlarmService
from .storage import JsonAlarmStorage

DEFAULT_STORAGE = Path.home() / ".alarm_clock" / "alarms.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="alarm-clock",
        description="A small persistent Python CLI alarm clock.",
    )
    parser.add_argument("--data", type=Path, default=DEFAULT_STORAGE, help="Path to the JSON alarm file")
    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set", help="Create an alarm")
    set_parser.add_argument("time", help="Alarm time in HH:MM, e.g. 08:30")
    set_parser.add_argument("--label", default="Alarm", help="Alarm label")
    set_parser.add_argument("--daily", action="store_true", help="Repeat every day")

    subparsers.add_parser("list", help="List alarms")

    cancel_parser = subparsers.add_parser("cancel", help="Disable an alarm")
    cancel_parser.add_argument("alarm_id")

    delete_parser = subparsers.add_parser("delete", help="Delete an alarm")
    delete_parser.add_argument("alarm_id")

    subparsers.add_parser("run", help="Run the alarm clock")
    return parser


def print_alarms(alarms) -> None:
    if not alarms:
        print("No alarms configured.")
        return
    print("ID      TIME   TYPE    STATUS   LABEL")
    print("------  -----  ------  -------  ----------------")
    for alarm in alarms:
        alarm_type = "DAILY" if alarm.recurring else "ONCE"
        status = "ACTIVE" if alarm.enabled else "OFF"
        print(f"{alarm.id:<7} {alarm.time:<6} {alarm_type:<7} {status:<8} {alarm.label}")


def run_clock(service: AlarmService) -> None:
    print("Alarm clock is running. Press Ctrl+C to stop.")
    fired_minute_keys: set[tuple[str, str]] = set()
    try:
        while True:
            alarms = service.list_alarms()
            now = service.scheduler.clock.now()
            due = service.scheduler.due(alarms)
            for alarm in due:
                key = (alarm.id, now.strftime("%Y-%m-%d %H:%M"))
                if key in fired_minute_keys:
                    continue
                fired_minute_keys.add(key)
                print(f"\n\a⏰ ALARM: {alarm.label} ({alarm.time})")
                print("Press Ctrl+C to dismiss. Use 'set' to create a new alarm or stop the clock to snooze manually.")
                service.mark_fired(alarm)
            time_module.sleep(1)
    except KeyboardInterrupt:
        print("\nAlarm clock stopped.")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    storage = JsonAlarmStorage(args.data)
    service = AlarmService(storage)

    try:
        if args.command == "set":
            alarm = service.create(args.time, args.label, args.daily)
            kind = "daily" if alarm.recurring else "one-time"
            print(f"Created {kind} alarm {alarm.id} for {alarm.time}: {alarm.label}")
        elif args.command == "list":
            print_alarms(service.list_alarms())
        elif args.command == "cancel":
            print("Alarm cancelled." if service.cancel(args.alarm_id) else "Alarm not found.")
        elif args.command == "delete":
            print("Alarm deleted." if service.delete(args.alarm_id) else "Alarm not found.")
        elif args.command == "run":
            run_clock(service)
    except (ValueError, RuntimeError) as exc:
        parser.error(str(exc))
