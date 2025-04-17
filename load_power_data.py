import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime

def load_and_submit_power_data(csv_file, api_url='http://localhost:5000'):
    """
    Load power data from CSV and submit to blockchain
    """
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Process each row
    for _, row in df.iterrows():
        # Create voltage, current and power vectors
        voltage_vector = np.array([
            float(row['voltage_1']),
            float(row['voltage_2']),
            float(row['voltage_3'])
        ])
        
        current_vector = np.array([
            float(row['current_1']),
            float(row['current_2']),
            float(row['current_3'])
        ])
        
        power_vector = np.array([
            float(row['power_1']),
            float(row['power_2']),
            float(row['power_3'])
        ])

        # Prepare metadata
        metadata = {
            'location': row['location'],
            'measurement_type': row['measurement_type'],
            'sampling_rate': row['sampling_rate'],
            'timestamp': row['timestamp']
        }

        # Prepare data payload
        data = {
            'voltage_vector': voltage_vector.tolist(),
            'current_vector': current_vector.tolist(),
            'power_vector': power_vector.tolist(),
            'node_id': row['node_id'],
            'metadata': metadata
        }

        try:
            # Submit power data
            response = requests.post(f'{api_url}/new_power_data', json=data)
            print(f"Submitted data for {row['timestamp']}: {response.text}")

            if response.status_code == 201:
                # Mine the block
                mine_response = requests.get(f'{api_url}/mine')
                print(f"Mining result: {mine_response.text}")
            
            # Add a small delay to prevent overwhelming the server
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Error submitting data: {e}")

def main():
    # Make sure the blockchain API is running first
    print("Ensure the blockchain API (api.py) is running before proceeding.")
    input("Press Enter to continue...")

    csv_file = 'power_data.csv'
    
    # Allow user to specify different API URL if needed
    api_url = input("Enter API URL (press Enter for default 'http://localhost:5000'): ")
    if not api_url:
        api_url = 'http://localhost:5000'

    print(f"\nLoading and submitting power data from {csv_file}")
    print(f"Using API endpoint: {api_url}")
    
    load_and_submit_power_data(csv_file, api_url)

if __name__ == "__main__":
    main()