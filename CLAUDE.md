# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`maraton.py` is a single-file Python/Tkinter desktop app for importing JPEG photos at a Swedish Photo Marathon competition. Competitors submit a memory card with 4 or 8 JPEGs; the app copies each image to two destinations under a chosen target folder.

## Running and building

```bash
# Run directly
python3 maraton.py

# Build standalone macOS app
pyinstaller --windowed --onefile maraton.py
```

No dependencies beyond the Python standard library (`tkinter`, `pathlib`, `shutil`, `re`, `os`).

## Architecture

The entire program is a single file with no classes — global variables hold both UI widgets and application state.

**User workflow:**
1. **Setup** — pick the target folder; the app scans it for subdirectories matching `^tema` (case-insensitive) and stores them in `target_subdirs`
2. **Enter competitor number** (e.g. `42` → canonicalized to `042`); pressing Enter or clicking Browse creates `<target_dir>/Nr 042/` if it doesn't exist
3. **Browse** — pick the competitor's memory card directory; `rglob("*.[jpeg jpg JPEG JPG]*")` finds all JPEGs recursively (note: this is a character-class glob, not extension matching)
4. **Import** (`ingest()`) — copies each JPEG to two destinations, coloring labels green on success or red on failure

**Copy destinations per JPEG (index `i`, competitor `NNN`, theme `target_subdirs[i]`):**
- Theme copy: `<target_dir>/<TemaFolder>/Nr NNN - <TemaFolder>.jpg`
- Competitor copy: `<target_dir>/Nr NNN/Nr NNN - <TemaFolder>.jpg`

The UI widgets for the file list (`copy_theme`, `copy_user`) are destroyed and rebuilt on every Browse call. Checkboxes are pre-checked unless the destination file already exists.

## Known bugs

Five bugs are documented in `BUGS.md`. The most impactful:

- **Wrong widget on success** (`ingest()` line 97–98): success text is written to `copy_user[i]` instead of `copy_theme[i]` when a theme copy succeeds.
- **`default_dir` clobbered in rglob loop** (line 161–162): ends up as the parent of the last JPEG found; source paths break when JPEGs span multiple subdirectories.
- **`jpegs` undefined crash**: clicking Import before Browse raises `NameError`.

## Test fixtures

`test/` holds sample data for manual testing:
- `test/DCIM/` — four sample JPEGs (`0001.jpg`–`0004.jpg`)
- `test/Tema/` — eight `Tema Nr N - NAME/` subdirectories matching the `^tema` pattern
