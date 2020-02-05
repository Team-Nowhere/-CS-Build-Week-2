import json

def get_rooms(room_number=None, filename='traversal_graph.json'):
    with open(filename, 'r') as f:
        graph = json.load(f)
    
    if room_number == None:
        return graph
    else:
        return {room_number: graph[str(room_number)]}


def write_json(data, filename='traversal_graph.json'):
    with open(filename, 'w', ) as f:
        json.dump(data, f, indent=4)


def add_room(room_data, filename='traversal_graph.json'):
    """
    Data must be in {"0": {"n": '?', 'e' : 4, 's': 5, 'w': 2}}
    format for adding to traversal graph

    Add to json or updates room
    """
    with open(filename) as json_file:
        data = json.load(json_file)

        for k, v in room_data.items():
            data[k] = v

    write_json(data)