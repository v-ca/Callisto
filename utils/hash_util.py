import hashlib as _hl  # the underscore is used to indicate that the variable is private and should not be accessed or exported directly.
import json

__all__ = [
    "hash_string_256",
    "hash_block",
]  # this is a list of strings that defines what symbols in a module will be exported when from <module> import * is used on the module. Only these identifiers will be imported from the module when the import * statement is used.


def hash_string_256(string):
    return _hl.sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block["transactions"] = [
        tx.to_dict() for tx in hashable_block["transactions"]
    ]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
