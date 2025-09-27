

# Ensure requirements are installed before importing other modules
import importlib.util
import importlib
import subprocess
import sys
import os

def _install_missing_requirements(requirements_path):
    """Install missing Python packages listed in a requirements file.

    Args:
        requirements_path (str): The path to the requirements file.

    Raises:
        ImportError: If src._0_utils cannot be found.
    """
    spec = importlib.util.find_spec('src._0_utils')
    if spec is None:
        raise ImportError('src._0_utils must be present in src directory.')
    _0_utils = importlib.import_module('src._0_utils')
    _0_utils.install_missing_requirements(requirements_path)

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
_install_missing_requirements(requirements_path)

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
