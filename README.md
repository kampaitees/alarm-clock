# Alarm Clock CLI

A small, persistent command-line alarm clock written in Python. It supports one-time alarms, daily recurring alarms, cancellation, deletion, and a foreground scheduler loop.

The project is intentionally lightweight: alarms are stored in a local JSON file, runtime code uses only the Python standard library, and scheduling logic is separated from terminal I/O for straightforward testing.

## Features

- Create one-time alarms with a label.
- Create alarms that repeat every day.
- List alarms with their ID, time, type, status, and label.
- Cancel an alarm without deleting its stored record.
- Delete an alarm permanently.
- Run a scheduler that checks for due alarms every second.
- Use a custom JSON path for isolated projects or demos.
- Test time-dependent behavior with an injected clock.

## Requirements

- Python 3.10 or newer
- `pytest` for development and tests

No database, web server, or third-party runtime dependency is required.

## Quick Start

Run these commands from the repository root.

```powershell
python -m alarm_clock --help
python -m alarm_clock set 16:00 --label "Test alarm"
python -m alarm_clock list
python -m alarm_clock run
```

To create a daily alarm:

```powershell
python -m alarm_clock set 08:00 --label "Morning" --daily
```

For a quick scheduler demo, create an alarm one or two minutes ahead of the current local time and then run the clock. Press `Ctrl+C` to stop the scheduler.

## Command Reference

### Create an alarm

```powershell
python -m alarm_clock set HH:MM [--label LABEL] [--daily]
```

`HH:MM` must use 24-hour time, such as `07:30` or `18:45`. Labels default to `Alarm`.

### List alarms

```powershell
python -m alarm_clock list
```

### Cancel an alarm

Cancellation disables the alarm but keeps it in the JSON file.

```powershell
python -m alarm_clock cancel <alarm-id>
```

### Delete an alarm

Deletion removes the alarm from storage.

```powershell
python -m alarm_clock delete <alarm-id>
```

### Run the scheduler

```powershell
python -m alarm_clock run
```

The scheduler runs in the foreground and checks once per second. One-time alarms are disabled after firing; daily alarms remain enabled.

## Data Storage

By default, alarms are saved to:

```text
~/.alarm_clock/alarms.json
```

Use `--data` to select another JSON file. Put the global option before the subcommand:

```powershell
python -m alarm_clock --data .\alarms.json set 16:00 --label "Demo"
python -m alarm_clock --data .\alarms.json list
```

The storage layer writes JSON atomically through a temporary file and validates alarms when loading them.

## Development Setup

Create and activate a virtual environment if desired, then install the development dependency:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the test suite:

```powershell
python -m pytest -q
```

## Architecture

```text
CLI (argparse and terminal I/O)
              |
              v
       AlarmService
          /      \
         v        v
    Scheduler   JSON Storage
         |
         v
      Alarm model
```

- `cli.py` parses arguments, prints output, and runs the foreground loop.
- `services.py` coordinates alarm creation and state changes.
- `scheduler.py` contains time-based behavior and accepts an injectable clock.
- `storage.py` owns JSON persistence.
- `models.py` defines and validates the `Alarm` dataclass.

## Scope and Future Improvements

This is a local, foreground CLI rather than an operating-system alarm service. It intentionally does not include time zones, custom recurrence rules, authentication, multi-user support, or a database.

Potential next steps include OS-level background notifications, configurable snooze actions, richer recurrence rules, and timezone-aware scheduling.

## License

No license has been selected for this project yet.
