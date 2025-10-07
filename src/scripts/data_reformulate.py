import pandas as pd
import numpy as np
import os

def reformulate_data(data_folder: str, appliance: str):
    # Step 1: Generate list of monthly filenames from 2022-09 to 2023-08
    start = pd.Timestamp('2022-09')
    end = pd.Timestamp('2023-08')
    date_range = pd.date_range(start, end, freq='MS')
    file_list = [f"{data_folder}/{date.strftime('%Y-%m')}.csv" for date in date_range]

    # Step 2: Load and concatenate data
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

    # Step 3: Check for appliance column
    if appliance not in df.columns:
        raise ValueError(f"Appliance '{appliance}' not found in columns: {df.columns.tolist()}")

    # Step 4: Handle issue == -1 by replacing values with NaN
    if 'issue' in df.columns:
        df.loc[df['issue'] == 1, appliance] = np.nan

    # Step 5: IQR filtering to remove outliers (optional but helpful)
    Q1 = df[appliance].quantile(0.25)
    Q3 = df[appliance].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    lower_bound = Q1 - 1.5 * IQR
    df.loc[(df[appliance] > upper_bound) | (df[appliance] < lower_bound), appliance] = np.nan

    # Step 6: Interpolate missing values linearly
    df[appliance] = df[appliance].interpolate(method='linear')

    # Step 7: Resample every 30 seconds
    resampled = df[appliance].resample('30s').first().dropna().reset_index()
    resampled['timestamp'] = resampled['timestamp'].astype('int64') // 10**9

    # Step 8: Build output DataFrame
    result = pd.DataFrame({
        'measurement': 'Electricity',
        'appliance': appliance,
        'value': resampled[appliance],
        'timestamp': resampled['timestamp']
    })

    # Step 9: Save to CSV
    output_folder = r"C:\Users\Ghada\Desktop\Digital Twin\Datasets\Plegma_clean_dataset\DT\House_01\Data\data_preprocessed\predicition_data"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{appliance}_data_for_prediction.csv")
    result.to_csv(output_file, index=False)

    print(f"✅ Cleaned and formatted data saved to {output_file}")

# ✅ Example usage
reformulate_data(r'Data\Plegma Dataset\Electric_data', 'boiler')
