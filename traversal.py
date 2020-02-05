import random
from main_functions import *
from endpoints import *

rev_dir = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

# Open existing map
with open('traversal_graph.json', 'r') as map_file:
    mapped_area = json.load(map_file) # Use this to roam
    # Make sure the keys come back as integers and not string
    mapped_area = {int(k):v for k,v in mapped_area.items()}

print('########## Grabbing start room...')
init_res = get_current_room() # Init api call
cooldown(init_res)
current_room = init_res
prev_room_id = 0
prev_direction = ''
print('########## Grabbing player info...')
status_res = status()
cooldown(status_res)
have_fly = 'fly' in status_res['abilities']
have_dash = 'dash' in status_res['abilities']
have_recall = 'recall' in status_res['abilities']
have_warp = 'warp' in status_res['abilities']

# Only used on first time boot up or if program ends without entering new room info
if init_res['room_id'] not in mapped_area:
    data = {}
    data['title'] = init_res['title']
    data['coordinates'] = init_res['coordinates']
    data['terrain'] = init_res['terrain']
    for direction in init_res['exits']:
        data[f'{direction}'] = '?'
    mapped_area[init_res['room_id']] = data

    # Save updated mapped_area
    print('========== Updating map_file...')
    with open('traversal_graph.json', 'w') as map_file:
        json.dump(mapped_area, map_file, indent=4)

while True:
    print(f'Rooms been to: {len(mapped_area)}')
    crd = dict() # current_room_dictonary
    current_room_id = current_room['room_id']

    # Check to see if player has explored the room already
    if current_room_id not in mapped_area:
        print(f'!!!!!!!!!! Room {current_room_id} is new!')
        data = {}
        data['title'] = current_room['title']
        data['coordinates'] = current_room['coordinates']
        data['terrain'] = current_room['terrain']
        for direction in current_room['exits']:
            data[f'{direction}'] = '?'
        mapped_area[current_room_id] = data

        if prev_direction is not '':
            # Update direction coming from
            mapped_area[current_room_id][rev_dir[f'{prev_direction}']] = prev_room_id
        
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
        print(f'Heading {direction} into an unknown room...')
        move_res = move(direction)
        cooldown(move_res)

        # Update the ?'s
        new_room_id = move_res['room_id']
        mapped_area[current_room_id][direction] = new_room_id

        # Update the current_room variables and prev_room_id
        prev_room_id = current_room_id
        current_room = move_res
        prev_direction = direction

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

        # Runs if 0 exists AND recall exists, AND in a position greater-equal than 3
        if 0 in path_to_next and have_recall is True and path_to_next.index(0) >= 3:
            print('>>>>>>>>>> Recalling to starting point...')
            recall_res = recall()
            cooldown(recall_res)

            zero_pos = path_to_next.index(0)
            path_to_next = path_to_next[zero_pos:]
            print(f'New proposed path back: {path_to_next}')

        # Make sure there's actually something being returned
        if path_to_next is not None and len(path_to_next) > 0:
            # Check to see if the paths are dashable
            directions = []	
            for i in range(len(path_to_next) - 1):	
                for direction in mapped_area[path_to_next[i]]:	
                    if mapped_area[path_to_next[i]][direction] == path_to_next[i+ 1]:	
                        directions.append(direction)
            dash_groups = dash_check(path_to_next, directions)

            # Dash activates when dash path is shorter AND have dash ability
            if len(dash_groups) < len(path_to_next)-1 and have_dash is True:
                for subgroup in dash_groups:
                    if len(subgroup) <= 1:
                        print(f'Heading {subgroup[0][1]}...')
                        print(f'Next room should be {subgroup[0][0]}...')

                        if have_fly is True and mapped_area[subgroup[0][0]]['terrain'] is not 'CAVE':
                            move_res = fly(subgroup[0][1], subgroup[0][0])
                        else:
                            move_res = move(subgroup[0][1], subgroup[0][0])
                        cooldown(move_res)

                        bfs_room_id = move_res['room_id']
                        print(f'>>>>>>>>>> Made it to room {bfs_room_id}')
                    else:
                        arr_len = len(subgroup)
                        room_id_arr = []
                        for tup in subgroup:
                            room_id_arr.append(str(tup[0]))
                        room_arr_str = ','.join(room_id_arr)
            
                        print(f'Dashing {subgroup[0][1]} through {arr_len} rooms...')
                        print(f'Next room should be {subgroup[arr_len-1][0]}...')

                        move_res = dash(subgroup[0][1], arr_len, room_arr_str)
                        cooldown(move_res)

                        bfs_room_id = move_res['room_id']
                        print(f'>>>>>>>>>> Made it to room {bfs_room_id}')
                    # Update the current_room variables and prev_room_id
                    prev_room_id = current_room_id
                    current_room_id = bfs_room_id
                    current_room = move_res
            else:
                for index in range(len(path_to_next) - 1):
                    for direction in mapped_area[path_to_next[index]]:
                        if mapped_area[path_to_next[index]][direction] == path_to_next[index + 1]:
                            print(f'Heading {direction}...')
                            print(f'Next room should be {path_to_next[index + 1]}...')

                            if have_fly is True and mapped_area[path_to_next[index+1]]['terrain'] is not 'CAVE':
                                move_res = move(direction, path_to_next[index + 1])
                            else:
                                move_res = fly(direction, path_to_next[index + 1])

                            cooldown(move_res)
                            bfs_room_id = move_res['room_id']
                            print(f'>>>>>>>>>> Made it to room {bfs_room_id}')

                            # Update the current_room variables and prev_room_id	
                            prev_room_id = current_room_id
                            current_room_id = bfs_room_id
                            current_room = move_res
            print('========== BFS Complete!')
        else:
            print('********** The map has been fully explored!')
            break