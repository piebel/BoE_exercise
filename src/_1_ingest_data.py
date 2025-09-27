import requests
import logging
from bs4 import BeautifulSoup
import os
import time
import re

# logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# url to scrape
URL = "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/lms/previous"

response = requests.get(URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

# find all links that match the CSV link pattern and end with a version-like suffix (e.g., v117)
csv_links = []

# this regex matches ONS CSV download links that:
# contain 'generator?format=csv&uri=' (the CSV generator endpoint)
# end with a version suffix like '/v117' (where 117 is any number)
pattern = re.compile(r'generator\?format=csv&uri=.*?/v\d+$')

for a in soup.find_all('a', href=True): # parse through html page components to find links
    href = a['href']
    if pattern.search(href):
        # make sure the link is absolute
        if href.startswith('http'):
            csv_links.append(href)
        else:
            csv_links.append('https://www.ons.gov.uk' + href)
    if len(csv_links) >= 25:
        break

# download the first 25 csvs 
dest_folder = "input_data"
os.makedirs(dest_folder, exist_ok=True)

def extract_release_date(csv_content):
    """Extract the release date from the CSV content.

    Args:
        csv_content (bytes): The content of the CSV file.

    Returns:
        str: The release date extracted from the CSV content, or None if not found.
    """
    # look for the release date in the first few lines of the CSV content
    lines = csv_content.decode(errors='ignore').splitlines()
    import re
    for line in lines[:10]:
        if 'Release date' in line:
            # use the release date as part of the filename
            parts = line.split(',')
            if len(parts) > 1:
                date_str = parts[1].strip().replace(' ', '_').replace(':', '-')
                # clean the date string to be a valid filename
                date_str = re.sub(r'[<>:"/\\|?*\'\"]', '', date_str)
                return date_str
    return None

for i, link in enumerate(csv_links):
    logging.info(f"Downloading {link}...")
    r = requests.get(link)
    r.raise_for_status() # raise an error if the download request returned an unsuccessful status code
    release_date = extract_release_date(r.content)
    if release_date:
        filename = os.path.join(dest_folder, f"vintage_{release_date}.csv")
    else:
        filename = os.path.join(dest_folder, f"file_{i+1}.csv")
    with open(filename, 'wb') as f:
        f.write(r.content)
    logging.info(f"Saved as {filename}")
    time.sleep(2)  # added 2 seconds delay between downloads to avoid request limit error from website
logging.info("Download complete.")
