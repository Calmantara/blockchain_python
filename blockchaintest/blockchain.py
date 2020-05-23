import datetime
import json
import hashlib
import requests


class Blockchain:
    def __init__(self):
        """Constructor"""
        self._chain = []
        self._previous_chain = {}
        self._nodes = []
        self._transactions = []

        self.create_genesis_block()

    def create_genesis_block(self):
        """Create genesis block in the firsttime create blockchain"""
        self.create_block(_message="",
                          _previous_hash=0)

    def create_block(self,  _message: str,
                     _previous_hash: str = 0,
                     _transaction: dict = {}):
        """Create block procedure"""
        block = {
            'block_number': len(self._chain),
            'message': _message,
            'nonce': 0,
            'timestamp': str(datetime.datetime.now()),
            'hash': '',
            'previous_hash': _previous_hash,
            'transaction': _transaction
        }
        # get valid block
        block = self.proof_of_work(_single_block=block)
        # append valid block into blockchain
        self._chain.append(block)

    def get_block_hash(self, _block: dict):
        """Create hash fromcurrent block"""
        _encoded_block = json.dumps(_block, sort_keys=True).encode()
        _encoded_block_hash = hashlib.sha256(_encoded_block).hexdigest()
        return _encoded_block_hash

    def proof_of_work(self, _single_block: dict):
        """proof of work algorithm with formula nonce+1"""
        _nonce = 0
        _proof_status = False
        while(_proof_status == False):
            _single_block['nonce'] = _nonce
            _single_block_hash = str(self.get_block_hash(_block=_single_block))
            print(_single_block_hash)
            if(_single_block_hash[:3] == '000'):
                _proof_status = True
                _single_block['hash'] = _single_block_hash
            _nonce += 1
        return _single_block

    def validate_block(self, _chain: list):
        """To check all blocks in node"""
        _status = True
        for prev_block, current_block in zip(self._chain, self._chain[1:]):
            if(prev_block['hash'] != current_block['previous_hash']):
                _status = False
                return _status
            if(prev_block['hash'][:3] != '000'):
                _status = False
                return _status
        return _status

    def add_transaction(self, sender, receiver, amount):
        """add transaction list"""
        self._transactions.append({'sender': sender,
                                   'receiver': receiver,
                                   'amount': amount})
        return self._transactions[-1]

    def add_node(self, list_of_node: list):
        """Add Node to the network"""
        for node in list_of_node:
            self._nodes.append(node)
        length_node = len(self._nodes)
        if(length_node > 0):
            return "There are %s nodes in the network" % (length_node)
        else:
            return "No connected nodes in the network"

    def replace_chain(self):
        """Replace the longest chain in node"""
        network = self._nodes
        longest_chain = None
        max_length = len(self._chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # replace with longest chain
                if length > max_length and self.validate_block(_chain=chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
