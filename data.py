import sqlite3
from flask import Flask, g, current_app

DATABASE = 'database.db'

def get_db(): 
    db = getattr(g, '_database', None)
    if db is None: 
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def read_db(query):
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

def write_db(query): 
    cur = get_db().execute(query)
    cur.close()

def get_all():
    query = "SELECT * FROM pastes WHERE private_paste = 'False';"
    return read_db(query)

def get_paste(id, user='Not logged in'): 
    query = "SELECT * FROM pastes WHERE id = '" + str(id) + "';"
    return read_db(query)

def save_paste_to_db(query):
    write_db(query)

def user_credentials(username): 
    query = "SELECT * FROM 'users' WHERE user = '" + str(username) + "';"
    return read_db(query)

def add_user(username, pw, email="Null"): 
    query = "INSERT INTO users (user, pw, email) VALUES ('" + username + "', '" + pw + "', '" + email + "');"
    try: 
        write_db(query)
    except: 
        print("Error.")

def get_user_pastes(username): 
    query = "SELECT * FROM pastes WHERE user='" + str(username) + "';"
    return read_db(query)

