# fotomaraton
This program handles the importing of files for a Swedish Photo Marathon where
competitors submits a memory card containing 4 or 8 JPEG images.

First click "Setup" to locate the folder containing the "Tema" sub folders.
Normally there are 8 Tema-folders and they have to contain the word "Tema".

Once you're setup you can start processing competitors:
Enter their starting number, e.g., 42.  The program will expand to three digits
when you hit Enter or click Browse.

When you click Browse, you can navigate to the competitor's memory card.
The program will recursively list all JPEG files so you don't have to
find the specific subfolder where they are.

When the program has been presented with the JPEG images it will list
what it is about to copy.  If the file names have already been copied
the respective checkbox won't be checked.  (Notice that the program
does not detect if the files are identical, only that the file is already
there.)

Click "Import" to start the copy.  If all goes well, the names should turn
green.  If for some reason it doesn't work (write protection?) and the file
can't be copied, it will turn red.

Then you can enter another competitor's number, click "Browse" etc.

![Screenshot](http://competition.smfotografi.se/ftp/fotomaraton.png)

This program is (C) Kjell Post kjell@irstafoto.se

Use it, abuse it, but don't pretend you wrote it.

# Standalone distributions

Mac M-processors: http://competition.smfotografi.se/ftp/maraton-silicon.zip

Mac Intel processors: http://competition.smfotografi.se/ftp/maraton-intel.zip

# Note on using pyinstaller

``
pyinstaller --windowed --onefile maraton.py
``
