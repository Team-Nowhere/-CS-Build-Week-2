import requests
import json
from decouple import config

SECRET_TOKEN = config('SECRET_TOKEN')
TOKEN_HEADER = 'Token ' + SECRET_TOKEN
AUTH_HEADER = {'Authorization': TOKEN_HEADER}
base_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/'
bc_url = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/'

def get_current_room():
    return requests.get(
        url=base_url+'init',
        headers={'Authorization': TOKEN_HEADER}
    ).json()

def move(move_direction: str, next_room_id = None):
    if next_room_id == None:
        return requests.post(
            url=base_url+'move/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'direction': f'{move_direction}'
            }
        ).json()
    else:
        return requests.post(
            url=base_url+'move/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'direction': f'{move_direction}',
                'next_room_id': f'{next_room_id}'
            }
        ).json()

def take(treasure_name:str):
    return requests.post(
            url=base_url+'take/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'name': f'{treasure_name}'
            }
        ).json()

def drop(treasure_name:str):
    return requests.post(
            url=base_url+'drop/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'name': f'{treasure_name}'
            }
        ).json()

def sell(treasure_name:str):
    return requests.post(
            url=base_url+'sell/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'name': f'{treasure_name}'
            }
        ).json()

def status():
    return requests.post(
            url=base_url+'status/',
            headers={
                'Authorization': TOKEN_HEADER
            }
        ).json()

def equip(item_name:str):
    return requests.post(
            url=base_url+'wear/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'name': f'{item_name}'
            }
        ).json()

def unequip(item_name:str):
    return requests.post(
            url=base_url+'undress/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'name': f'{item_name}'
            }
        ).json()

def change_name(new_name:str):
    return requests.post(
            url=base_url+'change_name/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'name': f'{new_name}'
            }
        ).json()

def pray(item_name:str):
    return requests.post(
            url=base_url+'pray/',
            headers={
                'Authorization': TOKEN_HEADER
            }
        ).json()

def fly(direction:str):
    return requests.post(
            url=base_url+'fly/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'direction': f'{direction}'
            }
        ).json()

def dash(direction:str, num_rooms:str, next_room_ids:str):
    return requests.post(
            url=base_url+'dash/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'direction': f'{direction}',
                'num_rooms': f'{num_rooms}',
                'next_room_ids': f'{next_room_ids}'
            }
        ).json()

def give_ghost(item_name:str):
    return requests.post(
            url=base_url+'carry/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'name': f'{item_name}'
            }
        ).json()

def take_ghost():
    return requests.post(
            url=base_url+'receive/',
            headers={
                'Authorization': TOKEN_HEADER
            }
        ).json()

def warp():
    return requests.post(
            url=base_url+'warp/',
            headers={
                'Authorization': TOKEN_HEADER
            }
        ).json()

def recall():
    return requests.post(
            url=base_url+'recall/',
            headers={
                'Authorization': TOKEN_HEADER
            }
        ).json()

def transmogrify(item_name:str):
    return requests.post(
            url=base_url+'transmogrify/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'name': f'{item_name}'
            }
        ).json()

def mine(new_proof):
    return requests.post(
            url=bc_url+'mine/',
            headers={
                'Authorization': TOKEN_HEADER
            },
            json={
                'proof': f'{new_proof}'
            }
        ).json()

def last_proof():
    return requests.get(
            url=bc_url+'last_proof/',
            headers={
                'Authorization': TOKEN_HEADER
            }
        ).json()

def get_balance():
    return requests.get(
            url=bc_url+'get_balance/',
            headers={
                'Authorization': TOKEN_HEADER
            }
        ).json()