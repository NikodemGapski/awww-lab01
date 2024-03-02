import re
import utils
from image_scraper import scrape_image
from image_scraper import scrape_images

class City:
    def __init__(self, name):
        self.name = name
        self.note = ''
        self.landscape_files = []
        self.day_trip_url = ''

# --- IMAGES ---
def download_view_image(city):
    query = city.name + ' tourist view'
    filename = utils.img_dir + city.name + '_view.jpg'
    scrape_image(query, filename)

def download_landscape_images(city):
    query = city.name + ' landscape'
    scrape_images(query, [utils.md_dir + f for f in city.landscape_files])

def download_images(cities):
    for c in cities:
        download_view_image(c)
        download_landscape_images(c)

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

def cities_add_info(cities):
    for c in cities:
        city_add_note(c, 'https://en.wikipedia.org/wiki/' + c.name)
        c.day_trip_url = utils.get_link('day trips ' + c.name)
        c.landscape_files = [utils.img_dir_in_docs + c.name + '_landscape_' + str(i) + '.jpg' for i in range(4)]

def cities_list(_soup):
    list_raw = _soup.find_all('ol')[-1]
    contents = [li.get_text().split(' ')[0] for li in list_raw.find_all('li')]
    res = [City(pos) for pos in contents]
    cities_add_info(res)
    return res

def md_city(c):
    s = '[[Back to the list]](city_list.md)\n'
    # Name
    s += '# ' + c.name + '\n'
    # Note
    s += '**Overview:** ' + c.note + '\n'
    # Image
    query = c.name + ' tourist view'
    filename = utils.img_dir_in_docs + c.name + '_view.jpg'
    s += '\n![' + query + '](' + filename + ')' + '\n'
    # Day trips and landscape
    s += '## Trips and landscape\n'
    s += '**Day trips:** take a look at the best day trips from the city [here](' + c.day_trip_url + ').\n'
    files = []
    for file in c.landscape_files:
        files += ['![landscape image](' + file + ')']
    s += '\n|  |  |\n'
    s += '| --- | --- |\n'
    s += '| ' + files[0] + ' | ' + files[1] + ' |\n'
    s += '| ' + files[2] + ' | ' + files[3] + ' |\n'

    return s