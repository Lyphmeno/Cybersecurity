#!/usr/bin/env python3

import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import concurrent.futures
import argparse


class Crawl:
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
    def __init__(self) -> None:
        self.ext = [".jpeg", ".jpg", ".png", ".bmp", ".gif"]
        self.links = []

    def parser(self):
        parser = argparse.ArgumentParser(usage="\n"+Crawl.__doc__, add_help=False)
        parser.add_argument('url')
        if parser.add_argument('-r', '--recursive', action='store_true'):
            parser.add_argument('-l', '--level', default=5, type=int)
        parser.add_argument('-p', '--path', default='./data/')
        args = parser.parse_args()
        print("URL:\t\t\t", args.url)
        print("Recursion:\t\t", args.recursive)
        print("Level of recursion:\t", args.level)
        print("Path:\t\t\t", args.path)
        return args

    def execute(self):
        args = self.parser()
        

