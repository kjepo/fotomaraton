# BUGS.md

## 1. Wrong widget updated on theme copy success (line 97–98)

```python
copy_theme[i]["fg"] = "green"
copy_user[i].config(text=f"{jpeg} ⇒ {theme_destinations[i]} ✔")  # wrong widget!
```

When a theme-folder copy succeeds, the success text is written to the *user* row (`copy_user[i]`) instead of the theme row (`copy_theme[i]`). The theme row turns green but keeps its original label; the user row gets the wrong text.

**Fix:** change `copy_user[i].config(...)` to `copy_theme[i].config(...)` on line 98.

---

## 2. `default_dir` gets clobbered inside the rglob loop (lines 161–162)

```python
for path in Path(default_dir).rglob("*.[jpeg jpg JPEG JPG]*"):
    default_dir = str(path.parent)   # overwritten each iteration
    jpegs.append(path.name)
```

`default_dir` ends up as the parent folder of the *last* JPEG processed. In `ingest()`, all source paths are built as `default_dir + "/" + jpeg`. If the memory card has JPEGs in more than one subdirectory, every file not in that last directory will have a wrong source path and fail to copy.

**Fix:** store the full path in `jpegs` instead of just the filename, and drop the `default_dir` reassignment inside the loop.

---

## 3. rglob pattern `*.[jpeg jpg JPEG JPG]*` is a character class, not an extension list (line 160)

`[jpeg jpg JPEG JPG]` means "match one character from the set j, p, e, g, space, J, P, E, G". It happens to work for `.jpg`/`.jpeg` (because `j`/`J` is in the set), but it also matches `.png`, `.psd`, `.gif`, `.eps`, etc.

**Fix:**
```python
for path in Path(default_dir).rglob("*"):
    if path.suffix.lower() in (".jpg", ".jpeg"):
```

---

## 4. `ingest()` crashes if Import is clicked before Browse (lines 87, 104)

`jpegs` does not exist as a name until `browse()` runs. Clicking Import first raises `NameError: name 'jpegs' is not defined`.

**Fix:** add a guard at the top of `ingest()`:
```python
def ingest():
    if 'jpegs' not in globals() or not jpegs:
        return
```

---

## 5. `from tkinter import *` imported twice (lines 37–38)

Harmless duplicate import. Remove one of them.
