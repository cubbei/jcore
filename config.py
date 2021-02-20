import json
import traceback

from log import critical



def load_settings():
    try:
        with open("config.json", "r") as stream:
            return json.load(stream)
    except Exception as e:
        critical("The configuration file could not be found. Ensure `config.json` is in the same folder the script is executed from.")
        print(type(e), traceback.format_exc())
        exit()