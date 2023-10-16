#!/usr/bin/env python3.10

import sys


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
        except ValueError as ve:
            print(f"{ve}")

    def check_error(self):
        self.argc = len(sys.argv)
        if self.argc <= 1:
            raise ValueError("Not enough arguments")
        for filename in sys.argv:
            if filename.endswith(tuple(self.ext)):
                self.files.append(filename)
        print("\n".join(self.files))
