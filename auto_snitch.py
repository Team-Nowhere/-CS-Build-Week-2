from endpoints import *
from main_functions import *
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Snitch Locator')
parser.add_argument('--snitches')
args = parser.parse_args()

want = int(args.snitches)

os.system('pipenv shell')

current_room = get_current_room()
cooldown(current_room)

if int(current_room["room_id"]) < 500:
    print('>>>>>>> Warping to underworld')
    warp_res = warp()
    cooldown(warp_res)

if int(current_room["room_id"]) != 555:
    os.system('python fast_travel.py --room 555')


def well_number():
    data = examine('Well')
    cooldown(data)
    desc = data['description']

    desc = desc.strip('You see a faint pattern in the water...\n\n').split('\n')

    with open('well_data.txt', 'w') as data:
        for i in desc:
            data.write(f'{i}\n')

    print('Updating well_data.txt...')
    time.sleep(2)
    cmd = ['python', 'ls8.py', 'well_data.txt']


    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    output = output.split('\n')
    snitch_room = ''

    for i in output:
        try:
            int(i)
            snitch_room += i
        except:
            continue

    print('Snitch Room: ', snitch_room)

    return snitch_room, data


captured = 0
wait_for_snitch = False
while captured < want:
    # Examine the well
    start_snitch, data = well_number()
    new_num = start_snitch

    if wait_for_snitch == True:
        while new_num == start_snitch:
            new_num, data = well_number()

    os.system(f'python fast_travel.py --room {new_num}')

    current_room = get_current_room()
    cooldown(current_room)
    print(current_room['items'])
    if current_room['items']:
        for i in current_room['items']:
            if i.upper() == 'GOLDEN SNITCH':
                take_res = take(i)
                cooldown(take_res)
                if 'warmth' in take_res['messages'][0]:
                    print('\n!!!! Caputured Snitch !!!!')
                    captured += 1
                    print(f'Snitches Captured: {captured}\n')
                    wait_for_snitch = False
                else:
                    wait_for_snitch = True
                    print('\nNot Captured')
                    print(take_res['messages'][0])

    res = recall()
    cooldown(res)
    res = warp()
    cooldown(warp)

    os.system(f'python fast_travel.py --room 555')



