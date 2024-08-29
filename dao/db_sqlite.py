from sqlite3 import connect
from err import Errors
from constants import SELECT_TABLES, EXCLUDED_TABLES, EXCLUDED_COLUMNS, PRAGMA_TABLE_INFO


def list_tables(db_path):
    tables_info = {}

    try:
        connection = connect(db_path)
        cursor = connection.cursor()
        
        cursor.execute(SELECT_TABLES)
        tables = [row[0] for row in cursor.fetchall()]

        tables = sorted(tables)
        
        for table in tables:
            if table in EXCLUDED_TABLES:
                continue

            cursor.execute(PRAGMA_TABLE_INFO % table)
            columns = cursor.fetchall()

            tables_info[table] = sorted([
                {'name': col[1], 'type': col[2]} for col in columns if col[1] not in EXCLUDED_COLUMNS
            ], key=lambda x: x['name'])
        
        connection.close()
        return tables_info
    except Exception as e:
        raise Errors(code=6, message=f"Error listing database tables: {e}")
