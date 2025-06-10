import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Load data
df = pd.read_csv('fridge_data_for_prediction.csv')

# Convert timestamp to datetime (assuming it's in seconds since epoch)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Plot the 30-second resolution data
plt.figure(figsize=(15, 5))
plt.plot(df['timestamp'], df['value'], linestyle='-', marker='o', markersize=2, color='purple')
plt.title('Fridge Consumption (30s Resolution)')
plt.xlabel('Time')
plt.ylabel('Watts')

# Format x-axis to show date and time
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.xticks(rotation=45)

plt.grid(True)
plt.tight_layout()
plt.show()