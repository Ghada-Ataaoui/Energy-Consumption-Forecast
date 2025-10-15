import pandas as pd
import numpy as np
import os
import glob
import dotenv

# Load environment variables
dotenv.load_dotenv()

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
    
    # Fill NaNs using linear interpolation
    # df[appliance] = df[appliance].interpolate(method='linear')

    # # Compute 30-second rolling median
    # rolling_median = df[appliance].rolling('30s').median()
    resampled = df[appliance].resample('30s').first().dropna().reset_index()
    resampled['timestamp'] = resampled['timestamp'].astype('int64') // 10**9

    # Build DataFrame with required columns
    result = pd.DataFrame({
        'measurement': 'Electricity',
        'appliance': appliance,
        'value': resampled[appliance],
        'timestamp': resampled['timestamp']
    })
    
    # Save to CSV with columns
    output_folder = os.getenv('prediction_data_path')
    if not output_folder:
        raise EnvironmentError("❌ 'prediction_data_path' not found in .env file.")
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{appliance}_data_for_prediction.csv")
    result.to_csv(output_file, index=False)

    print(f"✅ Column-formatted data saved to {output_file}")

    # -----------------------------------------------
    # Example for InfluxDB formatted output (optional)
    # -----------------------------------------------
    # Final result DataFrame
    # result = pd.DataFrame({
    #     'measurement': 'Temperature',
    #     'type': appliance,
    #     'value': df[appliance],
    #     'timestamp': df.index.astype('int64') // 10**9
    # })
    # Format each row to a string like: measurement=,type= value= timestamp (influxdb format)
    # formatted_result = result.apply(
    #     lambda row: f"{row['measurement']},appliance={row['appliance']} value={row['value']} {row['timestamp']}",
    #     axis=1
    # )
    # # If needed as a list of strings
    # formatted_list = formatted_result.tolist()

    # # Define output path
    # output_folder = os.getenv('influxdb_data_path')
    # if not output_folder:
    #     raise EnvironmentError("❌ 'influxdb_data_path' not found in .env file.")
    # os.makedirs(output_folder, exist_ok=True)
    # output_file = os.path.join(output_folder, f"Extracted_{appliance}_data.csv")

    # # # Save to CSV
    # # formatted_list.to_csv(output_file, index=False)
    # # print(f"✅ Reformulated data saved to {output_file}")

    # with open(output_file, 'w') as f:
    #     for line in formatted_list:
    #         f.write(line + '\n')

    # return formatted_list

# Example usage
reformulate_data(os.getenv('electric_data_path'), 'P_agg')
