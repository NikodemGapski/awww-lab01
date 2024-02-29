import requests
from bs4 import BeautifulSoup
from image_scraper import scrape_image
import os

md_dir = './docs/'
img_dir = md_dir + 'resources/'
img_dir_in_docs = './resources/'

class City:
    def __init__(self, name):
        self.name = name
        self.note = ''

def create_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def get_view_images(cities):
    for el in cities:
        query = el.name + ' tourist view'
        filename = img_dir + el.name + '_view.jpg'
        scrape_image(query, filename)


def md_listed_content(contents):
    s = ''
    for el in contents:
        # Name
        s += '## ' + el.name + '\n'
        # Note
        s += '**Overview:** ' + el.note + '\n'
        # Image
        query = el.name + ' tourist view'
        filename = img_dir_in_docs + el.name + '_view.jpg'
        s += '\n![' + query + '](' + filename + ')' + '\n'

    return s


def md_create_file(contents, filename):
    with open(md_dir + filename, 'w') as f:
        f.write(contents)

def cities_list(_soup):
    list_raw = _soup.find_all('ol')[-1]
    contents = [li.get_text().split(' ')[0] for li in list_raw.find_all('li')]
    res = [City(pos) for pos in contents]
    return res

def city_add_note(c, url):
    soup = create_soup(url)
    text = soup.find('div', 'mw-content-ltr mw-parser-output')
    intro = text.find(lambda tag: tag.name == 'p' and tag.text.strip() and 'city' in tag.text)
    if intro:
        c.note = intro.get_text()
    else:
        url = 'https://en.wikipedia.org/wiki/' + c.name + ',_Peru'
        print('Wikipedia page not found. Now searching for: ' + url)
        city_add_note(c, url)

def cities_add_note(cities):
    for c in cities:
        city_add_note(c, 'https://en.wikipedia.org/wiki/' + c.name)


if __name__ == '__main__':
    print('Hello there')
    soup = create_soup('https://www.worldatlas.com/maps/peru')
    # Scrape list and create md content
    cities = cities_list(soup)
    cities_add_note(cities)

    content = md_listed_content(cities)
    # Create md file
    md_create_file(content, 'city_list.md')
    # Scrape images
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        get_view_images(cities)
    print('Done.')