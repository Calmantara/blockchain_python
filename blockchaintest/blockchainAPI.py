from blockchain import Blockchain
from flask import Flask, jsonify
from uuid import uuid4

# initiate flask
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# initiate blockchain
blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    blockchain.create_block(_message='Hello World',
                            _previous_hash=blockchain._chain[-1]['hash'])
    return jsonify(blockchain._chain[-1]), 200

# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain._chain,
                'length': len(blockchain._chain)}
    return jsonify(response), 200


@app.route('/validate_chain', methods=['GET'])
def validate_chain():
    response = {'valid_status': blockchain.validate_block()}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.validate_block(_chain=blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {
            'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


# Running the app
app.run(host='127.0.0.1', port=5000, debug=True)
