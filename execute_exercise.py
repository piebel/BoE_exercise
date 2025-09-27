
# Ensure requirements are installed before importing other modules
import importlib.util
import importlib
import subprocess
import sys
import os

# Ensure pkg_resources is available (install setuptools if needed)
try:
    import pkg_resources
except ImportError:
    print("pkg_resources not found. Installing setuptools...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'setuptools'])
    import pkg_resources



# Check if all requirements are installed
def check_requirements(requirements_file='requirements.txt'):
    """Check if all requirements in requirements.txt are installed."""
    try:
        with open(requirements_file) as f:
            requirements = f.read().splitlines()
        pkg_resources.require(requirements)
        print("All requirements are satisfied.")
    except pkg_resources.DistributionNotFound as e:
        print(f"Missing package: {e.report()}")
        sys.exit(1)
    except pkg_resources.VersionConflict as e:
        print(f"Version conflict: {e.report()}")
        sys.exit(1)

# Check requirements before running anything else
check_requirements()

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
