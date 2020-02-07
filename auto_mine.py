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

# Cooldown penalty check
if current_room['errors'] is not None and len(current_room['errors']) > 0:
    print('\n!!!! Cooldown Penalty !!!!')
    cooldown(current_room)
    print('Getting current room id...')
    current_room = get_current_room()
    cooldown(current_room)
else:
    print('Getting current room id...')
    cooldown(current_room)

status_res = status()
cooldown(status_res)



while coins_mined < coins_to_mine:

    # Travel to well
    run_script = 'python fast_travel.py --room 55'
    if status_res['abilities']:
        run_script += ' --abilities'
        for ability in status_res['abilities']:
            run_script += f' {ability}'
    
    os.system(run_script)

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

    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    output = output.decode('utf-8').replace('\n', '').split(' ')[-3]
    mining_room = output.rstrip('HALTING')
    
    print(f'\nTraveling to room {mining_room} to mine\n')

    run_script = f'python fast_travel.py --room {mining_room}'
    if status_res['abilities']:
        run_script += ' --abilities'
        for ability in status_res['abilities']:
            run_script += f' {ability}'
    
    os.system(run_script)

    os.system('python mine.py')

    coins_mined += 1

balance = get_balance()
cooldown(balance)
balance_message = balance['messages'][0]
print(f'\n{balance_message}\n')

