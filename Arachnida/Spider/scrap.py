#!/usr/bin/env python3

import sys
import os
import requests
import shutil
import imghdr
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class scrap():
    """\
------------------------------------------------------------------------------
    SCRAP:
        class used to scrap image from any website.

    Attributes:
        ext (list[str]): Allowed img extensions.
        url (str): url website to scrap
        response (http request): http request response from the website

    Methods:
        exemple(): def.
------------------------------------------------------------------------------\
    """
    ext: list[str] = [".jpeg", ".jpg", ".png", ".bmp", ".gif"]
    path: str
    url: str
    url_rec: str
    rec: int
    response: any
    links: list[str]

    def __init__(self, rec=2, path='./data/') -> None:
        self.rec = rec
        self.path = path
        self.links = []
        argc = len(sys.argv)
        if argc < 2:
            raise ValueError("Wrong number of arguments")
        if not isinstance(sys.argv[argc - 1], str):
            raise ValueError("Last argument should be a string URL")
        self.url = sys.argv[argc - 1]
        self.response = requests.get(self.url)
        if not self.response:
            raise ValueError("Invalid URL type")
        # If -p option, ask which path to create file !!!!!!!
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    def get_img(self, link) -> None:
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        img_tag = soup.find_all('img')
        img_list = []
        for i in img_tag:
            img_url = i.get('src')
            if img_url:
                img_url = urljoin(self.url, img_url)
                img_name = os.path.basename(img_url)
                if img_name.endswith(tuple(self.ext)):
                    img_list.append(img_name)
        for i in img_list:
            with open(os.path.join(self.path, i), 'wb') as img_file:
                img_file.write(requests.get(img_url).content)

    def get_url(self, link_url, lvl) -> None:
        if lvl < 1:
            return
        response = requests.get(link_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            link_url = link.get('href')
            if link_url not in self.links:
                if link_url is not None and link_url.startswith('http'):
                    self.links.append(link_url)
                    self.get_url(link_url, lvl - 1)

    def get_all_url(self) -> None:
        self.get_url(self.url, self.rec)
        self.printlinks()

    def printlinks(self) -> None:
        for link in self.links:
            print(link)

    def print_res(self) -> None:
        print(self.response)
