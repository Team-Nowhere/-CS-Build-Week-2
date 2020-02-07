import hashlib
from decouple import config
import sys
import json
from main_functions import cooldown
from uuid import uuid4
from timeit import default_timer as timer
import random
from endpoints import *

def proof_of_work(last_proof, difficulty):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """
    start = timer()
    print("Searching for next proof")
    block_string = json.dumps(last_proof, sort_keys=True)
    # print(block_string, last_proof, difficulty)
    proof = random.randint(0, 10000000000)
    while valid_proof(block_string, proof, difficulty) is False:
        proof += 1
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof

def valid_proof(last_hash, proof, difficulty):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?
    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    difficultStr = '0' * difficulty
    guess = f"{last_hash}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # encoded_hash = f"{last_hash}".encode()
    # hash_last_hash = hashlib.sha256(encoded_hash).hexdigest()
    # print(guess_hash, difficultStr)
    return guess_hash[:difficulty] == difficultStr

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = bc_url

    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        last_proof_res = last_proof()
        new_proof = proof_of_work(last_proof_res['proof'], last_proof_res['difficulty'])

        # Check to see if mining with found proof works
        mine_res = mine(new_proof)
        cooldown(mine_res)
        if not mine_res['errors']:
            if mine_res['messages']:
                if 'New Block Forged' in mine_res['messages']:
                    print('''
>!!!!!!!!!!!!!!!!!!!!<
>!!!              !!!<
>!!!  Coin Mined  !!!<
>!!!              !!!<
>!!!!!!!!!!!!!!!!!!!!<
                    ''')
                    break

        else:
            print(mine_res['errors'][0])
            print('Trying again...\n')