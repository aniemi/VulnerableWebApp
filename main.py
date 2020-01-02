from flask import Flask
from flask import render_template, redirect, request, url_for, session
import sqlite3
import os
from flask import g
from routes import index, form, paste, login, logout

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)

@app.teardown_appcontext
def close_connection(exception): 
    db = getattr(g, '_database', None)
    if db is not None: 
        db.close()

app.add_url_rule('/', 'index', index)
app.add_url_rule('/form', 'form', form)
app.add_url_rule('/paste/', 'paste', paste)
app.add_url_rule('/login', 'login', login, methods=["POST"])
app.add_url_rule('/logout', 'logout', logout)

if __name__ == "__main__":
    app.run()