# Power System Blockchain

A specialized blockchain implementation for power system data that creates a time-stamped series of records using the SHA-256 hashing algorithm. Each block contains power system measurements (voltage, current, and power vectors) and is cryptographically linked to the previous block, ensuring data integrity and immutability.

## Features

- **Secure Data Storage**: Uses SHA-256 hashing to create immutable records
- **Power System Specific**: Designed to store and validate power measurement data
- **Proof of Work**: Mining mechanism ensures computational work for adding new blocks
- **Network Deployment**: Uses Flask for local network deployment
- **Data Validation**: Mathematical verification of blockchain integrity
- **Node Consensus**: Implements longest chain rule for network consensus

## Technical Architecture

### Block Structure

Each block contains:

- Block number
- Timestamp
- Power system measurements (voltage, current, power vectors)
- Node ID
- Previous block's hash
- Current block's hash
- Nonce (for proof of work)
- Metadata (location, measurement type, sampling rate)

### Blockchain Features

- Configurable mining difficulty
- Pending transactions queue
- Block validation
- Chain validation
- Network consensus mechanism

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd power-system-blockchain
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the blockchain node:

```bash
python api.py
```

This will start the Flask server on `http://localhost:5000`

2. Interact with the blockchain using the following API endpoints:

### Submit Power Data

```bash
curl -X POST http://localhost:5000/submit_data \
-H "Content-Type: application/json" \
-d '{
    "voltage_vector": [230.5, 231.2, 230.8],
    "current_vector": [10.2, 10.1, 10.3],
    "power_vector": [2351.1, 2335.12, 2377.24],
    "node_id": "station_001",
    "metadata": {
        "location": "Grid Section A",
        "measurement_type": "three_phase",
        "sampling_rate": "1000Hz"
    }
}'
```

### Mine a Block

```bash
curl -X GET http://localhost:5000/mine
```

### Get the Full Chain

```bash
curl -X GET http://localhost:5000/chain
```

### Register a New Node

```bash
curl -X POST http://localhost:5000/register_node \
-H "Content-Type: application/json" \
-d '{"node_address": "http://localhost:5001"}'
```

### Update Chain (Consensus)

```bash
curl -X GET http://localhost:5000/nodes/resolve
```

## Project Structure

```
power-system-blockchain/
├── api.py              # Flask API endpoints
├── block.py            # Block class implementation
├── blockchain.py       # Blockchain class implementation
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Data Format

Power system data should be submitted in the following format:

```json
{
    "voltage_vector": [float, float, float],  // Three-phase voltage measurements
    "current_vector": [float, float, float],  // Three-phase current measurements
    "power_vector": [float, float, float],    // Three-phase power measurements
    "node_id": "string",                      // Unique identifier for the power station
    "metadata": {
        "location": "string",
        "measurement_type": "string",
        "sampling_rate": "string"
    }
}
```

## Development

- Python version: 3.8+
- Key dependencies:
  - Flask
  - NumPy
  - Requests

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Testing with Sample Power Data

### Using load_power_data.py

The project includes a utility script `load_power_data.py` that allows you to bulk load power system measurements from a CSV file into the blockchain.

1. First, ensure your CSV file follows this structure:

```csv
timestamp,node_id,voltage_1,voltage_2,voltage_3,current_1,current_2,current_3,power_1,power_2,power_3,location,measurement_type,sampling_rate
2023-01-01 00:00:00,station_001,230.5,231.2,230.8,10.2,10.1,10.3,2351.1,2335.12,2377.24,Grid Section A,three_phase,1000Hz
```

2. Start the blockchain node:

```bash
python api.py
```

3. In a separate terminal, run the data loading script:

```bash
python load_power_data.py
```

The script will:

- Prompt you to confirm the blockchain API is running
- Allow you to specify a custom API URL (default: http://localhost:5000)
- Read data from `power_data.csv`
- Submit each measurement to the blockchain
- Automatically trigger mining for each submission
- Display progress and confirmation messages

### Sample Data Format

Your CSV file should contain the following columns:

- `timestamp`: Measurement timestamp
- `node_id`: Unique identifier for the power station
- `voltage_1,voltage_2,voltage_3`: Three-phase voltage measurements
- `current_1,current_2,current_3`: Three-phase current measurements
- `power_1,power_2,power_3`: Three-phase power measurements
- `location`: Physical location of the measurement
- `measurement_type`: Type of measurement (e.g., three_phase)
- `sampling_rate`: Data sampling rate

### Example Usage

1. Create a sample CSV file named `power_data.csv` with your measurements
2. Start the blockchain:

```bash
python api.py
```

3. In a new terminal, activate the virtual environment:

```bash
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

4. Run the loading script:

```bash
python load_power_data.py
```

5. Monitor the output for successful submissions and mining operations

### Error Handling

The script includes error handling for:

- Missing or invalid CSV files
- Network connection issues
- Invalid data formats
- Server errors

If an error occurs during data submission, the script will:

- Display an error message
- Continue with the next record
- Maintain a log of failed submissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)
