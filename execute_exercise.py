

# Ensure correct Python version (3.12)
import sys
if not (sys.version_info.major == 3 and sys.version_info.minor == 12):
    print(f"Error: Python 3.12 is required. You are using {sys.version.split()[0]}")
    sys.exit(1)

import subprocess
import os
import json


# Install requirements at the start
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
except subprocess.CalledProcessError as e:
    print(f"Failed to install requirements: {e}")
    sys.exit(1)


import logging
logging.basicConfig(level=logging.INFO)


# --- Proxy configuration --- for instance, ECB requires proxies to access external sites
proxies = {
    # Example: uncomment and edit as needed
    # 'http': 'http://proxy.example.com:8080',
    # 'https': 'http://proxy.example.com:8080',
}

# Save proxies to a file for use by _1_ingest_data.py
with open('proxies.json', 'w') as f:
    json.dump(proxies, f)

scripts = [
    os.path.join('src', '_1_ingest_data.py'),
    os.path.join('src', '_2_prepare_data.py'),
    os.path.join('src', '_3_visualize_data.py'),
    os.path.join('src', '_4_forecast_data.py'),
]

for script in scripts:
    logging.info(f"Running {script}...")
    process = subprocess.Popen([sys.executable, script], stdout=None, stderr=None)
    retcode = process.wait()
    if retcode != 0:
        logging.info(f"Script {script} failed with exit code {retcode}.")
        break
else:
    logging.info("All scripts ran successfully.")
