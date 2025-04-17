from hashlib import sha256
from datetime import datetime 
import numpy as np

class Block:
    def __init__(self, block_number, power_data, previous_hash, nonce = 0):
        '''
        Inputs: 
        - block_number: int
        - power_data: dictionary containing power system vectors
        - previous_hash: hexadecimal number
        - nonce: int (default=0)
        
        Power data structure:
        {
            'timestamp': datetime,
            'voltage_vector': np.array,
            'current_vector': np.array,
            'power_vector': np.array,
            'node_id': str,
            'metadata': dict
        }
        '''
        self.block_number = block_number
        self.power_data = power_data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hashid = sha256()
        self.timestamp = datetime.now()

    def mine(self, difficulty):
        '''
        Modified to handle numpy arrays in power_data by converting them to lists
        before hashing
        '''
        # Convert numpy arrays to lists for hashing
        hashable_data = {
            'timestamp': str(self.power_data['timestamp']),
            'voltage_vector': self.power_data['voltage_vector'].tolist(),
            'current_vector': self.power_data['current_vector'].tolist(),
            'power_vector': self.power_data['power_vector'].tolist(),
            'node_id': self.power_data['node_id'],
            'metadata': self.power_data['metadata']
        }

        self.hashid.update(
            str(self.nonce).encode('utf-8') +
            str(hashable_data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.block_number).encode('utf-8')
        )
        
        while int(self.hashid.hexdigest(), 16) > 2**(256 - difficulty):
            self.nonce += 1
            self.hashid = sha256()
            self.hashid.update(
                str(self.nonce).encode('utf-8') +
                str(hashable_data).encode('utf-8') +
                str(self.previous_hash).encode('utf-8') +
                str(self.timestamp).encode('utf-8') +
                str(self.block_number).encode('utf-8')
            )
        
        self.hashid = self.hashid.hexdigest()  # Now hashid is a string
        return self.hashid

    def __str__(self):
        """
        Enhanced string representation to show actual vector values
        """
        return f"""Block Hash: {self.hashid}
Block Number: {self.block_number}
Node ID: {self.power_data['node_id']}
Timestamp: {self.timestamp}
Voltage Vector: {self.power_data['voltage_vector'].tolist()}
Current Vector: {self.power_data['current_vector'].tolist()}
Power Vector: {self.power_data['power_vector'].tolist()}
Metadata: {self.power_data['metadata']}"""
