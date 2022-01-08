from os import listdir, curdir, SEEK_END
import json


def create_cache(dict):
    cache = {}
    s_keys = set()
    for key in dict:
        s_keys.add(key)
        s_keys.add(key[:-1])
    for key in s_keys:
        cache[key] = [k for k in dict if key in k]
    return cache


def sort_dict(unsorted_dictionary):
    return dict(sorted(unsorted_dictionary.items(), key=lambda y: y[1], reverse=True))


def does_file_exist(file_name):
    files_in_folder = listdir(curdir)
    if file_name in files_in_folder:
        return True
    else:
        return False


def read_from_file(file_name):
    with open(file_name, 'r') as f:
        read_data = f.read()
        return read_data


def write_to_file(file_name, data):
    with open(file_name, 'a') as f:
        f.write(data)


def delete_from_file(file_name):
    with open(file_name, 'rb+') as filehandle:
        filehandle.seek(-1, SEEK_END)
        filehandle.truncate()


def read_json_file(file_name):
    data = {}
    with open(file_name) as f:
        data = json.load(f)
    return data


def write_to_json_file(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f)
