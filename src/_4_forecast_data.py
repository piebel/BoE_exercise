import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd
import os
import matplotlib.pyplot as plt


# ensure output folder exists
output_folder = "output_data"
os.makedirs(output_folder, exist_ok=True)

# load the merged vintages data
input_folder = "output_data"
df = pd.read_csv(os.path.join(input_folder, 'all_vintages.csv'))

# use the latest vintage (last column) for forecasting
latest_vintage = df.columns[-1]
series = df[["date", latest_vintage]].copy()
series = series.dropna()
series[latest_vintage] = pd.to_numeric(series[latest_vintage], errors='coerce')
series = series.dropna()

# convert 'date' to datetime (assume format 'YYYY MMM')

series['date'] = pd.to_datetime(series['date'], format='%Y %b')
series = series.set_index('date')
series = series.asfreq('MS')  # set frequency to month start


# rolling moving average forecast: for each future month, use the mean of the previous 12 values (including previous forecasts)
window = 12 # 12-month moving average
history = list(series[latest_vintage].tail(window)) # last 12 months of actual data
future_dates = pd.date_range(series.index[-1] + pd.offsets.MonthBegin(), periods=12, freq='MS') # this line generates the next 12 months of dates using pd.date_range to ensure correct monthly frequency
forecast_values = [] # to hold forecasted values
for _ in range(12): # for each future month
	next_value = sum(history[-window:]) / window # mean of last 12 values
	forecast_values.append(next_value) # append to forecast list
	history.append(next_value) # add to history for next iteration
forecast = pd.Series(forecast_values, index=future_dates) # create forecast series

# plot
plt.figure(figsize=(10,5))
plt.plot(series.index, series[latest_vintage], label='Actual')
plt.plot(forecast.index, forecast.values, label='Forecast', linestyle='--', marker='o')
plt.title(f'Vacancy Forecast using {latest_vintage}')
plt.xlabel('Date')
plt.ylabel('Vacancy Estimate')
plt.legend()
plt.tight_layout()

# save chart to output_data
chart_path = os.path.join(output_folder, 'vacancy_forecast.png')
plt.savefig(chart_path)
logging.info(f"Chart saved to {chart_path}")

# export forecast table to output_data
df_forecast = pd.DataFrame({'date': forecast.index.strftime('%Y %b'), 'forecast': forecast.values})
table_path = os.path.join(output_folder, 'vacancy_forecast_table.csv')
df_forecast.to_csv(table_path, index=False)
logging.info(f"Forecast table saved to {table_path}")
