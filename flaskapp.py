# -*- coding: utf-8 -*-
from contextlib import closing
from flask import Flask
from flask import abort
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

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


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/students')
def show_students():
    cur = g.db.execute('select name, klass from students order by id desc')
    students = [dict(name=row[0], klass=row[1]) for row in cur.fetchall()]
    return render_template('show_students.html', students=students)


@app.route('/students/add', methods=['POST'])
def add_student():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into students (name, klass) values (?, ?)',
                 [request.form['name'], request.form['klass']])
    g.db.commit()
    flash('New student was successfully created')
    return redirect(url_for('show_students'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_students'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_students'))


if __name__ == '__main__':
    app.run()
