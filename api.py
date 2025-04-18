from uuid import uuid4
from flask import Flask, request
import json
import jsonpickle
import numpy as np
from blockchain import Blockchain
from block import Block

app = Flask(__name__)

blockchain = Blockchain(20) # constructs a blockchain with 20 difficulty
blockchain_node = str(uuid4()).replace('-', '') # generates a unique universal identifier that identifies the node

@app.route('/')
def welcome():
    '''
    Welcome message that is shown upon connection to the server. 
    '''
    return "Welcome to the blockchain.\nYou can use http requests to view the current blockchain, submit transactions, and mine blocks."


@app.route('/new_power_data', methods=['POST'])
def new_power_data():
    '''
    Endpoint to submit new power system data
    '''
    data = request.get_json()
    required_fields = ['voltage_vector', 'current_vector', 'power_vector', 'node_id']
    
    if not all(field in data for field in required_fields):
        return 'Failure: Missing required fields', 400
    
    try:
        blockchain.add_power_data(
            voltage_vector=np.array(data['voltage_vector']),
            current_vector=np.array(data['current_vector']),
            power_vector=np.array(data['power_vector']),
            node_id=data['node_id'],
            metadata=data.get('metadata', {})
        )
        return "Success: Power data ready to be added to the blockchain.", 201
    except Exception as e:
        return f"Failure: {str(e)}", 400


@app.route('/mine', methods=['GET'])
def mine():
    '''
    Mines pending power data into a new block
    '''
    result = blockchain.mine_power_data()
    if type(result) == Block:
        return str(result), 200
    else:
        return "Failure: Did not mine the blockchain.", 400


@app.route('/chain', methods = ['GET'])
def chain():
    '''
    This endpoint displays the entire blockchain.
    '''
    return str(blockchain) # string representation of object


@app.route('/chain_details', methods = ['GET'])
def chain_details():
    '''
    This endpoint returns the current chain of the blockchain as well as its length. 
    '''
    chain = jsonpickle.encode(blockchain.chain) # chain is serialized to json because it is a complex object that needs to be transferred
    length = len(blockchain.chain)
    result = {'Chain': chain, 'Length': length}
    return result, 200


@app.route('/add_nodes', methods = ['POST'])
def add_nodes():
    '''
    This endpoint collects a node url from the client and proceeds to add it to the set of nodes that is 
    recognized by the blockchain. 
    '''
    result = request.get_json()
    nodes = result["Nodes"]
    if len(nodes) == 0: # ensures that a node has been submitted 
        return "Failure: Please enter a list of nodes", 400
    for node in nodes:
        blockchain.register_node(node) # the node is registered by the blockchain 
    return "Success: Added another node on the network", 201

@app.route('/consensus', methods = ['GET'])
def consensus():
    '''
    This endpoint looks at all the chains of all the other nodes and proceeds to replace the current blockchain of the
    client, if a longer and accurate alternate blockchain is found. 
    '''
    new_chain = blockchain.find_longest_chain() # looks for an alternate chain that is superior
    if new_chain:
        return "Chain was replaced by another longer chain.", 201
    else:
        return "Chain was not replaced. Current chain is the longest.", 201

if __name__ == "__main__":
    answer = input("Please enter the node that you want to use on the network: ")
    if answer == "1":
        app.run(port= 5000) # allows for multiple nodes on the network and objective of consensus
    if answer == "2":
        app.run(port=5001)
