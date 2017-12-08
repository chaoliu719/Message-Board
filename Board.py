# coding=utf-8
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from flask_moment import Moment
from datetime import datetime
import time


app = Flask('demo')
moment = Moment(app)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'demo.db'),
    DEBUG=False,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    USERNAME='admin',
    PASSWORD='default'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    """Initializes the database."""
    with app.app_context():
        db = get_db()
        with app.open_resource('./schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text, rec, user from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries, current_time=datetime.utcnow(), conv=datetime.strptime)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text, rec, user) values (?, ?, ?, ?)',
               [request.form['title'], request.form['text'], datetime.utcnow(), session['username']])
    db.commit()
    flash('New message was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        inputpw = request.form['password']
        confirm = request.form['confirm_password']

        db = get_db()
        cur = db.execute('SELECT `username` FROM user WHERE username = ?',[username])
        if cur.fetchone():
            error = 'Duplicated Username!'
        elif inputpw != confirm:
            error = 'Unmatched Confirm!' 
        else:
            db.execute('insert into user (username, password) values (?, ?)', [request.form['username'], request.form['password']])
            db.commit()
            flash('Sign Up Secceed!')
            return redirect(url_for('login'))
    return render_template('signup.html', error=error, current_time=datetime.utcnow(), conv=datetime.strptime)

    



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.execute('SELECT `username`, `password` FROM user WHERE username = ?',[username])
        data = cur.fetchone()
        if (not data) or password != data[1]: 
            error = 'Invalid username or password'
        else:
            session['username'] = username
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error, current_time=datetime.utcnow(), conv=datetime.strptime)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



#init_db()
#app.run(port=5001, debug=True)
