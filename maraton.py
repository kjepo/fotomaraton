# maraton.py
#
# This program handles the importing of files for a Photo Marathon where
# competitors submits a memory card containing 4 or 8 JPEG images.
#
# First click "Setup" to locate the folder containing the "Tema" sub folders
# Normally there are 8 Tema-folders and they have to contain the word "Tema".
#
# Once you're setup you can start processing competitors:
# Enter their starting number, e.g., 42.  The program will expand to three digits
# when you hit Enter or click Browse.
# When you click Browse, you can navigate to the competitor's memory card.
# The program will recursively list all JPEG files so you don't have to
# find the specific subfolder where they are.
#
# When the program has been presented with the JPEG images it will list
# what it is about to copy.  If the file names have already been copied
# the respective checkbox won't be checked.  (Notice that the program
# does not detect if the files are identical, only that the file is already
# there.)
#
# Click "Import" to start the copy.  If all goes well, the names should turn
# green.  If for some reason it doesn't work (write protection?) and the file
# can't be copied, it will turn red.
#
# Then you can enter another competitor's number, click "Browse" etc.
#
# This program is (C) Kjell Post kjell@irstafoto.se
# Use it, abuse it, but don't pretend you wrote it.
#
# pyinstaller --windowed --onefile maraton4.py
#
# rglob doesn't return full path to JPEGs


from tkinter import *
import os, re, shutil
from tkinter import filedialog as fd
from tkinter import simpledialog
from tkinter import messagebox
from pathlib import Path

root = Tk()
root.title("Marathon")
root.geometry("700x700")  # set starting size of window
root.maxsize(700, 700)  # width x height
root.config() # bg="lightgrey")

target_dir = os.path.expanduser('~')
target_subdirs = []
default_dir = "/Volumes/"
copy_theme = {}
copy_theme_states = {}
theme_destinations = {}
copy_user = {}
copy_user_states = {}
user_destinations = {}

def getStartNumber(start):
    snr = start.get()
    if not snr:
        return snr
    snr = int(snr)
    snr = f"{snr:03d}"
    return snr

def setup():
    global target_dir, target_subdirs, label_info
    target_dir = fd.askdirectory(initialdir=target_dir)
    target_subdirs = []
    p = Path(target_dir)
    for f in p.iterdir():
        if f.is_dir():
            if re.match(r"tema", f.name, re.IGNORECASE):
                target_subdirs.append(f.name)
    target_subdirs.sort()
    label_info.config(text="\n".join(target_subdirs))

def ingest():
    global default_dir, start
    global copy_theme, copy_theme_states, theme_destinations
    global copy_user, copy_user_states, user_destinations
    if 'jpegs' not in globals() or not jpegs:
        return
    snr = getStartNumber(start)
    i = 0
    copy_errors = False
    for jpeg in jpegs:
        if copy_theme_states[i].get():
            source = str(jpeg)
            dest = target_dir + "/" + theme_destinations[i]
            if Path(dest).is_file():
                print(f"file {dest} already exists")
            else:
                try:
                    shutil.copy(source, dest)
                    copy_theme[i]["fg"] = "green"
                    copy_theme[i].config(text=f"{jpeg.name} ⇒ {theme_destinations[i]} ✔")
                except EnvironmentError:
                    copy_errors = True
                    copy_theme[i]["fg"] = "red"                    
        i = i + 1                

    i = 0
    for jpeg in jpegs:
        if copy_user_states[i].get():
            source = str(jpeg)
            dest = target_dir + "/" + user_destinations[i]
            if Path(dest).is_file():
                print(f"file {dest} already exists")
            else:
                try:
                    shutil.copy(source, dest)
                    copy_user[i]["fg"] = "green"
                    copy_user[i].config(text=f"{jpeg.name} ⇒ {user_destinations[i]} ✔")
                except EnvironmentError:
                    copy_user[i]["fg"] = "red"
                    copy_errors = True
        i = i + 1

    if copy_errors:
        messagebox.showerror('Error', 'Some files could not be copied')


# make start number canonical (three digits, for example "042")
# create directory "Nr 042" if it doesn't exist
def setuser():
    global startinfo, start, root, target_dir
    snr = getStartNumber(start)
    if not snr:
        return snr
    start.delete(0, END)
    start.insert(0, snr)
    # Create directory "Nr 042" (for example)
    if target_subdirs:
        path = target_dir + "/Nr " + snr
        # print(f"checking path={path}")
        if not os.path.exists(path):
            os.makedirs(path)
            startinfo.config(text=f"Created Nr {snr}")
        else:
            startinfo.config(text=f"Nr {snr} exists")
    else:
        startinfo.config(text="Please \"Setup\" first")
    root.update()
    return snr

def on_enter(event):
    setuser()

def browse():
    global jpegs, button_import, default_dir, root, copy_theme, copy_user, copy_theme_states, copy_user_states
    global theme_destinations, user_destinations, warning_label
    snr = setuser()
    if not snr:
        startinfo.config(text="Enter competitor number first")
        return
    default_dir = fd.askdirectory(initialdir = default_dir)
    if not default_dir:
        return
    jpegs = []
    for path in Path(default_dir).rglob("*"):
        if path.suffix.lower() in (".jpg", ".jpeg"):
            jpegs.append(path)
    jpegs.sort()
    print("default_dir")
    print(default_dir)

    for i in copy_theme:
        copy_theme[i].destroy()
    for i in copy_user:
        copy_user[i].destroy()
    copy_theme = {}
    copy_user = {}

    if len(target_subdirs) > 0:
        # Prefer mapping to unfilled tema slots so a second batch of 4 images lands
        # in the next 4 empty slots rather than re-mapping to the already-filled first 4.
        # Fall back to all slots when there aren't enough empty ones (e.g. re-browsing
        # after a complete import), in which case destinations are shown pre-unchecked.
        available_subdirs = [
            subdir for subdir in target_subdirs
            if not Path(f"{target_dir}/{subdir}/Nr {snr} - {subdir}.jpg").is_file()
        ]
        subdirs_to_use = available_subdirs if len(available_subdirs) >= len(jpegs) else target_subdirs

        i = 0
        for jpg in jpegs:
            if i >= len(subdirs_to_use):
                break
            subdir = subdirs_to_use[i]

            copy_theme_states[i] = IntVar()
            theme_destinations[i] = f"{subdir}/Nr {snr} - {subdir}.jpg"
            copy_theme[i] = Checkbutton(root, text=f"{jpg.name} ⇒ {theme_destinations[i]}", variable=copy_theme_states[i])
            copy_theme[i].grid(row=2+2*i, column=1, padx=5, pady=0, columnspan=2, sticky=W)

            theme_exists = Path(target_dir + "/" + theme_destinations[i]).is_file()
            theme_label = f"{jpg.name} ⇒ {theme_destinations[i]}" + (" (exists)" if theme_exists else "")
            copy_theme[i].config(text=theme_label)
            if not theme_exists:
                copy_theme[i].select()
            else:
                copy_theme[i].deselect()

            copy_user_states[i] = IntVar()
            user_destinations[i] = f"Nr {snr}/Nr {snr} - {subdir}.jpg"
            user_exists = Path(target_dir + "/" + user_destinations[i]).is_file()
            user_label = f"{jpg.name} ⇒ {user_destinations[i]}" + (" (exists)" if user_exists else "")
            copy_user[i] = Checkbutton(root, text=user_label, variable=copy_user_states[i])
            copy_user[i].grid(row=3+2*i, column=1, padx=5, pady=0, columnspan=2, sticky=W)

            if not user_exists:
                copy_user[i].select()
            else:
                copy_user[i].deselect()

            i = i + 1

        existing_count = sum(
            1 for dest in theme_destinations.values()
            if Path(target_dir + "/" + dest).is_file()
        )
        if existing_count:
            warning_label.config(text=f"Warning: {existing_count} file(s) already exist and will not be overwritten")
        else:
            warning_label.config(text="")

        startinfo.config(text="")
        #start.delete(0, 'end')
        #start.focus_force()

def quit():
    exit(0)

Button(root, text='Setup',  height=2, width=5, command=setup).grid(row=0, column=0, padx=5, pady=5)
Button(root, text='Browse', height=2, width=5, command=browse).grid(row=2, column=0, rowspan=3, padx=5, pady=5)
# Button(root, text='Quit', height=2, width=5, command=quit).grid(row=20, column=0, padx=5, pady=5)
Label(root, text="Competitor #").grid(row=1, column=0, padx=5, pady=5)
Label(root, text="© Kjell Post, kjell@irstafoto.se", anchor="w", font= ('Aerial', 8)).grid(row=21, column=0, columnspan=3, padx=5, pady=5)
start = Entry(root)
start.bind('<Return>', on_enter)
startinfo = Label(root)
startinfo.grid(row=1, column=2, padx=5, pady=5, sticky="W")
start.grid(row=1, column=1, padx=5, pady=5, sticky="W")
Button(root, text='Import', height=2, width=5, command=ingest).grid(row=8, column=0, rowspan=3, padx=5, pady=5)
label_info = Label(root, width=60, height=10, wraplength=520, justify=LEFT, anchor="nw", bg="#DDDDDD")
label_info.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
warning_label = Label(root, text="", fg="orange", anchor="w")
warning_label.grid(row=20, column=1, columnspan=2, padx=5, pady=2, sticky=W)

root.mainloop()
