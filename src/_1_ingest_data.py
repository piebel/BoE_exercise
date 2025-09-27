#this script scrapes the ONS website for CSV download links of employment data vintages, downloads the first 25 CSV files, and saves them locally with filenames that include their release dates.


import logging
import os
import time
from _0_utils import extract_release_date, get_ons_csv_links

# logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# url to scrape
URL = "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/lms/previous"

csv_links = get_ons_csv_links(URL, max_files=25)

dest_folder = "input_data"
os.makedirs(dest_folder, exist_ok=True)


import requests
# Allow for proxies via environment variables (HTTP_PROXY, HTTPS_PROXY)
proxies = {
    'http': os.environ.get('HTTP_PROXY'),
    'https': os.environ.get('HTTPS_PROXY')
}
# Remove None values if not set
proxies = {k: v for k, v in proxies.items() if v}

for i, link in enumerate(csv_links):
    logging.info(f"Downloading {link}...")
    try:
        if proxies:
            r = requests.get(link, proxies=proxies)
        else:
            r = requests.get(link)
        r.raise_for_status()
        release_date = extract_release_date(r.content)
        if release_date:
            filename = os.path.join(dest_folder, f"vintage_{release_date}.csv")
        else:
            filename = os.path.join(dest_folder, f"file_{i+1}.csv")
        with open(filename, 'wb') as f:
            f.write(r.content)
        logging.info(f"Saved as {filename}")
    except Exception as e:
        logging.error(f"Failed to download {link}: {e}")
    time.sleep(2)
logging.info("Download complete.")
