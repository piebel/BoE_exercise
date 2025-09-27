#this script merges all vintage csv files into a single dataframe and exports it as all_vintages.csv

import os
import pandas as pd
import re
import logging
from datetime import datetime


input_folder = "input_data"
output_folder = "output_data"

all_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')] #list all csv files in input_data folder

all_vintages = pd.DataFrame() #prepare empty dataframe to hold all vintages

for file in all_files: #loop through each vintage file
    df = pd.read_csv(os.path.join(input_folder, file), skiprows=7) #skip the metadata rows
    col_name = os.path.splitext(file)[0].replace('vintage_', '')
    df = df.rename(columns={df.columns[0]: 'date', df.columns[1]: col_name})
    df = df[['date', col_name]]
    if all_vintages.empty:
        all_vintages = df.copy()
    else:
        all_vintages = pd.merge(all_vintages, df, on='date', how='outer')



    
# only keep rows where 'date' matches YYYY MMM (e.g., 2021 MAR), as the exercise specifies only monthly data is needed
month_pattern = re.compile(r'^\d{4}\s+[A-Z]{3}$')
all_vintages = all_vintages[all_vintages['date'].apply(lambda x: bool(month_pattern.match(str(x).strip())))]

# sort columns by vintage date in dd-mm-yyyy format
def extract_vintage_date(col):
    if col == 'date':
        return datetime.min
    # expecting format like '13-05-2025'
    match = re.search(r'(\d{2}-\d{2}-\d{4})', col)
    if match:
        try:
            return datetime.strptime(match.group(1), '%d-%m-%Y')
        except Exception:
            return datetime.max
    return datetime.max

#create dataframe in long format for easier sorting
cols = list(all_vintages.columns)
cols_sorted = ['date'] + sorted([c for c in cols if c != 'date'], key=extract_vintage_date)
all_vintages = all_vintages[cols_sorted]

# export to output_data folder
all_vintages.to_csv(os.path.join(output_folder, 'all_vintages.csv'), index=False)
logging.info(f"Merged dataframe saved as {os.path.join(output_folder, 'all_vintages.csv')}")