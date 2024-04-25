from functools import reduce
import hashlib as hl
from collections import OrderedDict
import json
import pickle

from utils.hash_util import hash_string_256, hash_block
from utils.verification import Verification
from block import Block
from transaction import Transaction


MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, "", [], 100, 0)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id
        self.load_data()

    @property
    def chain(self):
        """
        The property decorator is used to access the private chain attribute
        without the need to call the get_chain method. This creates a read-only copy of the chain attribute.
        """
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        """
        The setter method is used to set the chain attribute to a new value as the 'setter' method. This is the same as self.__chain = val
        and is used to set the chain attribute to a new value.
        """
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                save_data = [
                    block.__dict__
                    for block in [
                        Block(
                            block_el.previous_hash,
                            block_el.index,
                            [tx.__dict__ for tx in block_el.transactions],
                            block_el.proof,
                            block_el.timestamp,
                        )
                        for block_el in self.__chain
                    ]
                ]
                f.write(json.dumps(save_data))
                f.write("\n")
                save_transactions = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(save_transactions))
        except IOError:
            print("Saving failed!")

    def load_data(self):
        try:
            with open("blockchain.txt", mode="r") as f:
                file_content = f.readlines()

                blockchain = json.loads(file_content[0][:-1])

                updated_blockchain = []

                for block in blockchain:
                    converted_tx = [
                        Transaction(tx["sender"], tx["recipient"], tx["amount"])
                        for tx in block["transactions"]
                    ]
                    updated_block = Block(
                        block["previous_hash"],
                        block["index"],
                        converted_tx,
                        block["proof"],
                        block["timestamp"],
                    )
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain  # This is a property setter method that sets the chain attribute to the updated_blockchain. This is the same as self.__chain = updated_blockchain
                self.__open_transactions = json.loads(file_content[1])

                updated_transactions = []
                for tx in self.__open_transactions:
                    updated_transaction = Transaction(
                        tx["sender"], tx["recipient"], tx["amount"]
                    )
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            print("Handled exception...")

    def get_last_blockchain_value(self):
        """
        We use __chain[-1] to get the last element of the list. This is the same as
        using __chain[len(__chain) - 1]. The -1 index is a shortcut to get the last
        element of a list. If the list is empty, it will return an IndexError.
        """
        if len(self.__chain) < 1:
            return None

        return self.__chain[-1]

    def get_balance(self):
        participant = self.hosting_node

        tx_sender = [
            [tx.amount for tx in block.transactions if tx.sender == participant]
            for block in self.__chain
        ]

        open_tx_sender = [
            tx.amount for tx in self.__open_transactions if tx.sender == participant
        ]

        tx_sender.append(open_tx_sender)

        amount_sent = reduce(
            lambda tx_sum, tx_amt: (
                tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0
            ),
            tx_sender,
            0,
        )

        tx_recipient = [
            [tx.amount for tx in block.transactions if tx.recipient == participant]
            for block in self.__chain
        ]

        amount_received = reduce(
            lambda tx_sum, tx_amt: (
                tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0
            ),
            tx_recipient,
            0,
        )

        return amount_received - amount_sent

    def add_transaction(self, recipient, sender, amount=1.0):
        if self.hosting_node == None:
            return False

        transaction = Transaction(sender, recipient, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        if self.hosting_node == None:
            return False

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        reward_transaction = Transaction("MINING", self.hosting_node, MINING_REWARD)

        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)

        block = Block(hashed_block, len(self.__chain), copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)

        proof = 0

        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1

        return proof
