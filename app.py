import logging
import os
import tomllib
import json
from datetime import datetime

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


def get_version():
    with open("pyproject.toml", "rb") as f:
        version = tomllib.load(f)["tool"]["poetry"]["version"]
    return version


version = get_version()


# == INDEX PAGE ==
@app.route("/monitoring")
def index():
    return render_template(
        "index.html.j2",
        version=version,
        report_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # not proper bc it updates when page is refreshed instead of when data is updated, but ok for now.
    )


@app.route("/monitoring/mapping-service")
def mapping_service():
    return render_template(
        "mapping-service-metrics.html.j2",
        version=version,
        report_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # not proper bc it updates when page is refreshed instead of when data is updated, but ok for now.
    )

@app.route("/monitoring/evoks")
def evoks():
    return render_template(
        "evoks-metrics.html.j2",
        version=version,
        report_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # not proper bc it updates when page is refreshed instead of when data is updated, but ok for now.
    )

@app.route("/monitoring/repository")
def repository():
    return render_template(
        "evoks-metrics.html.j2",
        version=version,
        report_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # not proper bc it updates when page is refreshed instead of when data is updated, but ok for now.
    )

@app.route("/monitoring/DCE")
def dce():
    return render_template(
        "evoks-metrics.html.j2",
        version=version,
        report_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # not proper bc it updates when page is refreshed instead of when data is updated, but ok for now.
    )

@app.route("/monitoring/FAIRDOScope")
def fairdoscope():
    return render_template(
        "evoks-metrics.html.j2",
        version=version,
        report_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # not proper bc it updates when page is refreshed instead of when data is updated, but ok for now.
    )


@app.route("/plot/<plot_name>")
def plot(plot_name: str):
    """
    Loads a plot and returns it as a JSON object.
    """
    logging.info(f"Loading plot {plot_name}")

    plotFile = 'data/' + plot_name + '.json'
    if os.path.isfile(plotFile):
        with open(plotFile, 'r') as f:
            return json.load(f)

    return {"error": f"Plot {plot_name} not found"}, 404


@app.route("/table/<table_name>")
def table(table_name: str):
    """
    Loads a table and returns it as html.
    """
    logging.info(f"Loading table {table_name}")

    # Load a demo table
    if table_name == "sample_table":
        df = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Age": [25, 30, 35],
                "Occupation": ["Engineer", "Doctor", "Lawyer"],
            }
        )

        return {"html": df.to_html(index=False, classes="table table-condensed")}

    return {"error": f"Table {table_name} not found"}, 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3838))
    app.run(debug=True, host="0.0.0.0", port=port)
