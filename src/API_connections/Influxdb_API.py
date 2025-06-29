from flask import Flask, jsonify
from influxdb import InfluxDBClient
import threading
import time

app = Flask(__name__)

# ==== InfluxDB Setup ====
client = InfluxDBClient(
    host='192.168.0.207',
    port=8086,
    username='Ghada',
    password='0000',
    database='Appliance_Electricity'
)

# ==== Global storage for each appliance ====
data_store = {
    'fridge': [],
    'washing_machine': [],
    'boiler': []
}
index_store = {
    'fridge': 0,
    'washing_machine': 0,
    'boiler': 0
}

# ==== Load Data Once ====
def load_data(appliance):
    all_data = []
    offset = 0
    batch_size = 1000
    start_time = "2022-08-31T00:00:00Z"
    end_time   = "2022-10-10T23:59:59Z"

    while True:
        query = f"""
        SELECT "value" FROM "Electricity"
        WHERE "appliance" = '{appliance}'
        AND time >= '{start_time}' AND time <= '{end_time}'
        ORDER BY time ASC
        LIMIT {batch_size} OFFSET {offset}
        """
        result = client.query(query)
        points = list(result.get_points())

        if not points:
            break

        for point in points:
            all_data.append({
                "value": point["value"],
                "timestamp": point["time"]
            })

        offset += batch_size

    data_store[appliance] = all_data
    print(f"✅ Loaded {len(all_data)} points for {appliance}")

# ==== Background thread to simulate streaming ====
def update_stream(appliance):
    while True:
        if appliance in data_store and data_store[appliance]:
            index_store[appliance] = (index_store[appliance] + 1) % len(data_store[appliance])
        time.sleep(3)

# ==== Flask Routes ====
@app.route("/fridge", methods=["GET"])
def fridge_api():
    idx = index_store['fridge']
    return jsonify(data_store['fridge'][idx])

@app.route("/washing_machine", methods=["GET"])
def washer_api():
    idx = index_store['washing_machine']
    return jsonify(data_store['washing_machine'][idx])

@app.route("/boiler", methods=["GET"])
def boiler_api():
    idx = index_store['boiler']
    return jsonify(data_store['boiler'][idx])

# ==== Main entry ====
if __name__ == "__main__":
    for appliance in data_store:
        load_data(appliance)
        threading.Thread(target=update_stream, args=(appliance,), daemon=True).start()

    app.run(host="0.0.0.0", port=5000)
