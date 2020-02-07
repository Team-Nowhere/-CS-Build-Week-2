from endpoints import *
from main_functions import *
import os

"""
Script for rerolling for exquisites
"""

current_room = get_current_room()
cooldown(current_room)

if int(current_room['room_id']) != 495:
    os.system('python fast_travel.py --room 495')

found_exq = False

while found_exq == False:
    reroll_item = None
    # Get an item
    player_status = status()
    cooldown(player_status)

    if player_status['inventory']:
        for item in player_status['inventory']:
            if 'exquisite' not in item:
                reroll_item = item
                break
    else:
        print('You need an item to transmog')
        break

    if reroll_item == None:
        print('No non-exquisite items available for reroll')
        break

    # Get player balance
    balance_res = get_balance()
    cooldown(balance_res)

    balance = int(balance_res['messages'][0].split(' ')[5].rstrip('\.0'))

    print('Balance: ', balance)

    if balance > 0:
        trans_res = transmogrify(reroll_item)
        cooldown(trans_res)

    if trans_res['errors']:
        print(trans_res['errors'][0])
        break

    new_tier = trans_res['messages'][0].strip('!').split(' ')[-2]
    print(trans_res['messages'][0])

    if 'exquisite' == new_tier:
        print('\nFOUND EXQUISITE ITEM\n')
        print(new_item)
        break

    
