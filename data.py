import sqlite3
from flask import g

DATABASE = 'database.db'

def init_db():
    with app.app_context(): 
        db = get_db() 
        with app.open_resource('schema.sql', mode='r') as f: 
            db.cursor().executescript(f.read())
        db.commit()

def get_db(): 
    db = getattr(g, '_database', None)
    if db is None: 
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    db.row_factory = sqlite3.Row
    return db

def get_all():
    query = "SELECT * FROM pastes WHERE private_paste = 'False';"
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close() 
    print(rv)
    return rv

def get_paste(id, user='Not logged in'): 
    query = "SELECT * FROM pastes WHERE id = '" + str(id) + "';"
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

def save_paste_to_db(query):
    cur = get_db().execute(query)
    cur.close()

def user_credentials(username): 
    query = "SELECT * FROM 'users' WHERE user = '" + str(username) + "';"
    print(query)
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close() 
    return rv

def add_user(username, pw, email="Null"): 
    query = "INSERT INTO users (user, pw, email) VALUES ('" + username + "', '" + pw + "', '" + email + "');"
    try: 
        cur = get_db().execute(query)
        cur.close()
    except: 
        print("error")

def get_user_pastes(username): 
    query = "SELECT * FROM pastes WHERE user='" + str(username) + "';"
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

