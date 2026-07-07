# Timer App

A simple countdown timer, implemented twice:

- `timer_app.py` — desktop GUI using Tkinter (Python standard library, no dependencies)
- `timer.html` — browser version (vanilla HTML/CSS/JS, no build step)

Both share the same dark theme, ring progress indicator, and Japanese-language UI (分/秒 for minutes/seconds).

## Running

- Desktop: `python3 timer_app.py`
- Browser: open `timer.html` directly, no server needed

## Conventions

- No build tooling or package manager — keep both versions dependency-free.
- Keep the Python and HTML versions' behavior in sync when changing timer logic (start/pause/reset, ring rendering, color thresholds).
