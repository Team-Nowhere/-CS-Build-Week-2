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
parser.add_argument('--room')
parser.add_argument('--collect_treasure', default=False)
args = parser.parse_args()

if not args.room:
    print('Please choose room ($ python fast_travel.py --room <room number>)')
else:
    current_room = get_current_room()
    if current_room['errors'] is not None and len(current_room['errors']) > 0:
        print('!!! Cooldown Penalty !!!')
        cooldown(current_room)
        print('Getting current room id...')
        current_room = get_current_room()
        cooldown(current_room)
    else:
        print('Getting current room id...')
        cooldown(current_room)
    
    print('\n== STARTING FAST TRAVEL ==\n')


    fast_travel(current_room['room_id'],
                str(args.room),
                collect_treasure=bool(args.collect_treasure))

    # Comment out if not selling all or praying
    # if args.room is '1':
    #     shop_room = get_current_room()
    #     cooldown(shop_room)
    #     sell_all(shop_room['room_id'])
    # elif args.room in ['22', '374', '461', '492', '499']:
    #     prayer_room = get_current_room()
    #     cooldown(prayer_room)
    #     say_prayer(prayer_room['room_id'])