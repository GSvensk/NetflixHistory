import pyodbc
from environment import CONNECTION_STRING

cnxn = pyodbc.connect(CONNECTION_STRING)

def add_media(name, runtime, is_movie):
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Media (media_name, runtime, is_movie) VALUES (?, ?, ?)", name, runtime, is_movie)
    cnxn.commit()

def get_media(name):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM Media WHERE media_name = ?", name)
    media = cursor.fetchone()

    if media:
        return media
    else:
        return None

def add_notfound(name):
    pass
    #cursor = cnxn.cursor()
    #cursor.execute("SELECT * FROM NotFound WHERE media_name = ?", name)
    #not_found = cursor.fetchone()
    #if not not_found:
    #    not_found = NotFound(name)
    #    db.session.add(not_found)
    #    db.session.commit()


def recreate_tables():
    cursor = cnxn.cursor()
    cursor.execute("DROP TABLE Media")
    cursor.execute("DROP TABLE NotFound")
    cursor.execute("CREATE TABLE Media (media_name varchar(255), runtime int, is_movie int)")
    cursor.execute("CREATE TABLE NotFound (media_name varchar(255) PRIMARY KEY)")
    cnxn.commit()


'''

def get_media(name):

    media = Media.query.filter_by(name=name).first()
    if media:
        return media
    else:
        return None

'''
