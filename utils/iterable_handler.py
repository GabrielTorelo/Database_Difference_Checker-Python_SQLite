from os import walk, path
from err import Errors
from constants import EXCLUDED_COLUMNS, EXCLUDED_TABLES


def find_db_files(root_dir) -> list:
    db_files = []

    try:
        for dirpath, _, filenames in walk(root_dir):
            for filename in filenames:
                if filename.endswith('.db'):
                    db_files.append(path.join(dirpath, filename))

        return db_files
    
    except Exception as e:
        raise Errors(code=8, message=f"Error finding db files: {str(e)}")

def compare_with_default(data_default: dict, data: dict) -> tuple:
    missing_tables = []
    missing_data = {}
    
    try:
        for table, schema in data_default.items():
            if table in EXCLUDED_TABLES:
                continue

            if table not in data:
                missing_tables.append(table)
            else:
                missing_columns = [
                    col for col in schema if col not in data[table] and col['nome'] not in EXCLUDED_COLUMNS
                ]

                if missing_columns:
                    missing_data[table] = missing_columns

        missing_tables.sort()
        missing_data = {table: sorted(columns, key=lambda x: x['nome']) for table, columns in sorted(missing_data.items())}

        return missing_tables, missing_data
    except Exception as e:
        raise Errors(code=4, message=f"Error comparing data: {str(e)}")

def compare_all_with_default(data_default: dict, *data_files: dict) -> dict:
    results = {}

    try:
        for data in data_files:
            database_name = data.get("database_name", "unknown")
            file_name = data.get('file_name', 'unknown').replace('.json', '')

            missing_tables, missing_data = compare_with_default(data_default, data)

            if database_name not in results:
                results[database_name] = {}

            results[database_name][file_name] = {
                "Missing_Tables": missing_tables,
                "Missing_Data": missing_data
            }

        return {db: dict(sorted(results[db].items())) for db in sorted(results)}
    except Exception as e:
        raise Errors(code=4, message=f"Error comparing all data: {str(e)}")
