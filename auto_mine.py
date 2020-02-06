import os
import argparse
from endpoints import *
from main_functions import *
import time
import subprocess

os.system('pipenv shell')


parser = argparse.ArgumentParser(description='Auto Miner')
parser.add_argument('--coin')
args = parser.parse_args()

coins_to_mine = int(args.coin)
coins_mined = 0

current_room = get_current_room()
cooldown(current_room)

if int(current_room['room_id']) > 499:
    warp_res = warp()
    cooldown(warp_res)

while coins_mined < coins_to_mine:

    # Travel to well
    os.system('python fast_travel.py --room 55')

    # Get Message
    print('Getting Well Data...')
    well_data = examine('Well')
    cooldown(well_data)

    desc = well_data['description']

    desc = desc.strip('You see a faint pattern in the water...\n\n').split('\n')

    with open('well_data.txt', 'w') as well_data:
        for i in desc:
            well_data.write(f'{i}\n')

    print('Updating well_data.txt...')
    time.sleep(2)
    cmd = ['python', 'ls8.py', 'well_data.txt']

    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    output = output.split('\n')
    mining_room = ''
    for i in output:
        try:
            int(i)
            mining_room += i
        except:
            continue
    
    print(f'Traveling to room {mining_room} to mine')
    os.system(f'python fast_travel.py --room {mining_room}')

    os.system('python mine.py')

    coins_mined += 1

balance = get_balance()
cooldown(balance)
balance_message = balance['messages'][0]
print(f'\n{balance_message}\n')

