from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import os
from utils.geojson_converter import convert_to_geojson

app = Flask(__name__)
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded.csv')
    file.save(filepath)
    df = pd.read_csv(filepath)

    with open('data/ph_regions.json') as f:
        raw_json = json.load(f)

    geojson_data, risk_map = convert_to_geojson(raw_json, df)

    # Convert to sorted list
    ranked_list = sorted(risk_map.items(), key=lambda x: x[1], reverse=True)

    # Prepare table data
    table_data = df.to_dict('records')

    return jsonify({
        "geojson": geojson_data,
        "rankings": ranked_list,
        "tableData": table_data
    })

if __name__ == '__main__':
    app.run(debug=True)