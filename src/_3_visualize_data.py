
import logging
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime
from _0_utils import select_month_popup, extract_vintage_date




# Load the merged vintages data
input_folder = "output_data"
output_folder = "output_data"
df = pd.read_csv(os.path.join(input_folder, 'all_vintages.csv'))

# user selects month from dropdown popup
months_available = sorted(df['date'].dropna().unique().tolist())
month_to_plot = select_month_popup(months_available)

assert re.match(r'^\d{4}\s+[A-Z]{3}$', month_to_plot)

row = df[df['date'] == month_to_plot]
if row.empty:
    logging.info(f"No data found for {month_to_plot}")
else:
    # drop the 'date' column and transpose to get vintage names and values
    vintages = row.drop('date', axis=1).T
    vintages.columns = ['Vacancy Estimate']
    vintages = vintages.reset_index().rename(columns={'index': 'Vintage'})
    # sort vintages by date if possible
   
    vintages = vintages.sort_values(by='Vintage', key=lambda x: x.apply(extract_vintage_date)) # sort using the extracted dates
    # plot
    os.makedirs(output_folder, exist_ok=True)
    plt.figure(figsize=(10,5))
    x = vintages['Vintage']
    y = vintages['Vacancy Estimate']
    plt.plot(x, y, marker='o', label='Estimate')

    # highlight revision points (where value changes)
    diffs = y.diff().fillna(0)
    revision_points = diffs != 0
    plt.scatter(x[revision_points], y[revision_points], color='red', zorder=5, label='Revision')

    # annotate largest upward and downward revision
    if len(diffs) > 1:
        max_up_idx = diffs.idxmax()
        max_down_idx = diffs.idxmin()
        if diffs[max_up_idx] > 0:
            plt.annotate('Largest Upward Revision', (x[max_up_idx], y[max_up_idx]),
                         textcoords="offset points", xytext=(0,10), ha='center', color='green', fontsize=8, arrowprops=dict(arrowstyle='->', color='green'))
        if diffs[max_down_idx] < 0:
            plt.annotate('Largest Downward Revision', (x[max_down_idx], y[max_down_idx]),
                         textcoords="offset points", xytext=(0,-15), ha='center', color='purple', fontsize=8, arrowprops=dict(arrowstyle='->', color='purple'))

    plt.title(f'Vacancy Estimate for {month_to_plot} across Vintages')
    plt.xlabel('Vintage')
    plt.ylabel('Vacancy Estimate')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    chart_path = os.path.join(output_folder, f'vintages_{month_to_plot.replace(" ", "_")}.png')
    plt.savefig(chart_path)
    logging.info(f"Chart saved to {chart_path}")
