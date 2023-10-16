#!/usr/bin/env python3.10

import sys
import imghdr
import os

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
            self.info: list[list[str]]
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

    def get_data(self, img):
        with open(img, 'rb') as f:
            img = f.read()
        img_type = imghdr.what(None, h=img)
        if img_type not in self.ext:
            return


    def execute(self):
        for img in self.files:
            self.get_data(img)
        print("\n".join(self.files))
