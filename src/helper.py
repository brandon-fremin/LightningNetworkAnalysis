import json
import requests
import pickle as pkl


def save(object, filename):
    filename = "pickles/" + filename
    pkl.dump(object, open(filename, "wb"))


def load(filename, req=None, try_load=True):
    filename = "pickles/" + filename
    if not req and not try_load:
        return {}

    if not req and try_load:
        try:
            return pkl.load(open(filename, "rb"))
        except:
            return {}

    if req and try_load:
        try:
            return pkl.load(open(filename, "rb"))
        except:
            data = requests.get(req).json()
            pkl.dump(data, open(filename, "wb"))
            return data

    if req and not try_load:
        data = requests.get(req).json()
        pkl.dump(data, open(filename, "wb"))
        return data


def print_json(data, indent=2):
    print(json.dumps(data, indent=indent))

