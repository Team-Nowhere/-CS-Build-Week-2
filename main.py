import time
import random
import endpoints as action
import t_graph
import sys

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
    print('Waiting for cooldown')
    wait_time = int(data['cooldown'])
    time.sleep(wait_time)
    print('Cooldown Done')
    
def bfs(starting_room, destination_room):
    queue = Queue()

    visited = set()

    queue.enqueue([starting_room])

    while queue.size() > 0:

        path = queue.dequeue()

        room = path[-1]

        if room not in visited:

            if room == destination_room:
                break

            visited.add(room)

            for next_room in list(t_graph.get_rooms(room).values()):
                if next_room != '?':
                    new_path = list(path)
                    new_path.append(next_room)
                    queue.enqueue(new_path)



data = action.get_room_data()
if '-start' in sys.argv:
    t_graph.add_room({data['room_id']: {i: '?' for i in data['exits']}})

# Explore until full inventory?
while True:
    # Get room data
    cooldown(data)

    # Choose a random direction to explore
    current_paths = data['exits']
    unexplored_paths = []
    for k, v in t_graph.get_rooms()[data['room_number']]:
        for path in current_paths:
            if v[path] == '?':
                unexplored_paths.append(path)


    choice = random.choice(unexplored_paths)

    data = action.move(choice)


