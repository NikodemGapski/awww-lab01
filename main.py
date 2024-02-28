import requests
from bs4 import BeautifulSoup


def first_word(word):
    return word.split(' ')[0]


def md_list(contents):
    s = ''
    for el in contents:
        s += '## ' + el[0] + '\n' + el[1] + '\n'
    return s[0:-1]


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
    print(md_list(cities_list(soup)))
