import json
import pandas as pd

def process_json_data(file_path):
    # Read JSON data from file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Create DataFrames for each plot
    dataframes = {}
    for plot_name, plot_data in data.items():
        df = pd.DataFrame(plot_data)
        dataframes[plot_name] = df
    
    return dataframes

if __name__ == "__main__":
    file_path = 'data/user_growth.json'
    dataframes = process_json_data(file_path)
    
    # Save DataFrames to a global dictionary or any other storage as needed
    for name, df in dataframes.items():
        df.to_json(f'data/{name}.json', orient='split')
