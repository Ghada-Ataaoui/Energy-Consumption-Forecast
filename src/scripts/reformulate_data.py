import pandas as pd
import numpy as np
import os

def reformulate_data(data_folder: str, appliance: str):
    # Generate list of monthly filenames from 2022-09 to 2023-08
    start = pd.Timestamp('2022-09')
    end = pd.Timestamp('2023-08')
    date_range = pd.date_range(start, end, freq='MS')
    file_list = [f"{data_folder}/{date.strftime('%Y-%m')}.csv" for date in date_range]

    # Load and concatenate data
    df_list = []
    for file in file_list:
        if os.path.exists(file):
            df_month = pd.read_csv(file, parse_dates=["timestamp"])
            df_list.append(df_month)
        else:
            print(f"⚠️ File not found: {file}")

    if not df_list:
        raise FileNotFoundError("❌ No data files found for the specified date range.")

    df = pd.concat(df_list, ignore_index=True)
    df = df.sort_values("timestamp")
    df.set_index("timestamp", inplace=True)

    if appliance not in df.columns:
        raise ValueError(f"Appliance '{appliance}' not found in columns: {df.columns.tolist()}")

    # Compute 30-second rolling median
    rolling_median = df[appliance].rolling('30s').median()
    resampled = rolling_median.resample('30s').first().dropna().reset_index()
    resampled['timestamp'] = resampled['timestamp'].astype('int64') // 10**9

    # Final result DataFrame
    result = pd.DataFrame({
        'measurement': 'Electricity',
        'appliance': appliance,
        'value': resampled[appliance],
        'timestamp': resampled['timestamp']
    })

    # Define output path
    output_folder = r"C:\Users\Ghada\Desktop\Digital Twin\Datasets\Plegma_clean_dataset\DT\House_01\Data\data_preprocessed\predicition_data"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{appliance}_data_for_prediction.csv")
    
    # Save to CSV
    result.to_csv(output_file, index=False)
    print(f"✅ Reformulated data saved to {output_file}")
    
    return result

# Example usage
df = reformulate_data('Data\Plegma Dataset\Electric_data', 'washing_machine')
