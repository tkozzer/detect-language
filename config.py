import os
import json

""" All methods dealing with the config.json file will be handled by this file.

    This includes, but is not limited to, checking if config exists, loading config
    into a dict and saving to the config     

"""

def get_config(file) -> dict:
    # TODO does config json files exist if so open file and get config variables
    __location__ = os.path.dirname(os.path.realpath(__file__))
    if not config_exists(os.path.join(__location__, file)):
        return {"Error": f"{file} does not exist"}
    with open(os.path.join(__location__, file), 'r') as f:
        config_dict = json.load(f)
        app_config = config_dict
    return app_config

def save_config(file, new_config) -> bool:
    if not config_exists(file):
        return False
    __location__ = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(__location__, file), 'w') as f:
        json.dump(new_config, f)
    return True

def config_exists(file) -> bool:
    return os.path.exists(file)

