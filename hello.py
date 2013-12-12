# -*- coding: utf-8 -*-
from contextlib import closing
from flask import Flask
from flask import render_template

import sqlite3

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS')
app.config.from_envvar('FLASK_SECRETS', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/user/<username>')
def hello_user(username):
    return render_template('hello.html', name=username)

if __name__ == '__main__':
    app.run()
