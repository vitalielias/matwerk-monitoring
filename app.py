import logging
import os
import tomllib
import json

from flask import Flask, render_template, jsonify, make_response
import pandas as pd

app = Flask(__name__)
logging.basicConfig(level = logging.INFO)
# Define the data for multiple tables
# dataframes = {
#     "sample_table": pd.DataFrame({
#         "Name": ["Alice", "Bob", "Charlie"],
#         "Age": [25, 30, 35],
#         "Occupation": ["Engineer", "Doctor", "Lawyer"]
#     }),
#     "metrics_table": pd.DataFrame({
#         'Metric': [
#             'Unique Users', 'Location of Users', 'Processed Gigabytes of Images', 'Number of Extractions/ Mappings',
#             'Processing Time per Image', 'User Engagement', 'Schema/Plugin Usage', 'Repeat Usage',
#             'API Response Times', 'Documentation Access', 'User Growth Rate', 'Number of Plugins'
#         ],
#         'Value': [100, 50, 200, 75, 0.5, 120, 30, 40, 0.1, 15, 10, 8]  # Dummy data
#     })
# }

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load DataFrames from JSON files
dataframes = {}
for filename in os.listdir('data'):
    if filename.endswith('.json'):
        name = filename.split('.')[0]
        with open(f'data/{filename}', 'r') as f:
            data = json.load(f)
            if name in data:  # Ensure the key exists in the JSON data
                df = pd.DataFrame(data[name])
                dataframes[name] = df

def get_version():
    with open("pyproject.toml", "rb") as f:
        version = tomllib.load(f)["tool"]["poetry"]["version"]
    return version


version = get_version()


# == INDEX PAGE ==
@app.route("/")
def index():
    return render_template(
        "index.html.j2", version=version, report_time="2024-07-07 @ 12:00"
    )

# @app.route("/plot/<plot_name>")
# def plot(plot_name: str):
#     """
#     Loads a plot and returns it as a JSON object.
#     """
#     logging.info(f"Loading plot {plot_name}")

#     # Load a demo plot
#     if plot_name == "sample_plot":
#         return {
#             "data": [
#                 {
#                     "type": "scatter",
#                     "x": [1, 2, 3, 4],
#                     "y": [10, 11, 12, 13],
#                     "mode": "lines+markers",
#                     "name": "Sample Plot",
#                } 
#             ],
#             "layout": {
#                 "title": "Sample Plot",
#                 "xaxis": {"title": "X Axis"},
#                 "yaxis": {"title": "Y Axis"},
#             },
#         }

#     return {"error": f"Plot {plot_name} not found"}, 404
@app.route("/plot/<plot_name>")
def get_plot(plot_name):
    df = dataframes.get(plot_name)
    if df is not None:
        data = {
            'x': df['dates'].tolist(),
            'y': df['users'].tolist()
        }
        return jsonify(data)
    return jsonify({"error": "Plot not found"}), 404

@app.route("/table/<table_name>")
def table(table_name: str):
    """
    Loads a table and returns it as html.
    """
    logging.info(f"Loading table {table_name}")

    # Load the table
    df = dataframes.get(table_name)
    if df is not None:
        table_html = df.to_html(index=False, classes="table table-condensed")
        return {"html": table_html}

    return {"error": f"Table {table_name} not found"}, 404
# def table(table_name: str):
#     """
#     Loads a table and returns it as html.
#     """
#     logging.info(f"Loading table {table_name}")

#     # Load a demo table
#     if table_name == "sample_table":
#         df = pd.DataFrame(
#             {
#                 "Name": ["Alice", "Bob", "Charlie"],
#                 "Age": [25, 30, 35],
#                 "Occupation": ["Engineer", "Doctor", "Lawyer"],
#             }
#         )

#         return {"html": df.to_html(index=False, classes="table table-condensed")}

#     return {"error": f"Table {table_name} not found"}, 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3838))
    app.run(debug=True, host="0.0.0.0", port=port)
