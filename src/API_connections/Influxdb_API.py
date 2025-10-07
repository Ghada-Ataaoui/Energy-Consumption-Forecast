from flask import Flask, jsonify
from influxdb import InfluxDBClient
import threading
import time
import os
import os, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ==== Global Time Range ====
start_time = "2022-09-01T00:00:00Z"
end_time   = "2023-09-01T23:59:59Z"

# ==== InfluxDB Clients ====
client = InfluxDBClient(
    host=os.getenv("Host_ip"),  # Use the Host_ip from .env file
    port=os.getenv("Host_port"),
    username=os.getenv("Username"),
    password=os.getenv("Password"),
    database=os.getenv("Appliance_Database")
)

env_client = InfluxDBClient(
    host=os.getenv("Host_ip"),  # Use the Host_ip from .env file
    port=os.getenv("Host_port"),
    username=os.getenv("Username"),
    password=os.getenv("Password"),
    database=os.getenv("Env_Database")
)

hvac_client = InfluxDBClient(
    host=os.getenv("Host_ip"),  # Use the Host_ip from .env file
    port=os.getenv("Host_port"),
    username=os.getenv("Username"),
    password=os.getenv("Password"),
    database=os.getenv("HVAC_Database")
)

aggregated_consumption_client = InfluxDBClient(
    host=os.getenv("Host_ip"),  # Use the Host_ip from .env file
    port=os.getenv("Host_port"),
    username=os.getenv("Username"),
    password=os.getenv("Password"),
    database=os.getenv("Agg_Database")
)

# ==== Global storage for each appliance ====
data_store = {
    'fridge': [],
    'washing_machine': [],
    'boiler': [],
    'internal_temperature': [],
    'ac_1': [],                     
    'ac_2': [],                     
    'aggregated_consumption': []
}

index_store = {
    'fridge': 0,
    'washing_machine': 0,
    'boiler': 0,
    'internal_temperature': 0,
    'ac_1': 0,                      
    'ac_2': 0,                      
    'aggregated_consumption': 0
}


# ==== Load Appliance Data ====
def load_data(appliance, measurement="Electricity", db_client=client):
    all_data = []
    offset = 0
    batch_size = 1000

    while True:
        query = f"""
        SELECT "value" FROM "{measurement}"
        WHERE "appliance" = '{appliance}'
        AND time >= '{start_time}' AND time <= '{end_time}'
        ORDER BY time ASC
        LIMIT {batch_size} OFFSET {offset}
        """
        result = db_client.query(query)
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

# ==== Load Temperature Data ====
def load_data_temperature(type='internal_temperature', measurement="Temperature", db_client=env_client):
    all_data = []
    offset = 0
    batch_size = 1000

    while True:
        query = f"""
        SELECT "value" FROM "{measurement}"
        WHERE "type" = '{type}'
        AND time >= '{start_time}' AND time <= '{end_time}'
        ORDER BY time ASC
        LIMIT {batch_size} OFFSET {offset}
        """
        result = db_client.query(query)
        points = list(result.get_points())

        if not points:
            break

        for point in points:
            all_data.append({
                "value": point["value"],
                "timestamp": point["time"]
            })

        offset += batch_size

    data_store['internal_temperature'] = all_data
    print(f"✅ Loaded {len(all_data)} points for internal_temperature")

def load_hvac_data(appliance, measurement="Electricity", db_client=hvac_client):
    all_data = []
    offset = 0
    batch_size = 1000

    while True:
        query = f"""
        SELECT "value" FROM "{measurement}"
        WHERE "appliance" = '{appliance}'
        AND time >= '{start_time}' AND time <= '{end_time}'
        ORDER BY time ASC
        LIMIT {batch_size} OFFSET {offset}
        """
        result = db_client.query(query)
        points = list(result.get_points())

        if not points:
            break

        for point in points:
            all_data.append({
                "value": point["value"],
                "timestamp": point["time"]
            })

        offset += batch_size

    data_store[appliance]= all_data
    print(f"✅ Loaded {len(all_data)} points for HVAC consumption")

def load_aggregated_consumption_data(type, measurement="Electricity", db_client=aggregated_consumption_client):
    all_data = []
    offset = 0
    batch_size = 1000

    while True:
        query = f"""
        SELECT "value" FROM "{measurement}"
        WHERE "type" = '{type}'
        AND time >= '{start_time}' AND time <= '{end_time}'
        ORDER BY time ASC
        LIMIT {batch_size} OFFSET {offset}
        """
        result = db_client.query(query)
        points = list(result.get_points())

        if not points:
            break

        for point in points:
            all_data.append({
                "value": point["value"],
                "timestamp": point["time"]
            })

        offset += batch_size

    data_store['aggregated_consumption'] = all_data
    print(f"✅ Loaded {len(all_data)} points for aggregated consumption")

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

@app.route("/internal_temperature", methods=["GET"])
def temperature_api():
    idx = index_store['internal_temperature']
    return jsonify(data_store['internal_temperature'][idx])

@app.route("/ac_1", methods=["GET"])
def ac_1_api():
    idx = index_store['ac_1']
    return jsonify(data_store['ac_1'][idx])

@app.route("/ac_2", methods=["GET"])
def ac_2_api():  
    idx = index_store['ac_2']
    return jsonify(data_store['ac_2'][idx])

@app.route("/aggregated_consumption", methods=["GET"])
def aggregated_consumption_api():   
    idx = index_store['aggregated_consumption']
    return jsonify(data_store['aggregated_consumption'][idx])


# ==== Main entry ====
if __name__ == "__main__":
    # Load appliance data
    for appliance in ['fridge', 'washing_machine', 'boiler']:
        load_data(appliance)
        threading.Thread(target=update_stream, args=(appliance,), daemon=True).start()

    # Load temperature data
    load_data_temperature()
    threading.Thread(target=update_stream, args=('internal_temperature',), daemon=True).start()

    # Load HVAC data
    for appliance in ['ac_1', 'ac_2']:
        load_hvac_data(appliance)
        threading.Thread(target=update_stream, args=(appliance,), daemon=True).start()
    
    # Load aggregated consumption data
    load_aggregated_consumption_data('P_agg')
    threading.Thread(target=update_stream, args=('P_agg',), daemon=True).start()
    # Start Flask app
    app.run(host="0.0.0.0", port=5000)
