from flask import Flask, redirect, render_template, session, request
import sqlite3
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
database = sqlite3.connect('trending.db')
db = database.cursor()


app = Flask(__name__)


@app.route('/login')
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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
        product = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hashed)",
                             username=request.form.get("username"), hashed=hashed)
        if not product:
            return render_template("apology.html")

    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
