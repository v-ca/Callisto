from uuid import uuid4

from utils.printable import Printable
from utils.verification import Verification
from blockchain import Blockchain
from wallet import Wallet


class Node(Printable):
    def __init__(self, data=None):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
        self.data = data
        self.next = None

    def get_user_input(self):
        return input("Your choice: ")

    def get_transaction_value(self):
        tx_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Enter your transaction amount: "))
        if tx_amount < 0 or tx_amount == "":
            print("Amount set to 0.")
            tx_amount = 0

        return tx_recipient, tx_amount

    def print_blockchain_elements(self):
        for (
            block
        ) in (
            self.blockchain.chain
        ):  # we don't need a getter method because the chain is public using the @property decorator
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
            print("5: Create wallet")
            print("6: Load wallet")
            print("q: Quit\n")

            user_choice = self.get_user_input()

            if user_choice == "1":
                recipient, amount = self.get_transaction_value()
                if self.blockchain.add_transaction(
                    recipient, self.wallet.public_key, amount=amount
                ):
                    print("Transaction added!")
                else:
                    print("Transaction failed!")
                print(self.blockchain.get_open_transactions())

            elif user_choice == "2":
                self.print_blockchain_elements()

            elif user_choice == "3":
                if not self.blockchain.mine_block():
                    print("\nMining failed. Got no wallet?")

            elif user_choice == "4":
                # verifier = Verification() # This is not needed because the method is a class method
                if Verification.verify_transactions(
                    self.blockchain.get_open_transactions(), self.blockchain.get_balance
                ):
                    print("\nAll transactions are valid!\n")
                else:
                    print("\nThere are invalid transactions!\n")

            elif user_choice == "5":
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
                print(f"\nWallet created!\n")

            elif user_choice == "6":
                self.wallet = Wallet()
                print(f"\nNew wallet loaded!\n")

            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("\nInvalid input, please pick a value from the list!")
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("\nInvalid blockchain!\n")
                break
            print(
                f"\nBalance of {self.wallet.public_key}: {self.blockchain.get_balance():6.6f}"
            )
        else:
            print("\nDone!\n")


if __name__ == "__main__":
    node = Node()
    node.listen_for_input()
