#!/usr/bin/env python3.10

import sys


def main() -> None:
    """\
------------------------------------------------------------------------------
    SPIDER:
        Scraping program to extract all the images from a website.
        The program will download the following extensions by default:
            • .jpg/jpeg
            • .png
            • .gif
            • .bmp

    Options:
        -r : Recursively downloads the images in a URL received as a parameter.
        -r -l : Indicates the maximum depth level of the recursive download.
                If not indicated, it will be 5.
        -p : Indicates the path where the downloaded files will be saved.
             If not specified, ./data/ will be used.

    Arguments:
        URL : string url of the website to scrap
------------------------------------------------------------------------------\
    """
    try:
        argc = len(sys.argv)
        if argc < 2:
            raise ValueError("Not enough arguments")
        return 0
    except Exception as e:
        print(f"{e}")
        print(f"Please refer to the program manual :{main.__doc__}")
        return 1


if __name__ == "__main__":
    main()
