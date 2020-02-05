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

Points of Interest:
    0 A brightly lit room (Starting point)
    1 Shop
    22 The Peak of Mt. Holloway (Pray here)
    55 Wishing Well (Mine quest start)
    374 Fully Shrine (Pray here)
    461 Linh's Shrine (Pray here)
    467 Pirate Ry's (Name Change)
    486 Arron's Athenaeum (Leaderboard)
    492 Sandofsky's Sanctum (Pray here)
    495 The Transmogriphier (Spend Lambda coins here for powerful stuff)
    499 Glasowyn's Grave (Pray here)
"""
parser = argparse.ArgumentParser(description='Fast travel')
parser.add_argument('--room')
parser.add_argument('--stop_treasure', default=False)
args = parser.parse_args()
if not args.room:
    print('Please choose room ($ python fast_travel.py --room <room number>)')
else:
    print('Grabbing room data...')
    current_room = get_current_room()
    cooldown(current_room)

    fast_travel(current_room['room_id'],
                str(args.room),
                stop_treasure=bool(args.stop_treasure))

    # Comment out if not selling
    if args.room is '1':
        shop_room = get_current_room()
        cooldown(shop_room)
        sell_all(shop_room['room_id'])
    elif args.room in ['22', '374', '461', '492', '499']:
        prayer_room = get_current_room()
        cooldown(prayer_room)
        say_prayer(prayer_room['room_id'])
