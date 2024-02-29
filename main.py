import utils
import city_data
import os

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
    # Create md file
    md_create_file(content, 'city_list.md')
    # Scrape images
    if not os.path.exists(utils.img_dir):
        os.makedirs(utils.img_dir)
        city_data.download_images(cities)
    print('Done.')