import requests
from bs4 import BeautifulSoup
from image_scraper import scrape_image
import os

md_dir = './docs/'
img_dir = md_dir + 'resources/'
img_dir_in_docs = './resources/'

def get_view_images(cities):
    for el in cities:
        [name, population] = el
        query = name + ' tourist view'
        filename = img_dir + name + '_view.jpg'
        scrape_image(query, filename)


def md_listed_content(contents):
    s = ''
    for el in contents:
        [name, population] = el
        # Name
        s += '## ' + name + '\n'
        # Population
        s += population + '\n'
        # Image
        query = name + ' tourist view'
        filename = img_dir_in_docs + name + '_view.jpg'
        s += '\n![' + query + '](' + filename + ')' + '\n'

    return s


def md_create_file(contents, filename):
    with open(md_dir + filename, 'w') as f:
        f.write(contents)

def cities_list(_soup):
    list_raw = _soup.find_all('ol')[-1]
    contents = [li.get_text().split(' ') for li in list_raw.find_all('li')]
    for pos in contents:
        pos[1] = '**Population:** ' + pos[1].strip('()')
    return contents


def create_soup():
    r = requests.get('https://www.worldatlas.com/maps/peru')
    return BeautifulSoup(r.text, 'html.parser')


if __name__ == '__main__':
    print('Hello there')
    soup = create_soup()
    # Scrape list and create md content
    cities = cities_list(soup)
    content = md_listed_content(cities)
    # Create md file
    md_create_file(content, 'city_list.md')
    # Scrape images
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        get_view_images(cities)
    print('Done.')