import json
import os
import sys
from datetime import datetime
from collections import defaultdict
import requests


def parse_ips(input_file, output_dir, prefix):
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
    new_locations = set()

    for entry in data:
        try:
            # Clean timestamp and parse
            raw_timestamp = entry['timestamp'].strip("[]")
            timestamp = datetime.strptime(raw_timestamp, "%d/%b/%Y:%H:%M:%S %z")
            day = timestamp.date()  # Aggregate by date
            ip = entry['ip']

            # Update counts for daily and unique users
            accesses_per_day[day] += 1
            unique_accesses_per_day[day].add(ip)
            
            # Fetch geolocation data and handle map updates
            response = requests.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                result = response.json()
                if (
                    result['status'] == 'success'
                    and result.get('city')
                    and result.get('lat')
                    and result.get('lon')
                ):
                    city = result['city']
                    location_counts[city] += 1
                    city_coordinates[city] = (result['lat'], result['lon'])
                elif result['status'] == 'fail' and result.get('message') == 'private range':
                    print(f"Private IP detected (excluded from map): {ip}")
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

    # Logging summary
    print(f"Total new users since last run: {len(unique_users_set)}")
    if new_locations:
        print(f"New locations added to the map: {', '.join(new_locations)}")
    else:
        print("No new locations added to the map.")

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
            "title": f"User Growth: Users accessing the tool daily",
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
            "title": f"Cumulative User Growth ({prefix.capitalize()})",
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
            "title": f"Unique users accessing the tool daily",
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
            "title": f"Cumulative Unique User Growth ({prefix.capitalize()})",
            "xaxis": {"title": "Date", "tickformat": "%Y-%m-%d"},
            "yaxis": {"title": "Cumulative Unique Users"}
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
                    "line": {"color": "darkgray", "width": 0.5},
                },
            }
        ],
        "layout": {
            "title": f"User Distribution ({prefix.capitalize()})",
            "geo": {
                "scope": "world",  # No restriction to Germany
                "projection": {"type": "mercator"},
                "center": {"lat": 51.1657, "lon": 10.4515},  # Centered on Germany
                "showland": True,
                "landcolor": "rgb(217, 217, 217)",
                "showlakes": True,
                "lakecolor": "rgb(255, 255, 255)",
                "subunitwidth": 1,
                "countrywidth": 1,
                "subunitcolor": "rgb(255, 255, 255)",
                "countrycolor": "rgb(255, 255, 255)",
            },
        },
    }

    # Save JSON data
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f'{prefix}_user_growth.json'), 'w') as file:
        json.dump(user_growth_data, file, indent=4)
    with open(os.path.join(output_dir, f'{prefix}_unique_accesses.json'), 'w') as file:
        json.dump(unique_accesses_data, file, indent=4)
    with open(os.path.join(output_dir, f'{prefix}_cumulative_user_growth.json'), 'w') as file:
        json.dump(cumulative_user_growth_data, file, indent=4)
    with open(os.path.join(output_dir, f'{prefix}_cumulative_unique_user_growth.json'), 'w') as file:
        json.dump(cumulative_unique_user_growth_data, file, indent=4)
    with open(os.path.join(output_dir, f'{prefix}_user_distribution.json'), 'w') as file:
        json.dump(user_distribution_data, file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 ip_parsing.py <input_file> <output_dir> <prefix>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    prefix = sys.argv[3]
    parse_ips(input_file, output_dir, prefix)