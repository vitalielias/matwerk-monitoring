import json
import os
import sys
from datetime import datetime
from collections import defaultdict
import requests


def parse_ips(input_file, output_dir):
    # Load data
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    with open(input_file, 'r') as file:
        data = json.load(file)

    # Prepare data structures
    accesses_per_day = defaultdict(int)
    unique_accesses_per_day = defaultdict(set)
    location_counts = defaultdict(int)
    city_coordinates = {}

    for entry in data:
        try:
            timestamp = datetime.strptime(entry['timestamp'], "%d/%b/%Y:%H:%M:%S %z")
            day = timestamp.date()  # Aggregate by date
            ip = entry['ip']

            accesses_per_day[day] += 1
            unique_accesses_per_day[day].add(ip)

            # Get location data
            response = requests.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 'success' and result['country'] == 'Germany':
                    city = result['city']
                    location_counts[city] += 1
                    city_coordinates[city] = (result['lat'], result['lon'])
        except Exception as e:
            print(f"Error processing entry {entry}: {e}")

    # Prepare daily and cumulative data
    sorted_days = sorted(accesses_per_day.keys())
    cumulative_accesses = []
    cumulative_unique_users = []

    total_accesses = 0
    unique_users_set = set()

    for day in sorted_days:
        total_accesses += accesses_per_day[day]
        unique_users_set.update(unique_accesses_per_day[day])

        cumulative_accesses.append(total_accesses)
        cumulative_unique_users.append(len(unique_users_set))

    # Prepare JSON data for growth rate and cumulative graphs
    user_growth_data = {
        "data": [
            {
                "type": "scatter",
                "x": [day.isoformat() for day in sorted_days],
                "y": [accesses_per_day[day] for day in sorted_days],
                "mode": "lines+markers",
                "name": "Daily Accesses"
            }
        ],
        "layout": {
            "title": "User Growth (Daily Accesses)",
            "xaxis": {"title": "Date", "tickformat": "%Y-%m-%d"},
            "yaxis": {"title": "Number of Accesses"}
        }
    }

    cumulative_user_growth_data = {
        "data": [
            {
                "type": "scatter",
                "x": [day.isoformat() for day in sorted_days],
                "y": cumulative_accesses,
                "mode": "lines+markers",
                "name": "Cumulative Accesses"
            }
        ],
        "layout": {
            "title": "Cumulative User Growth",
            "xaxis": {"title": "Date", "tickformat": "%Y-%m-%d"},
            "yaxis": {"title": "Cumulative Accesses"}
        }
    }

    unique_accesses_data = {
        "data": [
            {
                "type": "scatter",
                "x": [day.isoformat() for day in sorted_days],
                "y": [len(unique_accesses_per_day[day]) for day in sorted_days],
                "mode": "lines+markers",
                "name": "Unique Daily Users"
            }
        ],
        "layout": {
            "title": "Unique User Growth (Daily)",
            "xaxis": {"title": "Date", "tickformat": "%Y-%m-%d"},
            "yaxis": {"title": "Number of Unique Users"}
        }
    }

    cumulative_unique_user_growth_data = {
        "data": [
            {
                "type": "scatter",
                "x": [day.isoformat() for day in sorted_days],
                "y": cumulative_unique_users,
                "mode": "lines+markers",
                "name": "Cumulative Unique Users"
            }
        ],
        "layout": {
            "title": "Cumulative Unique User Growth",
            "xaxis": {"title": "Date", "tickformat": "%Y-%m-%d"},
            "yaxis": {"title": "Cumulative Unique Users"}
        }
    }

    # Save JSON data
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'MS_user_growth.json'), 'w') as file:
        json.dump(user_growth_data, file, indent=4)
    with open(os.path.join(output_dir, 'MS_unique_accesses.json'), 'w') as file:
        json.dump(unique_accesses_data, file, indent=4)
    with open(os.path.join(output_dir, 'MS_cumulative_user_growth.json'), 'w') as file:
        json.dump(cumulative_user_growth_data, file, indent=4)
    with open(os.path.join(output_dir, 'MS_cumulative_unique_user_growth.json'), 'w') as file:
        json.dump(cumulative_unique_user_growth_data, file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 ip_parsing.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    parse_ips(input_file, output_dir)