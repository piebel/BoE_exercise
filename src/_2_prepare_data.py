#this script merges all vintage csv files into a single dataframe and exports it as all_vintages.csv

import os
import logging
from _0_utils import merge_vintage_csvs, sort_vintage_columns

input_folder = "input_data"
output_folder = "output_data"

all_vintages = merge_vintage_csvs(input_folder)
all_vintages = sort_vintage_columns(all_vintages)

# export to output_data folder
all_vintages.to_csv(os.path.join(output_folder, 'all_vintages.csv'), index=False)
logging.info(f"Merged dataframe saved as {os.path.join(output_folder, 'all_vintages.csv')}")