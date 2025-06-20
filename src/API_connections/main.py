from flask import Flask, jsonify
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load predictions once at startup
file_path = os.path.join(
    os.path.dirname(__file__),
    'C:\\Users\\Ghada\\Desktop\\Digital Twin\\Datasets\\Plegma_clean_dataset\\DT\\House_01\\Data\\data_preprocessed\\predicition_data\\fridge_data_for_prediction.csv'
)
df = pd.read_csv(file_path)
noise = np.random.normal(0, 0.5, size=len(df))
df['predicted_value'] = df['value'] + noise
predictions = df['predicted_value'].round(2).tolist()

# Global index
current_index = {'i': 0}

@app.route('/predict', methods=['GET'])
def predict():
    i = current_index['i']
    if i >= len(predictions):
        return jsonify({"prediction": None, "message": "End of data"})

    value = predictions[i]
    current_index['i'] += 1

    return jsonify({
        "prediction": value,
        "unit": "kWh"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
