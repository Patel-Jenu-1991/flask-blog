#!/usr/bin/env python3

# blog.py - controller

# imports
from flask import Flask, render_template, request, session, \
flash, redirect, url_for, g
from functools import wraps
import sqlite3

# configuration
DATABASE = 'blog.db'
# User credentials to log-in to access the main blog page
USERNAME = 'admin'
PASSWORD = 'admin'
# Add the SECRET_KEY, which is used for managing user sessions
# Best-Practice: Use a random key generator to do this
# for example:
# import os
# os.urandom(24) # generates a random string of 24 chars, hard to guess
SECRET_KEY = b'\x94xt\x19>ra\xf6\r%\xa0%\xd6_\x92i\xb0\xc1\xa7\xf8\xdf9\x99\xf7'

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# function for requiring user authentication
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap

# function used for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# maps the url / to the function login()
# which in turn sets the route to login.html
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
        request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401   # 401 - not authorized
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code

# function for logging out
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

# Adding the ability to add new posts to the blog for users
@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        # if the provided fields are empty
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO posts (title, post) values (?, ?)',
        [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash("New entry was successfully posted!")
        return redirect(url_for('main'))

# maps the url /main to the function main()
# which in turn sets the route to main.html
@app.route('/main')
@login_required
def main():
    g.db = connect_db() # connects to the database
    # fetches data from the posts table within the database
    cur = g.db.execute('SELECT * FROM posts')
    # creates an array of dictionaries containing the data from
    # a row retrieved from posts table
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    # close the database connection
    g.db.close()
    # posts = posts passes that variable to the main.html file
    return render_template('main.html', posts=posts)

if __name__ == "__main__": app.run(debug=True)
