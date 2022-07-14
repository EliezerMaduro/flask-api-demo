import json
from utils import read_json

FILE_PATH = 'users.json'



def get_users():
    file = read_json(FILE_PATH)
    dataframe = file
    return json.loads(dataframe.to_json(orient = 'records')), dataframe.shape[0]

def get_user_by_id(user_id: int):
    file = read_json(FILE_PATH)
    dataframe = file[file["id"]==user_id]
    try:
        data = json.loads(dataframe.to_json(orient = 'records'))[0]
        return data
    except IndexError as e:
        return None

def verify_user(user_id):
    if (get_user_by_id(user_id)== None):
        return False
    else:
        return True