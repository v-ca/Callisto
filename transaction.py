from collections import OrderedDict
from utils.printable import Printable

class Transaction(Printable):
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return OrderedDict([Í
            ('sender', self.sender),
            ('recipient', self.recipient),
            ('amount', self.amount)
        ])