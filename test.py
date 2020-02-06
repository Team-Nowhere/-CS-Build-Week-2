from main_functions import *
from endpoints import *
import argparse
"""
Use this file to travel to a room

If you want to pick up treasure along the way
add the --collect_treasure flag

default for treasure is False

-- Dashing -- 
If you have dash you will auto dash

If you are collecting treasure, you will not dash
-------------

-- Recalling -- 
If you have recall and fast_travel to room 0, you will use recall

If you are collecting treasure, you will not recall
---------------

examples:
python fast_travel.py --room 80
python fast_travel.py --room 1
python fast_travel.py --room 12 --collect_treasure True
"""

parser = argparse.ArgumentParser(description='Fast travel')
parser.add_argument('--coin')
parser.add_argument('--abilities', default=None, nargs='+')
args = parser.parse_args()

print(args.coin)
print(args.abilities)
print(type(args.abilities))