# Repository Instructions

## Project

- This is a Python 3.10+ command-line alarm clock.
- Keep the existing layers focused: `cli.py` handles argparse and terminal I/O; `services.py` coordinates use cases; `scheduler.py` contains time-based behavior; `storage.py` owns JSON persistence; `models.py` contains the `Alarm` domain model.
- Do not introduce a database or web UI unless the task explicitly changes the project scope.

## Development

- Use the standard library for runtime code unless an existing dependency or the task clearly justifies another package.
- Keep scheduling logic independent from terminal I/O.
- Inject a clock into time-dependent code so tests remain deterministic; avoid sleeping or relying on wall-clock time in unit tests.
- Preserve the JSON storage format and validate alarms at the model boundary.
- Follow the existing type-hinting and dataclass style. Keep edits focused and avoid unrelated refactors.

## Validation

- Install dependencies with `python -m pip install -r requirements.txt` when needed.
- Run the test suite from the repository root with `python -m pytest -q`.
- For CLI behavior, invoke the module with `python -m alarm_clock` and use `--data` with a temporary or isolated JSON path.
- Add or update focused tests for behavior changes, especially scheduler and persistence changes.
