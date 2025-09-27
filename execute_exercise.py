

import os
import subprocess
import sys
from src._0_utils import install_missing_requirements

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
install_missing_requirements(requirements_path)


import logging

logging.basicConfig(level=logging.INFO)

# Define the scripts in the correct order
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
