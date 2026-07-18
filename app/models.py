import sqlite3

# with connects db and automatically closes it when done
with sqlite3.connect("upload-db.db") as connection:
    cursor = connection.cursor() # execute SQL commands and queries on db

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        status TEXT NOT NULL,
        target_size_mb REAL
    );
    '''

    cursor.execute(create_table_query)
    connection.commit()
