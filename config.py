import os
import json

""" All methods dealing with the config.json file will be handled by this file.

    This includes, but is not limited to, checking if config exists, loading config
    into a dict and saving to the config     

"""

class Config:

    def __init__(self, file) -> None:
        self.file = file
        self.dir_location = os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(self.dir_location, self.file)

    def get_config(self) -> dict:
        # TODO does config json files exist if so open file and get config variables
        if not self.config_exists():
            # TODO if config doesn't exist, set one up for user
            return {"Error": f"{self.file_path} does not exist"}
        with open(self.file_path, 'r') as f:
            config_dict = json.load(f)
            app_config = config_dict
        return app_config

    def save_config(self, new_config) -> bool:
        if not self.config_exists():
            # TODO if config doesn't exist, set one up for the user
            return False
        with open(self.file_path, 'w') as f:
            json.dump(new_config, f)
        return True

    def config_exists(self) -> bool:
        return os.path.exists(self.file_path)

