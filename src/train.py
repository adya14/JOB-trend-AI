# src/train.py

import pandas as pd
import os

# Import your custom functions
from feature_engineering import prepare_time_series_data
from model import forecast_skill_trend, plot_forecast

def run_pipeline():
    """
    Main function to run the entire forecasting pipeline.
    """
    # --- 1. Prepare the data ---
    print("Step 1: Preparing time series data...")
    timeseries_dir = 'data/processed/timeseries'
    prepare_time_series_data(output_dir=timeseries_dir)

    # --- 2. Run forecasting for each skill ---
    print("\nStep 2: Running forecasting models...")
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)

    # Get list of all skill data files
    try:
        skill_files = [f for f in os.listdir(timeseries_dir) if f.endswith('.csv')]
    except FileNotFoundError:
        print(f"Directory not found: {timeseries_dir}. Exiting.")
        return

    for skill_file in skill_files:
        skill_name = skill_file.replace('_timeseries.csv', '')
        print(f"  - Forecasting for: {skill_name}")

        # Load the data
        file_path = os.path.join(timeseries_dir, skill_file)
        skill_data = pd.read_csv(file_path)
        skill_data['ds'] = pd.to_datetime(skill_data['ds'])

        # Get forecast
        forecast_df = forecast_skill_trend(skill_data)

        if forecast_df is not None:
            # Save the forecast data to a CSV
            forecast_output_path = os.path.join(results_dir, f'{skill_name}_forecast.csv')
            forecast_df.to_csv(forecast_output_path, index=False)

            # Note: Prophet's plot functions don't return the model object needed for the plotting function.
            # A slight refactor of model.py would be needed to save plots directly.
            # For now, we save the data. Visualizing can be done in a notebook or a demo app.

    print(f"\nPipeline complete! All forecasts saved in the '{results_dir}' directory.")

if __name__ == '__main__':
    run_pipeline()