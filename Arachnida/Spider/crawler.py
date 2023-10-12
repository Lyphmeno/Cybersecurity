#!/usr/bin/env python3

import multiprocessing
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
        url : string url of the website to scrap
------------------------------------------------------------------------------\
    """
    def __init__(self) -> None:
        self.ext = [".jpeg", ".jpg", ".png", ".bmp", ".gif"]
        self.links = []
        self.domain: str

    def parser(self):
        parser = argparse.ArgumentParser(usage="\n"+Crawl.__doc__, add_help=False)
        parser.add_argument('url')
        parser.add_argument('-r', '--recursive', action='store_true')
        parser.add_argument('-l', '--level', default=5, type=int)
        parser.add_argument('-p', '--path', default='./data/')
        return parser.parse_args()

    def check(self):
        self.args = self.parser()
        if not self.args.url.endswith("/"):
            self.args.url += "/"
        response = requests.get(self.args.url)
        if not response.ok:
            raise ValueError("Invalid URL")
        self.domain = urlparse(self.args.url).hostname
        if os.path.exists(self.args.path):
            shutil.rmtree(self.args.path)
        os.makedirs(self.args.path)
        print("URL:\t\t\t", self.args.url)
        print("Recursion:\t\t", self.args.recursive)
        print("Level of recursion:\t", self.args.level)
        print("Path:\t\t\t", self.args.path)

    def get_urls(self, url, level):
        if level < 1:
            return
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and not href.startswith('#'):
                    true_link = urljoin(url, href)
                    if self.domain == urlparse(true_link).hostname\
                            and true_link not in self.links:
                        self.links.append(true_link)
                        self.get_urls(true_link, level-1)
        except requests.exceptions.RequestException as e:
            print(f"Error while processing {url}: {e}")
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")

    def execute(self):
        try:
            self.check()
            if self.args.recursive:
                self.get_urls(self.args.url, self.args.level)
            else:
                self.links.append(self.args.url)
            print("\n".join(self.links), "\n", len(self.links), "links")
        except ValueError as ve:
            print(ve)
        except requests.exceptions.RequestException as re:
            print("Request Error:", re)
        except Exception as e:
            print("An error occurred:", e)


