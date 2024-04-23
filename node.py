from uuid import uuid4

from printable import Printable
from verification import Verification
from blockchain import Blockchain


class Node(Printable):
    def __init__(self, data=None):
        # self.id = str(uuid4())
        self.id = "Vincent"
        self.blockchain = Blockchain(self.id)
        self.data = data
        self.next = None

    def get_user_input(self):
        return input("Your choice: ")

    def get_transaction_value(self):
        tx_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Enter your transaction amount: "))

        return tx_recipient, tx_amount

    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print("\nOutputting Block")
            print(block)
        else:
            print("-" * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("\nChoose an option")
            print("1: Add a new transaction value")
            print("2: Output the blockchain blocks")
            print("3: Mine a new block")
            print("4: Check transaction validity")
            print("q: Quit\n")

            user_choice = self.get_user_input()

            if user_choice == "1":
                recipient, amount = self.get_transaction_value()
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Transaction added!")
                else:
                    print("Transaction failed!")
                print(self.blockchain.open_transactions)

            elif user_choice == "2":
                self.print_blockchain_elements()

            elif user_choice == "3":
                self.blockchain.mine_block()

            elif user_choice == "4":
                verifier = Verification()
                if verifier.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print("\nAll transactions are valid!\n")
                else:
                    print("\nThere are invalid transactions!\n")

            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("\nInvalid input, please pick a value from the list!")
            verifier = Verification()
            if not verifier.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("\nInvalid blockchain!\n")
                break
            print(f"\nBalance of {self.id}: {self.blockchain.get_balance():6.6f}")
        else:
            print("\nDone!\n")

node = Node()
node.listen_for_input()