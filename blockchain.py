from hashlib import sha256
from collections import OrderedDict
from urllib.parse import urlparse
import requests
import jsonpickle
import numpy as np
from datetime import datetime
from block import Block

class Blockchain:
    def __init__(self, difficulty):
        '''
        Input: Difficulty as an int.
        Output: Does not return anything.

        The constructor initializes a blockchain object with a defined difficulty for mining its blocks. 
        '''
        self.difficulty = difficulty
        self.chain = []
        self.pending_power_data = []
        self.nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self):
        '''
        Creates the genesis block with empty power data
        '''
        previous_hash = sha256()
        previous_hash.update(''.encode('utf-8'))
        previous_hash = previous_hash.hexdigest()

        # Create genesis block with empty power data
        genesis_data = {
            'timestamp': datetime.now(),
            'voltage_vector': np.zeros(1),  # 1-dimensional zero array
            'current_vector': np.zeros(1),
            'power_vector': np.zeros(1),
            'node_id': 'genesis',
            'metadata': {'type': 'genesis_block'}
        }
        
        genesis_block = Block(1, genesis_data, previous_hash)
        genesis_block.mine(self.difficulty)
        self.chain.append(genesis_block)
        print("\nSuccess: Added Genesis Block to the blockchain.")
        print(genesis_block)

    def register_node(self, node_address):
        '''
        Input: An IP Address of the node on the network. 
        Output: Nothing.

        This method takes in the ip address that a node on the network is using and adds it to the set of nodes 
        recognized by the blockchain. 
        '''
        url = urlparse(node_address) # parse the url 
        self.nodes.add(url.netloc) # add the url to the set of nodes
        print(self.nodes)

    def proof_of_work(self, block, previous = -1):
        '''
        Input: A block object.
        Output: Returns a boolean indicating whether a block has been mined correctly.

        This method checks to see whether the hashid of a block meets the difficulty requirements and 
        has therefore actually been mined. The method also checks to see if the previous hash stored in the 
        block matches the hashid of the most recent block on the chain as a default.  
        '''
        return int(block.hashid, 16) <  2**(256 - self.difficulty) and block.previous_hash == self.chain[previous].hashid # two conditions
    
    def add_to_chain(self, block):
        '''
        Input: A block object. 
        Output: Does not return anything, prints whether the block has been succesfully added to the blockchain. 

        This method checks to see whether the work has been done to mine the block. If so, the block is appended
        to the chain list and a success message is printed out and the block is returned. If not, the block is not added and a 
        failure message is diplayed accordingly and returned. 
        '''
        if self.proof_of_work(block): # checks for proof of work 
            self.chain.append(block) 
            print("\nSuccess: Added block to the blockchain.\n")
            return self.chain[-1]
        print("\nFailure: Did not add block to the blockchain.")
        return "\nFailure: Did not add block to the blockchain."

    def add_power_data(self, voltage_vector, current_vector, power_vector, node_id, metadata=None):
        '''
        Input: Power system vectors and metadata
        Output: None

        Adds power system data to pending data queue
        '''
        power_data = {
            'timestamp': datetime.now(),
            'voltage_vector': np.array(voltage_vector),
            'current_vector': np.array(current_vector),
            'power_vector': np.array(power_vector),
            'node_id': node_id,
            'metadata': metadata or {}
        }
        self.pending_power_data.append(power_data)

    def mine_power_data(self):
        '''
        Mines pending power data into a new block
        '''
        if len(self.pending_power_data) > 0:
            data = self.pending_power_data.pop()
            block = Block(len(self.chain) + 1, data, self.chain[-1].hashid)
            block.mine(self.difficulty)
            result = self.add_to_chain(block)
            return result
        return "No pending power data to mine"

    def validate_chain(self):
        '''
        Input: Nothing.
        Output: Returns a boolean that determines whether the blockchain is valid. 

        This method determines whether the entire blockchain is accurate. It determines this by going 
        through each block in the chain and ensuring that the necessary proof of work has been conducted.
        It checks whether the hash of each block meets the difficulty requirement and also whether its 
        previous hash attribute matches the hashid of the previous block.  
        '''
        block_index = 1
        while block_index < len(self.chain): # goes through each block in the chain starting with the block after the genesis block
            block = self.chain[block_index]
            if not self.proof_of_work(block, block_index - 1): # fails to meet conditions 
                return False
            block_index += 1
        return True # entire chain is valid 
    
    def validate_another_chain(self, chain):
        '''
        Input: A chain of another blockchain. 
        Output: Returns a boolean that determines whether the other chain is valid. 

        This method determines whether another chain is accurate. It determines this by going 
        through each block in the chain and ensuring that the necessary proof of work has been conducted.
        It checks whether the hash of each block meets the difficulty requirement and also whether its 
        previous hash attribute matches the hashid of the previous block.  
        '''
        block_index = 1
        while block_index < len(chain): # goes through each block in the chain starting with the block after the genesis block
            block = chain[block_index]
            result = int(block.hashid, 16) <  2**(256 - self.difficulty) and block.previous_hash == chain[block_index - 1].hashid # checks the two requirements
            if result == False:
                return False
            block_index += 1
        return True # entire chain is valid

    def find_longest_chain(self):
        '''
        Input: Nothing.
        Output: Returns a boolean indicating whether the chain has been replaced by an alternate longer accurate chain. 

        This method implements the consensus algorithm. Suppose another node has a longer chain than ours that is accurate,
        we want to replace our own chain with this longer chain. This method checks the chains of the other nodes in the network
        and replaces our chain if another chain is found that is longer and accurate. True is returned if the replacement takes
        place and False otherwise. 
        '''
        other_nodes = self.nodes
        new_chain = False # indicates whether we adopt a new chain 
        current_length = len(self.chain)

        for node in other_nodes:
            chain_details = requests.get(f'http://{node}/chain_details') # obtain the chain data from the other nodes server
            print(chain_details.status_code)
            if chain_details.status_code == 200:
                chain = jsonpickle.decode(chain_details.json()['Chain']) # have to deserialize since we pass in a complex object to json
                length = chain_details.json()['Length']
            print(length)
            print(self.validate_another_chain(chain))
            if length > current_length and self.validate_another_chain(chain): # check if chain is longer and accurate
                current_length = length
                new_chain = chain
            
        if new_chain != False:
            self.chain = new_chain # update
            return True
        
        return False

    def __str__(self):
        '''
        Input: Nothing. 
        Output: Returns a representation of the blockchain in string format. 

        This special method iterates through the blocks held in the blockchain and appends their string
        representations to a block string. This block string is returned, which displays all the blocks. 
        '''
        block_string = ''
        for i in range(len(self.chain)):
            block_string += f"\n{str(self.chain[i])}" # string of all blocks in the blockchain 
        return block_string

