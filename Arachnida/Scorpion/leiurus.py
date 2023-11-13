#!/usr/bin/env python3.10

import sys
import tkinter as tk
import imghdr
import os
from gui import ImageViewer
from PIL import Image, ImageTk


class Leiurus:
    """\
------------------------------------------------------------------------------
    Leiurus:
        Image scraping class to retrieve metadata/EXIF.
        The program will accept the following extensions by default:
            • .jpg/jpeg
            • .png
            • .gif
            • .bmp

    Arguments:
        files (str): files path.
------------------------------------------------------------------------------\
    """
    def __init__(self):
        try:
            self.ext = [".jpeg", ".jpg", ".png", ".bmp", ".gif"]
            self.files = []
            self.check_error()
            self.execute()
        except ValueError as ve:
            print(f"ERROR:\t{ve}")

    def check_error(self):
        sys.argv.pop(0)
        self.argc = len(sys.argv)
        if self.argc <= 0:
            raise ValueError("Not enough arguments")
        for filename in sys.argv:
            self.files.append(filename)
        if not len(self.files):
            raise ValueError("Not enough valid files")

    def get_data(self):
        for file in self.files:
            with open(file, 'rb') as f:
                img = f.read()
            img_type = imghdr.what(None, h=img)
            if img_type not in self.ext:
                self.files.remove(file)

    def launch_gui(self):
        display_backup = os.getenv("DISPLAY", default=None)
        os.environ["DISPLAY"] = ":0.0"
        root = tk.Tk()
        viewer = ImageViewer(root, self.files)
        root.mainloop()
        os.environ["DISPLAY"] = display_backup

    def execute(self):
        self.get_data()
        self.launch_gui()
        print("\n".join(self.files))
