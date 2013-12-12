# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template

from os import environ

app = Flask(__name__)

DEBUG = hasattr(environ, 'DEBUG') and environ['DEBUG'] or False
DATABASE_URL = hasattr(environ, 'DATABASE_URL') and environ['DATABASE_URL'] \
    or ''


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/user/<username>')
def hello_user(username):
    return render_template('hello.html', name=DATABASE_URL)

if __name__ == '__main__':
    app.run(debug=DEBUG)
