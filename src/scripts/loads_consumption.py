import pandas as pd
from datetime import datetime, timedelta
import os

def loads_consumption(file_path):
    full_path = os.path.join("Electric_data", file_path)

    # Load the CSV file
    df = pd.read_csv(full_path)

    # Define the list of appliance columns
    appliance_columns = ['ac_1', 'ac_2', 'boiler', 'fridge', 'washing_machine']

    # Calculate the Load Consumption
    df['Load_Consumption'] = df['P_agg'] - df[appliance_columns].sum(axis=1)

    # Save the updated DataFrame back to the same CSV file
    df.to_csv(full_path, index=False)

# Date range: 2022-09 to 2023-09
start_date = datetime.strptime("2022-09", "%Y-%m")
end_date = datetime.strptime("2023-09", "%Y-%m")

# Build filenames list
filenames = []
current = start_date
while current <= end_date:
    filenames.append(current.strftime("%Y-%m") + ".csv")
    current += timedelta(days=31)
    current = current.replace(day=1)

# Apply function to each file
for filename in filenames:
    try:
        loads_consumption(filename)
        print(f"Processed: {filename}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")
