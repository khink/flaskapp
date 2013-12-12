# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template

from os import environ

app = Flask(__name__)

# with app.test_request_context():
# 	css_url = url_for('static', filename='style.css')

DATABASE_URL = environ['DATABASE_URL']

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/user/<username>')
def hello_user(username):
    return render_template('hello.html', name=DATABASE_URL)

if __name__ == '__main__':
    app.run(debug=True)
