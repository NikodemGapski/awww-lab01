import requests
from bs4 import BeautifulSoup

md_dir = 'docs/'
img_dir = md_dir + 'resources/'
img_dir_in_docs = 'resources/'


def create_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')
