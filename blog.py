#!/usr/bin/env python3

# blog.py - controller

# imports
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
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
SECRET_KEY =
\x1ef\xf9\xb2\x0e\xa0\xda\xab\xc7\xbc7\x89\x8a\xaf\xba\x1fT\x86Qo?\xbc,\xa1

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

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
        if request.form['username'] != app.config['USERNAME'] or
        request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
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

# maps the url /main to the function main()
# which in turn sets the route to main.html
@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == "__main__": app.run(debug=True)
