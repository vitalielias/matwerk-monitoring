import json
from datetime import datetime
from collections import defaultdict
import requests
import os

def parse_ips(input_file, output_dir):
    # Load data
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Prepare data structures
    accesses_per_hour = defaultdict(int)
    unique_accesses_per_hour = defaultdict(set)
    location_counts = defaultdict(int)
    city_coordinates = {}

    for entry in data:
        timestamp = datetime.fromisoformat(entry['timestamp'])
        hour = timestamp.replace(minute=0, second=0, microsecond=0)
        ip = entry['ip']

        accesses_per_hour[hour] += 1
        unique_accesses_per_hour[hour].add(ip)

        # Get location data
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success' and result['country'] == 'Germany':
                city = result['city']
                location_counts[city] += 1
                city_coordinates[city] = (result['lat'], result['lon'])

    # Prepare JSON data
    user_growth_data = {
        "data": [
            {
                "type": "scatter",
                "x": [hour.isoformat() for hour in sorted(accesses_per_hour.keys())],
                "y": [accesses_per_hour[hour] for hour in sorted(accesses_per_hour.keys())],
                "mode": "lines+markers",
                "name": "User Accesses"
            }
        ],
        "layout": {
            "title": "Number of Accesses per Hour",
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Number of Accesses"}
        }
    }

    unique_accesses_data = {
        "data": [
            {
                "type": "scatter",
                "x": [hour.isoformat() for hour in sorted(unique_accesses_per_hour.keys())],
                "y": [len(unique_accesses_per_hour[hour]) for hour in sorted(unique_accesses_per_hour.keys())],
                "mode": "lines+markers",
                "name": "Unique User Accesses"
            }
        ],
        "layout": {
            "title": "Number of Unique Accesses per Hour",
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Number of Unique Accesses"}
        }
    }

    user_distribution_data = {
        "data": [
            {
                "type": "scattergeo",
                "locationmode": "country names",
                "lat": [coords[0] for coords in city_coordinates.values()],
                "lon": [coords[1] for coords in city_coordinates.values()],
                "text": [f"{city}: {count}" for city, count in location_counts.items()],
                "marker": {
                    "size": [count for count in location_counts.values()],
                    "color": [count for count in location_counts.values()],
                    "colorscale": "Viridis",
                    "colorbar": {"title": "Number of Users"},
                    "line": {"color": "darkgray", "width": 0.5}
                }
            }
        ],
        "layout": {
            "title": "User Distribution in Germany",
            "geo": {
                "scope": "europe",
                "projection": {"type": "mercator"},
                "center": {"lat": 51.1657, "lon": 10.4515},  # Centered on Germany
                "showland": True,
                "landcolor": "rgb(217, 217, 217)",
                "subunitwidth": 1,
                "countrywidth": 1,
                "subunitcolor": "rgb(255, 255, 255)",
                "countrycolor": "rgb(255, 255, 255)",
                "lonaxis": {"range": [5.5, 15.5]},  # Approximate bounds for Germany
                "lataxis": {"range": [47.0, 55.0]}  # Approximate bounds for Germany
            }
        }
    }

    # Save JSON data
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'user_growth.json'), 'w') as file:
        json.dump(user_growth_data, file, indent=4)
    with open(os.path.join(output_dir, 'unique_accesses.json'), 'w') as file:
        json.dump(unique_accesses_data, file, indent=4)
    with open(os.path.join(output_dir, 'user_distribution.json'), 'w') as file:
        json.dump(user_distribution_data, file, indent=4)


input_file = '/var/www/matwerk-monitoring/data/ips_2024-08-1_timestamps.json'
output_dir = '/var/www/matwerk-monitoring/data/'
parse_ips(input_file, output_dir)