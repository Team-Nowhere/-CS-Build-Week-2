import hashlib
import requests
from decouple import config
import sys
import json
from main_functions import cooldown
from uuid import uuid4
from timeit import default_timer as timer
import random
SECRET_TOKEN = config('SECRET_TOKEN')
TOKEN_HEADER = 'Token ' + SECRET_TOKEN
AUTH_HEADER = {'Authorization': TOKEN_HEADER}
base_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/'
bc_url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/'
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
    proof = 0
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
    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof", headers={'Authorization': TOKEN_HEADER})
        data = r.json()
        # print(data)
        new_proof = proof_of_work(data.get('proof'), data.get('difficulty'))
        post_data = {"proof": new_proof}
        print(post_data)
        r = requests.post(url=node + "/mine", json=post_data, headers={'Authorization': TOKEN_HEADER})
        data = r.json()
        cooldown(data)
        print('data', data)
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print('Breaking...')
            break