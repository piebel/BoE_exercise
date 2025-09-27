import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Load the merged vintages data
input_folder = "output_data"
output_folder = "output_data"

df = pd.read_csv(os.path.join(input_folder, 'all_vintages.csv'))

# user selects month from dropdown popup
months_available = sorted(df['date'].dropna().unique().tolist())


# dropdown popup for month selection
def select_month_popup(options):
    """Prompt the user to select a month from a dropdown list.

    Args:
        options (list): A list of month options to choose from.

    Returns:
        str: The month selected by the user.
    """
    selected = {'value': None}
    
    def on_select(event=None):
        """Handle the selection of a month from the dropdown.

        Args:
            event (Event, optional): The event triggering the selection. Defaults to None.
        """
        selected['value'] = combo.get() # get the selected month
        win.destroy() # close the popup window

    win = tk.Tk() # create a new tkinter window
    win.title('Select Month')
    tk.Label(win, text='Select month to plot for visualization of different vintages trends:').pack(padx=10, pady=5)

    combo = ttk.Combobox(win, values=options, state='readonly') # create a dropdown combobox that is readonly and populated with month options
    combo.pack(padx=10, pady=5) # add the combobox to the window
    combo.current(0) # set the default selected option to the first month
    combo.bind('<<ComboboxSelected>>', on_select) # bind the selection event to the on_select handler
    tk.Button(win, text='OK', command=on_select).pack(pady=5) # add an OK button to confirm selection
    win.mainloop() # start the tkinter event loop meaning the window stays open until closed
    return selected['value'] # return the selected month

month_to_plot = select_month_popup(months_available) #run the popup and get the selected month

assert re.match(r'^\d{4}\s+[A-Z]{3}$', month_to_plot) #month_to_plot must be in 'YYYY MMM' format, e.g., '2021 MAR'

row = df[df['date'] == month_to_plot] # filter the row for the given month
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
