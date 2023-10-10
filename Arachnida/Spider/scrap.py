#!/usr/bin/env python3

import sys
import os
import requests
import shutil
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures

class Scrap:
    ext = [".jpeg", ".jpg", ".png", ".bmp", ".gif"]

    def __init__(self, rec=2, path='./data/'):
        self.rec = rec
        self.path = path
        self.links = []
        argc = len(sys.argv)
        if argc < 2:
            raise ValueError("Wrong number of arguments")
        if not isinstance(sys.argv[argc - 1], str):
            raise ValueError("Last argument should be a string URL")
        self.url = sys.argv[argc - 1]
        self.url_rec = self.url
        self.response = requests.get(self.url)
        if not self.response.ok:
            raise ValueError("Invalid URL or failed to retrieve content")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    def get_img(self, link):
        try:
            soup = BeautifulSoup(requests.get(link).text, 'html.parser')
            img_tag = soup.find_all('img')
            img_list = []
            for i in img_tag:
                img_url = i.get('src')
                if img_url:
                    img_url = urljoin(self.url, img_url)
                    img_name = os.path.basename(img_url)
                    if img_name.endswith(tuple(self.ext)):
                        img_list.append(img_url)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.download_image, img_list)
        except Exception as e:
            print(f"An error occurred while downloading images: {e}")

    def download_image(self, img_url):
        try:
            response = requests.get(img_url)
            if response.ok:
                img_name = os.path.basename(img_url)
                with open(os.path.join(self.path, img_name), 'wb') as img_file:
                    img_file.write(response.content)
            else:
                print(f"Failed to download image: {img_url}")
        except Exception as e:
            print(f"An error occurred while downloading an image: {e}")

    def get_url(self, link_url, lvl):
        if lvl < 1:
            return
        try:
            response = requests.get(link_url)
            if not response.ok:
                return
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                link_url = link.get('href')
                if link_url and link_url not in self.links:
                    img_url_parsed = urllib.parse.urlparse(link_url)
                    original_url_parsed = urllib.parse.urlparse(self.url)
                    if img_url_parsed.hostname == original_url_parsed.hostname:
                        self.links.append(link_url)
                        self.get_url(link_url, lvl - 1)
        except Exception as e:
            print(f"An error occurred while fetching URLs: {e}")

    def get_all_url(self):
        self.get_url(self.url, self.rec)
        self.printlinks()
        for link in self.links:
            self.get_img(link)

    def printlinks(self):
        for link in self.links:
            print(link)

    def print_res(self):
        print(self.response)

if __name__ == "__main__":
    try:
        scraper = Scrap()
        scraper.get_all_url()
        scraper.get_img(scraper.url_rec)
    except Exception as e:
        print(f"An error occurred: {e}")
