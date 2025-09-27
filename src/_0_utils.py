"""
utils.py
This module contains utility functions shared across the project scripts.
"""

import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import importlib.util
import subprocess
import sys

def install_missing_requirements(requirements_path):
    """Install missing Python packages listed in a requirements file.

    Args:
        requirements_path (str): The path to the requirements file.
    """
    with open(requirements_path) as f:
        required = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    missing = []
    for req in required:
        pkg_name = req.split('[')[0].split('==')[0].replace('-', '_')
        if importlib.util.find_spec(pkg_name) is None:
            missing.append(req)
    if missing:
        print(f"Installing missing packages: {missing}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
    else:
        print("All required packages are already installed.")


# --- Ingest Data Utilities ---
def extract_release_date(csv_content):
    """Extract the release date from the CSV content.

    Args:
        csv_content (bytes): The content of the CSV file.   

    Returns:
        str: The extracted release date or None if not found.
    """
    lines = csv_content.decode(errors='ignore').splitlines()
    for line in lines[:10]:
        if 'Release date' in line:
            parts = line.split(',')
            if len(parts) > 1:
                date_str = parts[1].strip()
                # Remove invalid filename characters (including quotes)
                date_str = re.sub(r'[<>:"/\\|?*\'\"]', '', date_str)
                return date_str
    return None

def get_ons_csv_links(url, max_files=25):
    """Scrape ONS page for CSV download links.

    Args:
        url (str): The URL of the ONS page to scrape.
        max_files (int, optional): The maximum number of CSV files to download. Defaults to 25.

    Returns:
        list: A list of CSV download links.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r'generator\?format=csv&uri=.*?/v\d+$')
    csv_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if pattern.search(href):
            if href.startswith('http'):
                csv_links.append(href)
            else:
                csv_links.append('https://www.ons.gov.uk' + href)
        if len(csv_links) >= max_files:
            break
    return csv_links

# --- Prepare Data Utilities ---
def merge_vintage_csvs(input_folder):
    """Merge all vintage CSVs into a single DataFrame.

    Args:
        input_folder (str): The path to the folder containing vintage CSV files.

    Returns:
        pd.DataFrame: A DataFrame containing the merged vintage data.
    """
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    all_vintages = pd.DataFrame()
    for file in all_files:
        df = pd.read_csv(os.path.join(input_folder, file), skiprows=7)
        col_name = os.path.splitext(file)[0].replace('vintage_', '')
        df = df.rename(columns={df.columns[0]: 'date', df.columns[1]: col_name})
        df = df[['date', col_name]]
        if all_vintages.empty:
            all_vintages = df.copy()
        else:
            all_vintages = pd.merge(all_vintages, df, on='date', how='outer')
    # Only keep rows where 'date' matches YYYY MMM
    month_pattern = re.compile(r'^\d{4}\s+[A-Z]{3}$')
    all_vintages = all_vintages[all_vintages['date'].apply(lambda x: bool(month_pattern.match(str(x).strip())))]
    return all_vintages

def extract_vintage_date(col):
    """Extract the vintage date from the column name.

    Args:
        col (str): The column name.

    Returns:
        datetime: The extracted vintage date or a maximum datetime if parsing fails.
    """
    if col == 'date':
        return datetime.min
    match = re.search(r'(\d{2}-\d{2}-\d{4})', col)
    if match:
        try:
            return datetime.strptime(match.group(1), '%d-%m-%Y')
        except Exception:
            return datetime.max
    return datetime.max

def sort_vintage_columns(df):
    """Sort the columns of the DataFrame by vintage date.

    Args:
        df (pd.DataFrame): The DataFrame to sort.

    Returns:
        pd.DataFrame: The DataFrame with sorted columns.
    """
    cols = list(df.columns)
    cols_sorted = ['date'] + sorted([c for c in cols if c != 'date'], key=extract_vintage_date)
    return df[cols_sorted]

# --- Visualize Data Utilities ---
def select_month_popup(options):
    """Prompt the user to select a month from a dropdown list.

    Args:
        options (list): A list of month options to choose from.

    Returns:
        str: The selected month.
    """
    selected = {'value': None}
    def on_select(event=None):
        selected['value'] = combo.get()
        win.destroy()
    win = tk.Tk()
    win.title('Select Month')
    tk.Label(win, text='Select month to plot for visualization of different vintages trends:').pack(padx=10, pady=5)
    combo = ttk.Combobox(win, values=options, state='readonly')
    combo.pack(padx=10, pady=5)
    combo.current(0)
    combo.bind('<<ComboboxSelected>>', on_select)
    tk.Button(win, text='OK', command=on_select).pack(pady=5)
    win.mainloop()
    return selected['value']

# --- Forecast Data Utilities ---
def moving_average_forecast(series, window=12, periods=12):
    """Generate a moving average forecast.

    Args:
        series (pd.Series): The time series data to forecast.
        window (int, optional): The window size for the moving average. Defaults to 12.
        periods (int, optional): The number of periods to forecast. Defaults to 12.

    Returns:
        list: A list of forecasted values.
    """
    history = list(series.tail(window))
    forecast_values = []
    for _ in range(periods):
        next_value = sum(history[-window:]) / window
        forecast_values.append(next_value)
        history.append(next_value)
    return forecast_values
