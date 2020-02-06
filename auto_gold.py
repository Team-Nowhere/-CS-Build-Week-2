from endpoints import *
from main_functions import *
import os
import subprocess
import argparse
import random

"""
Use this file to farm gold.

Make sure you uncomment:

    # if args.room is '1':
    #     shop_room = get_current_room()
    #     cooldown(shop_room)
    #     sell_all(shop_room['room_id'])

in fast_travel.py first!

examples:
python auto_gold.py
python auto_gold.py --gold 200
python auto_gold.py --gold 50000
"""

parser = argparse.ArgumentParser(description='Gold Farm')
parser.add_argument('--gold', default=999999999999)
args = parser.parse_args()

gold = int(args.gold)

os.system('pipenv shell')

status_res = status()

# Cooldown penalty check
if status_res['errors'] is not None and len(status_res['errors']) > 0:
    print('\n!!!! Cooldown Penalty !!!!')
    cooldown(status_res)
    print('Grabbing player gold...')
    current_room = get_current_room()
    cooldown(status_res)
else:
    print('Grabbing player gold...')
    cooldown(status_res)

current_gold = status_res['gold']
gold_goal = current_gold + gold

while current_gold < gold_goal:
    # Update player status
    print('Updating player info...')
    status_res = status()
    strength = status_res['strength']
    encumbrance = status_res['encumbrance']
    current_gold = status_res['gold']
    cooldown(status_res)

    # Check to see if encumbered
    if strength <= encumbrance:
        # Head to shop to sell everything first
        os.system(f'python fast_travel.py --room 1')
    
    # Get random number for room destination: 1 > n > 500
    room_to_go = random.choice(list(range(2, 500)))

    # Get collecting!
    os.system(f'python fast_travel.py --room {room_to_go} --collect_treasure True')
