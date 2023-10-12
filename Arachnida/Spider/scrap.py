#!/usr/bin/env python3

import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import concurrent.futures


class Scrop:
    ext = [".jpeg", ".jpg", ".png", ".bmp", ".gif"]

    def __init__(self, rec=5, path='./data/'):
        self.rec = rec
        self.path = path
        self.links = []
        argc = len(sys.argv)
        if argc < 2:
            raise ValueError("Wrong number of arguments")
        self.url = sys.argv[argc - 1]
        self.response = requests.get(self.url)
        if not self.response.ok:
            raise ValueError("Invalid URL or failed to retrieve content")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    def parser():
        parser.add_argument('url', help="url to scrap")
        parser.add_argument('-r', '--recursive', help="recursively downloads the images in a URL received as a parameter", action='store_true')
        parser.add_argument('-l', '--level', help='indicates the maximum depth level of the recursive download.', default=5, type=int)
        parser.add_argument('-p', '--path', help=' indicates the path where the downloaded files will be saved.', default='./data/')
        arg = parser.parse_args()
        return arg

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

    def is_same_domain(self, url1, url2):
        return urlparse(url1).hostname == urlparse(url2).hostname

    def get_url(self, url, lvl):
        print(f"---Trying to enter in {url, lvl}---")
        if lvl > self.rec and url not in self.links:
            return
        print(f"\t\t\t\t---lvl {lvl} of rec---")
        try:
            response = requests.get(url)
            if not response.ok:
                return
            soup = BeautifulSoup(response.text, 'html.parser')
            for i, link in enumerate(soup.find_all('a'), start=0):
                link_url = link.get('href')
                if link_url:
                    full_link = urljoin(url, link_url)
                    if self.is_same_domain(full_link, self.url) and full_link not in self.links:
                        print("\t\t", i, "+ ", full_link)
                        self.get_url(full_link, lvl + 1)
                        self.links.append(full_link)
        except Exception as e:
            print(f"An error occurred while fetching URLs: {e}")

    def get_all_url(self):
        if self.rec == 0:
            self.get_img(self.url)
            self.printlinks()
        else:
            self.get_url(self.url, 0)
            self.printlinks()
            for link in self.links:
                self.get_img(link)

    def printlinks(self):
        for link in self.links:
            print(link)
        print(f"{len(self.links)} links !")

    def print_res(self):
        print(self.response)
