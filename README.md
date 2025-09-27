# Vacancy Vintages Forecasting Project

This project downloads, processes, visualizes, and forecasts UK vacancy data vintages from the ONS website.

## Project Structure

- `src/` — Source scripts and utilities:
   - `_0_utils.py`: Shared utility functions for all scripts (data extraction, merging, popup, forecasting, etc.).
   - `_1_ingest_data.py`: Downloads the latest 25 CSV vintages from the ONS website (uses utilities).
   - `_2_prepare_data.py`: Cleans and merges vintages into a single CSV (uses utilities).
   - `_3_visualize_data.py`: Interactive visualization of how a given month's estimate changes across vintages (uses utilities).
   - `_4_forecast_data.py`: Forecasts future vacancy levels using the latest vintage (uses utilities).
- `output_data/` — All outputs (merged CSVs, charts, forecast tables, etc.)
- `requirements.txt` — Python dependencies.
- `execute_exercise.py` — Runs the full pipeline in order, ensuring all dependencies are installed.

## Setup

1. **Clone the repository** (if not already):
   ```sh
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. **Install Python 3.8+** (if not already installed).

3. **Install dependencies** (automatically handled by `run_all.py`, or manually):
   ```sh
   pip install -r requirements.txt
   ```

## Usage


### Full Pipeline (Recommended)
Run all steps in order:
```sh
python execute_exercise.py
```
This will:
- Ensure all dependencies are installed
- Download the latest data
- Prepare and merge vintages
- Let you interactively visualize a month
- Forecast future values and save results to `output_data/`

### Individual Steps

You can also run any script in `src/` individually:
```sh
python src/_1_ingest_data.py
python src/_2_prepare_data.py
python src/_3_visualize_data.py
python src/_4_forecast_data.py
```

## Notes
- All outputs (charts, merged CSVs, forecast tables) are saved in the `output_data/` folder.
- The visualization script will prompt you to select a month for comparison.
- The forecast uses a rolling moving average by default.

## License
MIT License
