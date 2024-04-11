import random
import string
import json

import pandas as pd


def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.json'

def read_json_file(file_path):
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The JSON contents as a dictionary.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            flattened = flatten_dict(v, new_key, sep=sep)
            if all(isinstance(val, dict) and not val for val in flattened.values()):
                continue  # Skip this dictionary if all values are empty dictionaries
            items.extend(flattened.items())
        else:
            items.append((new_key, v))
    return dict(items)


def transform_response(data: dict):
    if data is not None:
        properties= data.get("properties",'')
        if properties:
            results = [flatten_dict(d) for d in properties]
            df=pd.DataFrame(results)
            return df