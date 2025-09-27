
# Ensure requirements are installed before importing other modules
import subprocess
import sys
import os

# Install requirements at the start
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
except subprocess.CalledProcessError as e:
    print(f"Failed to install requirements: {e}")
    sys.exit(1)


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
