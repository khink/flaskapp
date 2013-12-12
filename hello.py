# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS')
app.config.from_envvar('FLASK_SECRETS', silent=True)


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/user/<username>')
def hello_user(username):
    return render_template('hello.html', name=app.config['DATABASE_URL'])

if __name__ == '__main__':
    app.run()
