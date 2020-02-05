from main_functions import *
from endpoints import *
import argparse
"""
Use this file to travel to a room

If you want to pick up treasure along the way
add the --stop_treasure flag

default for treasure is False

examples:
python fast_travel.py --room 80
python fast_travel.py --room 1
python fast_travel.py --room 12 --stop_treasure True
"""
parser = argparse.ArgumentParser(description='Fast travel')
parser.add_argument('--room')
parser.add_argument('--stop_treasure', default=False)
args = parser.parse_args()
if not args.room:
    print('Please choose room ($ python fast_travel.py --room <room number>)')
else:
    current_room = get_current_room()
    cooldown(current_room)

    fast_travel(current_room['room_id'],
                str(args.room),
                stop_treasure=bool(args.stop_treasure))

