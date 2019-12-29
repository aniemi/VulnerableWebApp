from flask import Flask
from flask import render_template, redirect, request, url_for, session
import sqlite3
import os
from flask import g

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)

@app.before_request
def make_session_permanent():
    session.permanent = True

from routes import index, form, paste, login, logout

app.add_url_rule('/', 'index', index)
app.add_url_rule('/form', 'form', form)
app.add_url_rule('/paste', 'paste', paste)
app.add_url_rule('/login', 'login', login, methods=["POST"])
app.add_url_rule('/logout', 'logout', logout)


if __name__ == "__main__":
    app.run()


