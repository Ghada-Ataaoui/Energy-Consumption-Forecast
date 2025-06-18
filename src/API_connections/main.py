from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    # Here you would call your actual ML model
    # For demo: just return a dummy value
    prediction = round(np.random.uniform(10, 15), 2)  # e.g., 12.34 kWh

    return jsonify({
        "prediction": prediction,
        "unit": "kWh"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Accessible from other devices
