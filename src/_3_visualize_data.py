
import logging
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime
from _0_utils import select_month_popup




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
   
    def extract_vintage_date(v):
        """Extract the date from the vintage string.

        Args:
            v (str): The vintage string.

        Returns:
            datetime: The extracted date or a maximum datetime if parsing fails.
        """
        match = re.search(r'(\d{2}-\d{2}-\d{4})', v)
        if match:
            try:
                return datetime.strptime(match.group(1), '%d-%m-%Y')
            except Exception:
                return datetime.max
        return datetime.max
    

    vintages = vintages.sort_values(by='Vintage', key=lambda x: x.apply(extract_vintage_date)) # sort using the extracted dates
    # plot
    os.makedirs(output_folder, exist_ok=True)
    plt.figure(figsize=(10,5))
    plt.plot(vintages['Vintage'], vintages['Vacancy Estimate'], marker='o')
    plt.title(f'Vacancy Estimate for {month_to_plot} across Vintages')
    plt.xlabel('Vintage')
    plt.ylabel('Vacancy Estimate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart_path = os.path.join(output_folder, f'vintages_{month_to_plot.replace(" ", "_")}.png')
    plt.savefig(chart_path)
    logging.info(f"Chart saved to {chart_path}")
