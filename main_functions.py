import time
import random
from endpoints import *
import t_graph
import json

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

def fast_travel(starting_room_id, destination_room_id, stop_treasure=False):
    with open('traversal_graph.json', 'r') as map_file:
        map_graph = json.load(map_file)

    map_graph = {int(k):v for k,v in map_graph.items()}
    queue = Queue()
    queue.enqueue([starting_room_id])
    visited = set()
    path_found = False

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

    print(f'Proposed path: {path_to_next}')

    if path_to_next is not None and len(path_to_next) > 0:
        # Have the player travel back to room with unknown exits
        for index in range(len(path_to_next) - 1):
            for direction in map_graph[path_to_next[index]]:
                if map_graph[path_to_next[index]][direction] == path_to_next[index + 1]:
                    print(f'Heading {direction}...')
                    print(f'Next room should be {path_to_next[index + 1]}...')
                    move_res = move(direction, path_to_next[index + 1])
                    cooldown(move_res)
                    if stop_treasure == True:
                        if len(move_res['items']) > 0:
                            for item in move_res['items']:
                                take_res = take(item)
                                print(take_res['messages'])
                                cooldown(take_res)
                    bfs_room_id = move_res['room_id']
                    print(f'>>>>>>>>>> Made it to room {bfs_room_id}')


        print('========== Fast Travel Complete!')

def sell_all(current_room_id):
    if current_room_id is not 1:
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
