# src/feature_engineering.py

import pandas as pd
import os

def prepare_time_series_data(input_path='data/processed/jobs_with_skills.csv', output_dir='data/processed/timeseries'):
    """
    Transforms the processed job data into individual time series files for each skill.
    """
    try:
        df = pd.read_csv(input_path)
        df['skills'] = df['skills'].apply(eval)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    # Explode the DataFrame to have one row per skill per job posting
    exploded_df = df.explode('skills')

    # Get a list of unique skills to process
    unique_skills = exploded_df['skills'].unique()

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Preparing time series for {len(unique_skills)} skills...")

    for skill in unique_skills:
        # Filter for the current skill
        skill_df = exploded_df[exploded_df['skills'] == skill]

        # Count daily occurrences
        time_series = skill_df.groupby(pd.Grouper(key='timestamp', freq='D')).size().reset_index(name='count')

        # Rename columns to fit Prophet's requirements ('ds' and 'y')
        time_series.rename(columns={'timestamp': 'ds', 'count': 'y'}, inplace=True)

        # Save to a separate file
        output_path = os.path.join(output_dir, f"{skill}_timeseries.csv")
        time_series.to_csv(output_path, index=False)

    print(f"Time series data saved in '{output_dir}'")

if __name__ == '__main__':
    prepare_time_series_data()