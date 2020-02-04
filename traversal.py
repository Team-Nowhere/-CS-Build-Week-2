import time
import json
import random
from main_functions import *
from endpoints import *

rev_dir = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

# Open existing map
with open('traversal_graph.json', 'r') as map_file:
    mapped_area = json.load(map_file) # Use this to roam
    # Make sure the keys come back as integers and not string
    mapped_area = {int(k):v for k,v in mapped_area.items()}

init_res = get_current_room() # Init api call
cooldown(init_res)
current_room_id = init_res['room_id']
current_room_title = init_res['title']
current_room_exits = init_res['exits']
current_room_messages = init_res['messages']
prev_room_id = 0

# Only used on first time boot up or if program ends without entering new room info
if init_res['room_id'] not in mapped_area:
    data = {}
    data['title'] = init_res['title']
    for direction in init_res['exits']:
        data[f'{direction}'] = '?'
    mapped_area[init_res['room_id']] = data

    # Save updated mapped_area
    print('========== Updating map_file...')
    with open('traversal_graph.json', 'w') as map_file:
        json.dump(mapped_area, map_file, indent=4)

while len(mapped_area) != 500:
    crd = dict() # current_room_dictonary

    # Check to see if player has explored the room already
    if current_room_id not in mapped_area:
        print(f'!!!!!!!!!! Room {current_room_id} is new!')
        data = {}
        data['title'] = current_room_title
        for direction in current_room_exits:
            data[f'{direction}'] = '?'
        mapped_area[current_room_id] = data

        # Update direction coming from
        if 'north' in current_room_messages:
            mapped_area[current_room_id]['s'] = prev_room_id
        elif 'south' in current_room_messages:
            mapped_area[current_room_id]['n'] = prev_room_id
        elif 'east' in current_room_messages:
            mapped_area[current_room_id]['w'] = prev_room_id
        elif 'west' in current_room_messages:
            mapped_area[current_room_id]['e'] = prev_room_id
        
        # Save updated mapped_area
        print('========== Updating map_file...')
        with open('traversal_graph.json', 'w') as map_file:
            json.dump(mapped_area, map_file, indent=4)

        # Set data from overall dict into crd
        crd = mapped_area[current_room_id]
    # If it already exists, grab data from overall dictionary
    else:
        print(f'!!!!!!!!!! Currently in room {current_room_id}')
        crd = mapped_area[current_room_id]

    # Check to see if there are still unknown rooms connected
    unknown_exits = list()
    for direction in crd:
        if crd[direction] == '?':
            unknown_exits.append(direction)

    # If unknowns exist, go in one of the directions
    if len(unknown_exits) != 0:
        # Randomly shuffle since we don't know where we're going anyway
        random.shuffle(unknown_exits)
        direction = unknown_exits[0]
        print(f'Heading {direction}...')
        move_res = move(direction)
        cooldown(move_res)
        print('>>>>>>>>>> Heading into new room...')

        # Update the ?'s
        new_room_id = move_res['room_id']
        mapped_area[current_room_id][direction] = new_room_id

        # Update the current_room variables and prev_room_id
        prev_room_id = current_room_id
        current_room_id = new_room_id
        current_room_title = move_res['title']
        current_room_exits = move_res['exits']
        current_room_messages = move_res['messages']

        # Save updated mapped_area
        print('========== Updating map_file...')
        with open('traversal_graph.json', 'w') as map_file:
            json.dump(mapped_area, map_file, indent=4)
    # Otherwise, find a way back to closest room with an unknown exit
    else:
        print('========== Starting a BFS...')
        # Find closest room via BFS
        path_to_next = bfs(current_room_id, mapped_area)
        
        print(f'Proposed path back: {path_to_next}')
        # Make sure there's actually something being returned
        if path_to_next is not None and len(path_to_next) > 0:
            # Have the player travel back to room with unknown exits
            for index in range(len(path_to_next) - 1):
                for direction in mapped_area[path_to_next[index]]:
                    if mapped_area[path_to_next[index]][direction] == path_to_next[index + 1]:
                        print(f'Heading {direction}...')
                        print(f'Next room should be {path_to_next[index + 1]}...')
                        move_res = move(direction, path_to_next[index + 1])
                        cooldown(move_res)
                        bfs_room_id = move_res['room_id']
                        print(f'>>>>>>>>>> Made it to room {bfs_room_id}')

                        # Update the current_room variables and prev_room_id
                        prev_room_id = current_room_id
                        current_room_id = move_res['room_id']
                        current_room_title = move_res['title']
                        current_room_exits = move_res['exits']
                        current_room_messages = move_res['messages']
        else:
            break
