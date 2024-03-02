import requests
import os
from duckduckgo_search import DDGS

def is_jpg_image(image_url):
    # Split the URL by "." and get the last part
    file_extension = image_url.split(".")[-1]
    # Check if the file extension is "jpg" or "jpeg"
    return file_extension.lower() in ["jpg", "jpeg"]

def is_downloaded_jpg(filename):
    data = open(filename,'rb').read(11)
    if str(data[:3]) != 'b\'\\xff\\xd8\\xff\'': return False
    if str(data[6:]) != 'b\'JFIF\\x00\'': return False
    return True


def get_image_urls(query, count):
    count *= 2
    try:
        ddg = DDGS()
        results = []
        while count > 0:
            new_res = ddg.images(query, max_results=count * 2)
            for r in new_res:
                if (not r) or (r['image'] in results) or (not is_jpg_image(r['image'])):
                    continue

                results += [r['image']]
                count -= 1
                if count == 0:
                    return results
            print('A batch for query "' + query + '" didn\'t contain enough matching photos. Trying again.')
    except Exception as e:
        print('Error on fetching images:', e)
    print('Didn\'t find urls for query: "' + query + '". Exiting.')
    return []

# Function to download the image from a given URL
def download_image(url, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print("Error occurred while downloading image:", e)

# Download the first image for the given query to the file named filename.
def scrape_image(query, filename):
    image_url = get_image_urls(query, 1)
    if image_url[0]:
        download_image(image_url[0], filename=filename)
    else:
        print("No images found for the query:", query)

def scrape_images(query, filenames):
    urls = get_image_urls(query, len(filenames))
    u = 0
    for filename in filenames:
        while True:
            download_image(urls[u], filename=filename)
            u += 1
            if not is_downloaded_jpg(filename):
                os.remove(filename)
            else:
                break
