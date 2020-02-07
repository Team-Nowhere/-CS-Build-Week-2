from endpoints import *
from main_functions import *
import os
import subprocess
import argparse
import time

parser = argparse.ArgumentParser(description='Snitch Locator')
parser.add_argument('--snitches')
args = parser.parse_args()

want = int(args.snitches)

with open('traversal_graph.json', 'r') as map_file:
    map_graph = json.load(map_file)

map_graph = {int(k):v for k,v in map_graph.items()}

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

if int(current_room["room_id"]) != 555:
    adv_fast_travel(current_room['room_id'], 555, abilities=['fly', 'dash', 'recall', 'warp'], map_graph=map_graph)


def well_number():
    data = examine('Well')
    time.sleep(data['cooldown'])
    desc = data['description']

    desc = desc.strip('You see a faint pattern in the water...\n\n').split('\n')

    with open('well_data.txt', 'w') as data:
        for i in desc:
            data.write(f'{i}\n')

    time.sleep(2)
    cmd = ['python', 'ls8.py', 'well_data.txt']


    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    output = output.decode('utf-8').replace('\n', '').split(' ')[-3]
    snitch_room = output.rstrip('HALTING')

    return snitch_room, data




captured = 0
wait_for_snitch = False

tries = 0
while captured < want:
    # Examine the well
    start_snitch, data = well_number()
    new_num = start_snitch
    camp_wait = 0

    print('\nCamping for 60 iterations')

    while new_num == start_snitch and camp_wait < 60:
        new_num, data = well_number()
        camp_wait += 1

    tries += 1
    print(f'\nSnitch located in room {new_num}\n')

    adv_fast_travel(555, new_num, abilities=['fly', 'dash', 'recall', 'warp'], map_graph=map_graph)

    take_res = take('golden snitch')
    cooldown(take_res)
    if not take_res['errors']:
        if take_res['messages']:
            if 'warmth' in take_res['messages'][0]:
                print('''
>!!!!!!!!!!!!!!!!!!!!!!!<
>!!!                 !!!<
>!!! Snitch Captured !!!<
>!!!                 !!!<
>!!!!!!!!!!!!!!!!!!!!!!!<
                ''')

                captured += 1
            else:
                print('\nThere is no snitch here\n')


    print(f'\nSnitches Captured: {captured} out of {tries}\n')

    adv_fast_travel(int(new_num), 555, abilities=['fly', 'dash', 'recall', 'warp'], map_graph=map_graph)