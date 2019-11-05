import os
from flask import Flask, redirect, render_template, session, request, flash
import sqlite3
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import sqlqueries
database = sqlite3.connect('trending.db')
db = database.cursor()


app = Flask(__name__)
app.secret_key = os.urandom(24)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'


@app.route('/get/')
def get():
    return session.get('key', 'not set')


@app.route('/login', methods=["GET", "POST"])
def login():

    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter a username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter a password")
            return render_template("login.html")

        # Query database for username
        records = sqlqueries.checkUser(request.form.get("username"))
        # Ensure username exists and password is correct
        if len(records) != 1 or not check_password_hash(records[0]["hash"], request.form.get("password")):
            flash("Incorrect Username or Password")
            return render_template("login.html")
        session["user_id"] = records[0]['userID']

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
            # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter a username")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("Please enter a password")
            return render_template("register.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match")
            return render_template("register.html")

        hashed = generate_password_hash(request.form.get(
            "password"), method='pbkdf2:sha256', salt_length=8)
        username = request.form.get("username")
        sqlqueries.insertUser(username, hashed)

        return render_template("login.html")
    return render_template("register.html")


@app.route("/changepwd", methods=["GET", "POST"])
def changepwd():
    return render_template("changepwd.html")


@app.route("/")
@login_required
def index():

    return render_template('index.html')


@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
