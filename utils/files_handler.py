from os import path
from json import load
from err import Errors
from constants import PATTERN_PATH_JSON
from utils.json_handler import create_json_from_data

def load_data() -> dict:
    try:
        if not path.exists(PATTERN_PATH_JSON):
            create_json_from_data()

        with open(PATTERN_PATH_JSON, 'r', encoding='utf-8') as file:
            data = load(file)

        return data
    except FileNotFoundError:
        raise Errors(code=2, message=f"File {PATTERN_PATH_JSON} not found")
    except Errors as err:
        raise err
    except Exception as e:
        raise Errors(code=2, message=f"Error loading file {PATTERN_PATH_JSON}: {str(e)}")
