import utils
import city_data
import os
import image_scraper

# ----- MARKDOWN CREATION -----
def md_listed_content(contents):
    s = '[[Back to the main page]](index.md)\n'
    for el in contents:
        # Name
        s += '## ' + el.name + '\n'
        # Note
        s += '**Overview:** ' + el.note + '\n'
        # Learn more
        s += '[[Learn more]](' + el.name + '.md)\n'
        # Image
        query = el.name + ' tourist view'
        filename = utils.img_dir_in_docs + el.name + '_view.jpg'
        s += '\n![' + query + '](' + filename + ')' + '\n'

    return s

def md_create_file(contents, filename):
    with open(utils.md_dir + filename, 'w') as f:
        f.write(contents)


# ----- MAIN -----
if __name__ == '__main__':
    print('Hello there')
    soup = utils.create_soup('https://www.worldatlas.com/maps/peru')
    # Scrape list and create md content
    cities = city_data.cities_list(soup)

    content = md_listed_content(cities)
    # Create md files
    md_create_file(content, 'city_list.md')
    for city in cities:
        md_create_file(city_data.md_city(city), city.name + '.md')
    # Scrape images
    if not os.path.exists(utils.img_dir):
        os.makedirs(utils.img_dir)
        image_scraper.download_image('https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.worldatlas.com%2Fr%2Fw1200%2Fupload%2F41%2Fff%2Fc6%2Fpe-01.png&f=1&nofb=1&ipt=d847b82ba22c3a2252b794f2b49a9b7be802703e5c312ff7d7706b3580e8c599&ipo=images', 'docs/resources/map.png')
        city_data.download_images(cities)
    print('Done.')