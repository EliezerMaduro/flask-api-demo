import pandas

def read_json(file_path):
    file = pandas.read_json(file_path)
    return file