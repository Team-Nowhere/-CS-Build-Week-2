from endpoints import *
from main_functions import *
import os
import subprocess
import argparse
import random

"""
Use this file to play automatically.

examples:
python auto_play.py
python auto_play.py --plays 20
python auto_play.py --plays 9000
"""

parser = argparse.ArgumentParser(description='Auto Play')
parser.add_argument('--plays', default=999999999999)
args = parser.parse_args()

plays = int(args.plays)

os.system('pipenv shell')

status_res = status()

# Cooldown penalty check
if status_res['errors'] is not None and len(status_res['errors']) > 0:
    print('\n!!!! Cooldown Penalty !!!!')
    cooldown(status_res)
    print('Grabbing player info...')
    current_room = get_current_room()
    cooldown(status_res)
else:
    print('Grabbing player info...')
    cooldown(status_res)

play_counter = 0

play_odds = dict()

# populate odds
for i in range(0, 29):
    play_odds[i] = 'gold'
for i in range(30, 59):
    play_odds[i] = 'coin'
for i in range(60, 89):
    play_odds[i] = 'snitch'
for i in range(90, 101):
    play_odds[i] = 'transmogrify'

while play_counter != plays:
    # grab user info
    print('Updating player info...')
    status_res = status()
    cooldown(status_res)

    # let's just make sure the person isn't encumbered, otherwise sell everything
    if status_res['encumbrance'] >= status_res['strength']:
        print('\n>>>>>>>>>> Going to get rid of some baggage!\n')
        os.system(f'python fast_travel.py --room 1')

    # randomly choose an action
    lets_do = random.randint(0, 101)

    # execute that action
    if play_odds[lets_do] == 'gold':
        random_num = random.randint(1000, 10001)
        print('\n>>>>>>>>>> Going to loot some treasure!')
        print(f'>>>>>>>>>> Worth {random_num} gold\n')
        os.system(f'python auto_gold.py --gold {random_num}')
    elif play_odds[lets_do] == 'coin':
        random_num = random.randint(1, 16)
        print('\n>>>>>>>>>> Going to the mines!')
        print(f'>>>>>>>>>> Mining {random_num} coins\n')
        os.system(f'python auto_mine.py --coin {random_num}')
    elif play_odds[lets_do] == 'snitch':
        random_num = random.randint(1, 16)
        print('\n>>>>>>>>>> Going to become a wizard!')
        print(f'>>>>>>>>>> Getting {random_num} snitches\n')
        os.system(f'python auto_snitch.py --snitches {random_num}')
    elif play_odds[lets_do] == 'transmogrify':
        print('\n>>>>>>>>>> Going to roll for exquisite gear!\n')
        os.system(f'python reroll.py')

    # let's do it again
    play_counter += 1
