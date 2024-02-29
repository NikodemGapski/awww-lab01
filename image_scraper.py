import requests
from duckduckgo_search import DDGS

def is_jpg_image(image_url):
    # Split the URL by "." and get the last part
    file_extension = image_url.split(".")[-1]
    # Check if the file extension is "jpg" or "jpeg"
    return file_extension.lower() in ["jpg", "jpeg"]

# Function to get the URL of the first image from DuckDuckGo search
def get_first_image_url(query):
    try:
        ddg = DDGS()
        while True:
            results = ddg.images(query)
            first_result = next(results, None)
            if first_result and is_jpg_image(first_result['image']):
                return first_result['image']
            else:
                print('.jpg image not found for query: "' + query + '". Looking again.')
    except Exception as e:
        print("Error occurred while fetching images:", e)
    return None

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
    image_url = get_first_image_url(query)
    if image_url:
        download_image(image_url, filename=filename)
    else:
        print("No images found for the query:", query)
