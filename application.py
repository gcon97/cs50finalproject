import os
from flask import Flask, redirect, render_template, session, request, flash
import sqlite3
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
database = sqlite3.connect('trending.db')
db = database.cursor()


app = Flask(__name__)
app.secret_key = os.urandom(24)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
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


def insertUser(username, hash):
    try:
        sqliteConnection = sqlite3.connect('trending.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_with_param = """INSERT INTO 'users'
                          ('username', 'hash') 
                          VALUES (?, ?);"""

        data_tuple = (username, hash)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into user table", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def checkUser(username):
    records = []
    try:
        sqliteConnection = sqlite3.connect('trending.db')
        cursor = sqliteConnection.cursor()
        sql_select_query = """select * from users where username = ?"""
        cursor.execute(sql_select_query, (username,))
        rows = cursor.fetchall()
        for row in rows:
            dictentry = {'userID': row[0], 'username': row[1], 'hash': row[2]}
            records.append(dictentry)

        for record in records:
            print(record)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into user table", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("closed")
        return records


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
        records = checkUser(request.form.get("username"))
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
            return render_template("apology.html")
        elif not request.form.get("password"):
            return render_template("apology.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("apology.html")

        hashed = generate_password_hash(request.form.get(
            "password"), method='pbkdf2:sha256', salt_length=8)
        username = request.form.get("username")
        insertUser(username, hashed)
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
