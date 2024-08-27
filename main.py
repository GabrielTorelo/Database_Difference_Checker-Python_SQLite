from json import dumps, load, loads
from os import listdir, path
from err import Errors
from utils import get_ok_response


def load_data(file_name: str) -> dict:
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = load(file)

        return data
    except FileNotFoundError:
        raise Errors(code=2, message=f"File {file_name} not found")
    except Exception as e:
        raise Errors(code=2, message=f"Error loading file {file_name}: {str(e)}")

def compare_with_default(data_default: dict, data: dict) -> tuple:
    missing_tables = []
    missing_data = {}
    
    try:
      for table, schema in data_default.items():
          if table not in data:
              missing_tables.append(table)
          else:
              missing_columns = [
                  col for col in schema if col not in data[table]
              ]
              if missing_columns:
                  missing_data[table] = missing_columns

      return missing_tables, missing_data
    except Exception as e:
        raise Errors(code=4, message=f"Error comparing data: {str(e)}")

def compare_all_with_default(data_default: dict, *data_files: dict) -> dict:
    results = {}

    try:
      for data in data_files:
          file_name = data.get('file_name', 'unknown').replace('.json', '')
          missing_tables, missing_data = compare_with_default(data_default, data)
          results[file_name] = {
              "Missing_Tables": missing_tables,
              "Missing_Data": missing_data
          }

      return results
    except Exception as e:
        raise Errors(code=4, message=f"Error comparing all data: {str(e)}")

def read_json_files_from_directory(directory: str) -> list:
    data_files = []

    try:
      for filename in listdir(directory):
          if filename.endswith('.json'):
              file_path = path.join(directory, filename)
              with open(file_path, 'r', encoding='utf-8') as file:
                  data = load(file)
                  data['file_name'] = filename
                  data_files.append(data)

      return data_files
    except FileNotFoundError:
        raise Errors(code=3, message=f"Directory {directory} not found")
    except Exception as e:
        raise Errors(code=3, message=f"Error reading files from directory {directory}: {str(e)}")

def write_json_output(data: dict) -> None:
    try:
        with open("Output.json", 'w') as file:
            file.write(dumps(data, indent=4))

        return get_ok_response()
    except Exception as e:
        raise Errors(code=5, message=f"Error writing output file: {str(e)}")

def main():
  RESPONSE = None

  try:
      default_data = load_data(file_name="MOCK/PATTERN/data_default.json")
      data_files = read_json_files_from_directory(directory="MOCK/DATA")

      comparison_results = compare_all_with_default(default_data, *data_files)

      RESPONSE = write_json_output(data=comparison_results)
  except Errors as e:
      RESPONSE = e.get_response()
  except Exception as e:
      RESPONSE = Errors(code=1, message=f"{str(e)}").get_response()
  finally:
      print(RESPONSE)

if __name__ == "__main__":
    main()
