from flask import abort
import json
from utils import read_json

FILE_PATH = 'tasks.json'



def get_tasks(completed: bool = None, title: str = None):
    file = read_json(FILE_PATH)
    if completed != None and title != None:
        dataframe = file[(file["title"]==title) & (file["completed"] == completed)]
    elif title != None or completed != None:
        if completed != None:
            dataframe = file[file["completed"]==completed]
        else:
            dataframe = file[file["title"]==title]
    else:
        dataframe = file
    return json.loads(dataframe.to_json(orient = 'records')), dataframe.shape[0]


def get_tasks_by_id(id: int):
    file = read_json(FILE_PATH)
    dataframe = file[file["id"]==id]
    try:
        data = json.loads(dataframe.to_json(orient = 'records'))[0]
        return data
    except IndexError:
        return abort(404)

def get_tasks_by_user_id(user_id: int, completed = None, title = None):
    file = read_json(FILE_PATH)
    if completed != None and title != None:
        dataframe = file[(file["title"]==title) & (file["completed"] == completed ) & (file["user_id"] == user_id)]
    elif title != None or completed != None:
        if completed != None:
            dataframe = file[(file["completed"]==completed) & (file["user_id"] == user_id)]
        else:
            dataframe = file[(file["title"]==title) & (file["user_id"] == user_id)]
    else:
        dataframe = file[file["user_id"]==user_id]
        
    
    return json.loads(dataframe.to_json(orient = 'records')), dataframe.shape[0]