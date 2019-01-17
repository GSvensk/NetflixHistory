import pyodbc
from environment import CONNECTION_STRING

cnxn = pyodbc.connect(CONNECTION_STRING)

def add_media(name, runtime, is_movie):
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Media (title, runtime, is_movie) VALUES (?, ?, ?)", name, runtime, is_movie)
    cnxn.commit()

def get_media(name):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM Media WHERE title = ?", name)
    media = cursor.fetchone()

    if media:
        return media
    else:
        return None

def add_notfound(name):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM NotFound WHERE title = ?", name)
    not_found = cursor.fetchone()
    if not not_found:
        cursor.execute("INSERT INTO NotFound (title) VALUES (?)", name)
        cnxn.commit()


def recreate_tables():
    cursor = cnxn.cursor()
    cursor.execute("DROP TABLE Media")
    cursor.execute("DROP TABLE NotFound")
    cursor.execute("CREATE TABLE Media (title varchar(255), runtime int, is_movie int)")
    cursor.execute("CREATE TABLE NotFound (title varchar(255) PRIMARY KEY)")
    cnxn.commit()

