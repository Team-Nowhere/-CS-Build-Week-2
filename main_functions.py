import time
import random
import endpoints as actions
import t_graph

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

# def bfs(starting_room, destination_room):
#     """
#     Use to find the shortest path between two room

#     Returns a list of directions ['n', 'n', 'e', 's', 's', 'e']

#     Starting and destination room are room numbers
#     ie bfs("0", "23")
#     """
#     queue = Queue()

#     visited = set()

#     queue.enqueue([starting_room])

#     while queue.size() > 0:

#         path = queue.dequeue()

#         room = path[-1]

#         if room not in visited:

#             if room == destination_room:
#                 break

#             visited.add(room)

#             for next_room in list(t_graph.get_rooms(room).values()):
#                 if next_room != '?':
#                     new_path = list(path)
#                     new_path.append(next_room)
#                     queue.enqueue(new_path)

#     directions = []
#     for i in range(len(path) - 1):
#         for direction, room in t_graph.get_rooms()[path[i]].items():
#             if room == path[i+1]:
#                 directions.append(direction)
    
#     return directions

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


def traverse(traverse_time: int):
    start_time = time.time()
    good_rooms = Stack()
    traversal_path = []

    while time.time() - start_time < traverse_time:
        # Get the current room data
        current_room = actions.get_current_room()
        cooldown(current_room)

        # Get the unexplored paths from room
        avail_paths = get_paths(current_room['room_id'])

        # If room has more than one unexplored exit, push to good rooms
        if len(avail_paths) > 1:
            good_rooms.push(current_room['room_id'])

        # If no available paths, find a good room
        if not avail_paths:

            found_room = False

            while found_room == False:
                backup_room = good_rooms.pop()

                if len(get_paths(backup_room)) > 0:
                    found_room == True

            move_back = bfs(current_room['room_id'], backup_room)

            # Travel to good room
            for move in move_back:
                current_room = actions.move(move)
                cooldown(current_room)

            # Add to return to good room to traversal path
            traversal_path += move_back

            # Get the current room
            current_room = actions.get_room_data()
            cooldown(current_room)
            
            # if room still a good room add back to good rooms
            if len(get_paths(current_room['room_id'])) > 1:
                good_rooms.push(current_room['room_id'])
        

        # If there are paths travel to them
        if 'w' in avail_paths:
            direction = 'w'
        elif 's' in avail_paths:
            direction = 's'
        elif 'n' in avail_paths:
            direction = 'n'
        elif 'e' in avail_paths:
            direction = 'e'
        

        new_room = actions.move(direction)
        cooldown(new_room)
        
        if new_room['room_id'] not in t_graph.get_rooms():
            new_room_json = {new_room['room_id']: {i: '?' for i in new_room['exits']}}
        else:
            new_room_json = t_graph.get_rooms(new_room['room_id'])
        old_room_json = t_graph.get_rooms(current_room['room_id'])
        
        new_room_json[new_room['room_id']][opp_dir(direction)] = current_room['room_id']
        old_room_json[current_room['room_id']][direction] = new_room['room_id']

        t_graph.add_room(new_room_json)
        time.sleep(1)
        t_graph.add_room(old_room_json)





    





