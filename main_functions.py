import time
import random
from endpoints import *
import t_graph
import json
from itertools import groupby

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)


class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


def cooldown(data):
    cd = data['cooldown']
    print(f'Cooldown: {cd} seconds')
    wait_time = int(cd + 1)  # Add extra second to avoid program updating too fast
    time.sleep(wait_time)
    print('Cooldown Done!')

def bfs(starting_room_id, map_graph):
    queue = Queue()
    queue.enqueue([starting_room_id])
    visited = set()

    while queue.size() > 0:
        # grab path
        path = queue.dequeue()
        # take last in path
        current_room = path[-1]
        visited.add(current_room)
        
        # looks through an array that contains similarities
        for direction in set(list('nsew')).intersection(map_graph[current_room]):
            if map_graph[current_room][direction] == '?':
                return path    
            elif map_graph[current_room][direction] not in visited:
                # create a new path to append direction
                new_path = list(path)
                new_path.append(map_graph[current_room][direction])
                queue.enqueue(new_path)

def opp_dir(direction: str):
    """
    Given a direction ("n")

    return the opposite direction ("s")
    """
    opp_dir = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e',
    }
    return opp_dir[direction]


def get_paths(room_id: str):
    """
    Given a room id ('120')

    Return the unexplored exits as list ['n', 'e']
    """
    paths = []
    for direction, room in t_graph.get_rooms(room_id)[room_id].items():
        if room == '?':
            paths.append(direction)

    return paths

def fast_travel(starting_room_id, destination_room_id, collect_treasure=False):
    with open('traversal_graph.json', 'r') as map_file:
        map_graph = json.load(map_file)

    map_graph = {int(k):v for k,v in map_graph.items()}
    queue = Queue()
    queue.enqueue([starting_room_id])
    visited = set()
    path_found = False

    # Check abilites
    stats = status()
    print('Checking abilities...')
    have_fly = 'fly' in stats['abilities']
    have_dash = 'dash' in stats['abilities']
    have_recall = 'recall' in stats['abilities']
    cooldown(stats)

    if int(destination_room_id) == 0 and have_recall is True:
        if collect_treasure == False:
            print('Recalling...')
            rec_res = recall()
            cooldown(rec_res)
            recall_message = rec_res['messages'][0]
            print(recall_message)
            return

    if int(destination_room_id) == 1 and have_recall is True:
        print('Recalling...')
        rec_res = recall()
        cooldown(rec_res)
        recall_message = rec_res['messages'][0]
        print(recall_message)
        move_res = move("w", "1")
        cooldown(move_res)
        return

    while queue.size() > 0 and path_found == False:
        # grab path
        path = queue.dequeue()
        # take last in path
        current_room = path[-1]
        visited.add(current_room)
        
        # looks through an array that contains similarities
        for direction in set(list('nsew')).intersection(map_graph[current_room]):
            if map_graph[current_room][direction] == int(destination_room_id):
                path.append(int(destination_room_id))
                path_to_next = path
                break
            elif map_graph[current_room][direction] not in visited:
                # create a new path to append direction
                new_path = list(path)
                new_path.append(map_graph[current_room][direction])
                queue.enqueue(new_path)

    print(f'\nProposed path:\n{path_to_next}\n')

    # Check to see if it's worth recalling first before continuing
    if 0 in path_to_next \
        and have_recall is True \
        and path_to_next.index(0) >= 3 \
        and collect_treasure is False:
        print('Recalling...')
        recall_res = recall()
        cooldown(recall_res)

        zero_pos = path_to_next.index(0)
        path_to_next = path_to_next[zero_pos:]
        print(f'\nNew proposed path:\n{path_to_next}\n')

    path_directions = []

    for i in range(len(path_to_next) - 1):
        for direction, room_number in map_graph[path_to_next[i]].items():
            if room_number == path_to_next[i + 1]:
                path_directions.append(direction)

    
    direction_chunks = [list(g) for k, g in groupby(path_directions)]
    
    number_chunks = []

    temp = path_to_next[1:]
    for i in direction_chunks:
        chunk_length = len(i)
        number_chunks.append(temp[:chunk_length])
        temp = temp[chunk_length:]

    if have_dash is True and have_fly is True and collect_treasure==False:
        for chunk in range(len(direction_chunks)):
            if len(direction_chunks[chunk]) < 3:
                for step in range(len(direction_chunks[chunk])):
                    try:
                        next_terrain = map_graph[number_chunks[chunk + 1][0]]['terrain']
                        if next_terrain == 'CAVE':
                            print(f'Walking {direction_chunks[chunk][step]}...')
                            print(f'Next room should be {number_chunks[chunk][step]}...')
                            move_res = move(direction_chunks[chunk][step], number_chunks[chunk][step])
                            cooldown(move_res)
                        else:
                            print(f'Flying {direction_chunks[chunk][step]}...')
                            print(f'Next room should be {number_chunks[chunk][step]}...')
                            move_res = fly(direction_chunks[chunk][step], number_chunks[chunk][step])
                            cooldown(move_res)
                    except:
                        next_terrain = map_graph[int(destination_room_id)]['terrain']
                        if next_terrain == 'CAVE':
                            print(f'Walking {direction_chunks[chunk][step]}...')
                            print(f'Next room should be {number_chunks[chunk][step]}...')
                            move_res = move(direction_chunks[chunk][step], number_chunks[chunk][step])
                            cooldown(move_res)
                        else:
                            print(f'Flying {direction_chunks[chunk][step]}...')
                            print(f'Next room should be {number_chunks[chunk][step]}...')
                            move_res = fly(direction_chunks[chunk][step], number_chunks[chunk][step])
                            cooldown(move_res)

                    bfs_room_id = move_res['room_id']
                    print(f'>>>>>>>>>> Made it to room {bfs_room_id}\n')


            else:
                number_of_rooms = len(direction_chunks[chunk])
                dash_direction = direction_chunks[chunk][0]
                dash_room_ids = ','.join([str(x) for x in number_chunks[chunk]])


                print(f'Dashing {dash_direction.upper()} through {number_of_rooms} rooms...')
                dash_res = dash(dash_direction, number_of_rooms, dash_room_ids)
                cooldown(dash_res)
                last_movement = 'dash'
                dash_room_id = dash_res["room_id"]
                print(f'>>>>>>>>>> Made it to room {dash_room_id}\n')


        print('============> Fast travel complete')

    elif have_dash is True and have_fly is False and collect_treasure==False:
        for chunk in range(len(direction_chunks)):
            if len(direction_chunks[chunk]) < 3:
                for step in range(len(direction_chunks[chunk])):
                    print(f'Walking {direction_chunks[chunk][step]}...')
                    print(f'Next room should be {number_chunks[chunk][step]}...')

                    move_res = move(direction_chunks[chunk][step], number_chunks[chunk][step])
                    cooldown(move_res)

                    bfs_room_id = move_res['room_id']
                    print(f'>>>>>>>>>> Made it to room {bfs_room_id}\n')

            else:
                number_of_rooms = len(direction_chunks[chunk])
                dash_direction = direction_chunks[chunk][0]
                dash_room_ids = ','.join([str(x) for x in number_chunks[chunk]])


                print(f'Dashing {dash_direction.upper()} through {number_of_rooms} rooms...')
                dash_res = dash(dash_direction, number_of_rooms, dash_room_ids)
                cooldown(dash_res)
                last_movement = 'dash'
                dash_room_id = dash_res["room_id"]
                print(f'>>>>>>>>>> Made it to room {dash_room_id}\n')


        print('============> Fast travel complete')

    elif have_dash is False and have_fly is True and collect_treasure == False:
        if path_to_next is not None and len(path_to_next) > 0:
            # Have the player travel back to room with unknown exits
            for index in range(len(path_to_next) - 1):
                for direction in map_graph[path_to_next[index]]:
                    if map_graph[path_to_next[index]][direction] == path_to_next[index + 1]:
                        next_terrain = map_graph[path_to_next[index + 1]]['terrain']
                        
                        if next_terrain == 'CAVE':
                            print(f'Walking {direction}...')
                            print(f'Next room should be {path_to_next[index + 1]}...')
                            move_res = move(direction, path_to_next[index + 1])
                            cooldown(move_res)
                        else:
                            print(f'Flying {direction}...')
                            print(f'Next room should be {path_to_next[index + 1]}...')
                            move_res = fly(direction, path_to_next[index + 1])
                            cooldown(move_res)

                        bfs_room_id = move_res['room_id']
                        print(f'>>>>>>>>>> Made it to room {bfs_room_id}\n')

            print('============> Fast travel complete')

    else:
        if path_to_next is not None and len(path_to_next) > 0:
            # Have the player travel back to room with unknown exits
            for index in range(len(path_to_next) - 1):
                for direction in map_graph[path_to_next[index]]:
                    if map_graph[path_to_next[index]][direction] == path_to_next[index + 1]:
                        next_terrain = map_graph[path_to_next[index + 1]]['terrain']
                        
                        if next_terrain != 'CAVE' and have_fly is True:
                            print(f'Flying {direction}...')
                            print(f'Next room should be {path_to_next[index + 1]}...')
                            move_res = fly(direction, path_to_next[index + 1])
                            cooldown(move_res)
                        else:
                            print(f'Walking {direction}...')
                            print(f'Next room should be {path_to_next[index + 1]}...')
                            move_res = move(direction, path_to_next[index + 1])
                            cooldown(move_res)

                        if collect_treasure == True:
                            if len(move_res['items']) > 0:
                                print('Picking up items first...')
                                for item in move_res['items']:
                                    take_res = take(item)
                                    print(take_res['messages'])
                                    cooldown(take_res)

                        bfs_room_id = move_res['room_id']
                        print(f'>>>>>>>>>> Made it to room {bfs_room_id}\n')

            print('============> Fast travel complete')

def dash_check(room_arr, dir_arr):
    last = dir_arr[0]
    new_path = []
    temp_path = []
    for i, direction in enumerate(dir_arr):
        if direction == last:
            tup = (room_arr[i+1], direction)
            temp_path.append(tup)
        else:
            new_path.append(temp_path)
            temp_path = []
            tup = (room_arr[i+1], direction)
            temp_path.append(tup)

        # Catch for the very last one
        if i is len(dir_arr)-1 and temp_path is not None and len(temp_path) > 0:
            new_path.append(temp_path)
            return new_path

        last = direction

def sell_all(current_room_id):
    if current_room_id != 1:
        print('You can only sell at the shop.')
    else:
        print('========== Welcome to the shop!')
        status_res = status()
        inventory = status_res['inventory']
        print(f'Current inventory: {inventory}')
        cooldown(status_res)

        if len(inventory) > 0 and inventory is not None:
            for item in inventory:
                print(f'>>>>>>>>>> Selling {item}...')
                sell_res = sell(item, True)
                cooldown(sell_res)
                print(f'!!!!!!!!!! Sold {item}!')
            print('========== All items sold!')
        else:
            print('========== Nothing to sell!')

def say_prayer(current_room_id):
    if current_room_id not in [22, 374, 461, 492, 499]:
        print('You can only pray at shrines.')
    else:
        print('========== You are at a place of worship...')
        status_res = status()
        cooldown(status_res)

        if 'pray' in status_res['abilities']:
            print('>>>>>>>>>> Praying...')
            pray_res = pray()
            cooldown(pray_res)
            messages = pray_res['messages']
            print(f'!!!!!!!!!! {messages[0]}')
        else:
            print('========== You do not have the ability to pray!')