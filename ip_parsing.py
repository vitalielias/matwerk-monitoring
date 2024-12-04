import json
import os
import sys
from datetime import datetime
from collections import defaultdict
import requests


def parse_ips(input_file, output_dir, service_name):
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

            # Update user counts
            accesses_per_day[day] += 1
            unique_accesses_per_day[day].add(ip)

            # Fetch geolocation data
            response = requests.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 'success' and result.get('city') and result.get('lat') and result.get('lon'):
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

    # Generate output JSON files
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{service_name}_user_growth.json"), 'w') as file:
        json.dump({
            "data": [{"x": list(map(str, sorted_days)), "y": list(accesses_per_day.values()), "type": "scatter"}],
            "layout": {"title": f"{service_name.capitalize()} Daily Growth"}
        }, file)
