import pandas as pd
import numpy as np
import os

def reformulate_data(data_folder: str, appliance: str):
    # Generate list of monthly filenames from 2022-09 to 2023-02
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

    # Sort the data by timestamp
    df = df.sort_values("timestamp")

    # Set timestamp as index
    df.set_index("timestamp", inplace=True)

    # Check if appliance column exists
    if appliance not in df.columns:
        raise ValueError(f"Appliance '{appliance}' not found in columns: {df.columns.tolist()}")

    # Compute 30-second rolling median on the appliance column
    rolling_median = df[appliance].rolling('30s').median()

    # Resample to get non-overlapping 30-second intervals
    resampled = rolling_median.resample('30s').first().dropna().reset_index()

    # Convert timestamp to UNIX timestamp in seconds
    resampled['timestamp'] = resampled['timestamp'].astype('int64') // 10**9

    # # Format each row (InfluxDB line protocol)
    # formatted_lines = resampled.apply(
    #     lambda row: f"Electricity,type={appliance} value={row[appliance]:.3f} {int(row['timestamp'])}",
    #     axis=1
    # )
    #     # Format each row (InfluxDB line protocol)
    # formatted_lines = resampled.apply(
    #     lambda row: f"{int(row['timestamp'])},{row[appliance]:.3f} ",
    #     axis=1
    # )
    # Create final result DataFrame
    result = pd.DataFrame({
        'measurement': 'Electricity',
        'appliance': appliance,
        'value': resampled[appliance],
        'timestamp': resampled['timestamp']
    })

    # Save the result DataFrame to CSV
    output_file = f"{appliance}_data_for_prediction.csv"
    result.to_csv(output_file, index=False)

    print(f"✅ Reformulated data saved to {output_file}")
    return result

# Example usage
df = reformulate_data('Electric_data', 'P_agg')