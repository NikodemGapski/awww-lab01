import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

md_dir = 'docs/'
img_dir = md_dir + 'resources/'
img_dir_in_docs = 'resources/'


def create_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')

def get_link(query):
    ddg = DDGS()
    res = [r for r in ddg.text(query)]
    return res[0]['href']