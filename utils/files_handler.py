from os import path
from json import load
from re import DOTALL, findall
from err import Errors
from constants import PATTERN_PATH_JSON
from utils.json_handler import create_json_from_data

def load_data() -> dict:
    try:
        if not path.exists(PATTERN_PATH_JSON):
            create_json_from_data(interpret_txt_file)

        with open(PATTERN_PATH_JSON, 'r', encoding='utf-8') as file:
            data = load(file)

        return data
    except FileNotFoundError:
        raise Errors(code=2, message=f"File {PATTERN_PATH_JSON} not found")
    except Errors as err:
        raise err
    except Exception as e:
        raise Errors(code=2, message=f"Error loading file {PATTERN_PATH_JSON}: {str(e)}")

def interpret_txt_file(file_path: str) -> dict:
    json_data = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()

        sections = findall(r'(\w+):\[(.*?)\]', data, DOTALL)

        for section_name, section_content in sections:
            entries = []
            matches = findall(r'\{name: (\w+), type: (\w+)\}', section_content)
            for name, typ in matches:
                entries.append({
                    "name": name,
                    "type": typ
                })

            entries.sort(key=lambda x: x['name'])
            
            json_data[section_name] = entries

        return dict(sorted(json_data.items()))
    except FileNotFoundError:
        raise Errors(code=2, message=f"Directory {file_path} not found")
    except Exception as e:
        raise Errors(code=9, message=f"Error processing data: {str(e)}")
