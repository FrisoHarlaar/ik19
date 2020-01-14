import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///brainbrawlers.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# The index page.
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST
    if request.method == "POST":

        # Assign form input to local dict
        form = {"username": request.form.get("username"), "password": request.form.get("password"), "confirmation": request.form.get("confirmation")}

        # Ensure form was fully filled out
        for form_item in form.items():
            if form_item[1] == '':
                message = "must provide " + form_item[0]
                return render_template("apology.html", message=message, code=400)

        # Ensure password and confirmation match
        if not form["password"] == form["confirmation"]:
            return render_template("apology.html", message="password and confirmation do not match", code=400)

        # hash password and insert data into database (we hebben nog geen database)
        hashed_password = generate_password_hash(form["password"])
        available = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                            username=form["username"], password=hashed_password)

        # Give error if username is not available
        if not available:
            return render_template("apology.html", message="username not available", code=400)

        session["user_id"] = (db.execute("SELECT id FROM users WHERE username= :username", username=form["username"])[0]["id"])

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/check", methods=["GET", "POST"])
def check():

    # Route is reached via GET
    if request.method == "GET":
        # Get username from register
        username = request.args.get("username")

        # Look for username in database
        usernames = db.execute("SELECT username FROM users WHERE username= :username", username=username)

        # Check if username is in database and longer than 1 character
        if len(usernames) == 0 and len(username) > 0:
            return jsonify(True)
        else:
            return jsonify(False)

    # Reached via POST
    else:

        # Get password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if password contains number(s)
        numbers = [str(number) for number in range(10) if str(number) in password]

        # Check length of password
        if len(password) >= 6 and len(password) < 20 and len(numbers) > 0 and password.find(" ") == -1:
            if password == confirmation:
                print(1)
                return jsonify(succes=True, confirmation=True)
            else:
                print(2, password, confirmation)
                return jsonify(succes=True, confirmation=False)
        else:
            return jsonify(succes=False)