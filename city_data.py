import re
import utils
from image_scraper import scrape_image

class City:
    def __init__(self, name):
        self.name = name
        self.note = ''

# --- IMAGES ---
def download_view_image(city):
    query = city.name + ' tourist view'
    filename = utils.img_dir + city.name + '_view.jpg'
    scrape_image(query, filename)

def download_landscape_images(city):
    query = city.name + ' landscape'
    filenames = [utils.img_dir + city.name + '_landscape_' + i + '.jpg' for i in range(4)]
    # scrape_images(query, filenames)

def download_images(cities):
    for c in cities:
        download_view_image(c)

# --- NOTES ---
def remove_brackets(string, char):
    pattern = '\\' + char[0] + '[^' + char[1] + ']*' + '\\' + char[1]
    return re.sub(pattern, '', string)

def city_add_note(c, url):
    soup = utils.create_soup(url)
    text = soup.find('div', 'mw-content-ltr mw-parser-output')
    intro = text.find(lambda tag: tag.name == 'p' and tag.text.strip() and 'city' in tag.text)
    if intro:
        txt = remove_brackets(intro.get_text(), '()')
        txt = remove_brackets(txt, '[]')
        c.note = txt
    else:
        url = 'https://en.wikipedia.org/wiki/' + c.name + ',_Peru'
        print('Wikipedia page not found. Now searching for: ' + url)
        city_add_note(c, url)

def cities_add_note(cities):
    for c in cities:
        city_add_note(c, 'https://en.wikipedia.org/wiki/' + c.name)

def cities_list(_soup):
    list_raw = _soup.find_all('ol')[-1]
    contents = [li.get_text().split(' ')[0] for li in list_raw.find_all('li')]
    res = [City(pos) for pos in contents]
    cities_add_note(res)
    return res