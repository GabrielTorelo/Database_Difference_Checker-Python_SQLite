from re import DOTALL, findall
from json import dump, load
from os import listdir, makedirs, path, walk
from err import Errors
from utils.iterable_handler import find_db_files
from utils.response_handler import get_ok_response
from dao import list_tables
from constants import DB_PATHS, OUTPUT_DB_PATH, PATTERN_PATH, PATTERN_PATH_JSON


def generate_json(multiple_files = False, multiple_db_files = False) -> str:
    db_paths = find_db_files(DB_PATHS)
    db_info = {}

    try:
        for db_path in db_paths:
            if path.exists(db_path):
                dir_name = path.basename(path.dirname(db_path))
                file_name = path.basename(db_path).replace(".db", "")
                if dir_name not in db_info:
                    db_info[dir_name] = {}
                db_info[dir_name][file_name] = list_tables(db_path)
            else:
                db_info[db_path] = "Database file not found"

        if not path.exists(OUTPUT_DB_PATH):
            makedirs(OUTPUT_DB_PATH)

        if multiple_files:
            for db_name in db_info:
                output_path = path.join(OUTPUT_DB_PATH, db_name)

                if not path.exists(output_path):
                    makedirs(output_path)

                for table_name in db_info[db_name]:
                    with open(path.join(OUTPUT_DB_PATH, db_name, f"{table_name}.json"), "w") as json_file:
                        dump(db_info[db_name][table_name], json_file, indent=4)
            return "JSON files generated successfully"

        if multiple_db_files:
            for db_name in db_info:
                with open(path.join(OUTPUT_DB_PATH, f"{db_name}.json"), "w") as json_file:
                    dump(db_info[db_name], json_file, indent=4)
            return "JSON files generated successfully"

        with open(path.join(OUTPUT_DB_PATH, "Data.json"), "w") as json_file:
            dump(db_info, json_file, indent=4)

        return "JSON file generated successfully"
    except Exception as e:
        raise Errors(code=7, message=f"Error generating JSON file: {str(e)}")

def create_json_from_data() -> None:
    file_path = ""
    json_data = {}

    try:
        for file in listdir(PATTERN_PATH):
            if file.endswith('.txt'):
                file_path = path.join(PATTERN_PATH, file)
                break

        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()

        sections = findall(r'(\w+):\[(.*?)\]', data, DOTALL)

        for section_name, section_content in sections:
            entries = []
            matches = findall(r'\{nome: (\w+), tipo: (\w+)\}', section_content)
            for nome, tipo in matches:
                entries.append({
                    "nome": nome,
                    "tipo": tipo
                })
            
            json_data[section_name] = entries

        with open(PATTERN_PATH_JSON, 'w', encoding='utf-8') as json_file:
            dump(json_data, json_file, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        raise Errors(code=3, message=f"Directory {file_path} not found")
    except Exception as e:
        raise Errors(code=9, message=f"Error processing data: {str(e)}")

def read_json_files_from_directory() -> list:
    data_files = []

    try:
        for dirpath, _, filenames in walk(OUTPUT_DB_PATH):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = load(file)
                        data['database_name'] = path.basename(dirpath)
                        data['file_name'] = filename
                        data_files.append(data)

        return data_files
    except FileNotFoundError:
        raise Errors(code=3, message=f"Directory {OUTPUT_DB_PATH} not found")
    except Exception as e:
        raise Errors(code=3, message=f"Error reading files from directory {OUTPUT_DB_PATH}: {str(e)}")

def write_json_output(data: dict) -> None:
    try:
        with open("Output.json", 'w') as file:
            dump(data, file, indent=4, ensure_ascii=False)

        return get_ok_response()
    except Exception as e:
        raise Errors(code=5, message=f"Error writing output file: {str(e)}")
