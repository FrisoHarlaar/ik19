import os
import urllib.request, json
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from tempfile import mkdtemp

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# The index page.
@app.route("/")
@login_required
def dashboard():
    # Query database for userdata
    rows = db.execute("SELECT * FROM users WHERE id = :user_id",
                    user_id=session["user_id"])
    # Take the username and highscore
    username, highscore = rows[0]["username"], rows[0]["highscore"]
    return render_template("dashboard.html", username=username, highscore=highscore)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("auth/login.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
         # Assign form input to local dict
        form = {"username": request.form.get("username"), "password": request.form.get("password")}

         # Ensure form was fully filled out
        for form_item in form.items():
            if form_item[1] == '':
                message = "must provide " + form_item[0]
                return render_template("apology.html", message=message, code=400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                         username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html", message="invalid username and/or password", code=400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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
        available = db.execute("INSERT INTO users (username, hash, highscore) VALUES (:username, :password, :hs)",
                            username=form["username"], password=hashed_password, hs=0)

        # Give error if username is not available
        if not available:
            return render_template("apology.html", message="username not available", code=400)

        session["user_id"] = (db.execute("SELECT id FROM users WHERE username= :username", username=form["username"])[0]["id"])

        return redirect("/")

    # User reached route via GET
    else:
        return render_template("auth/register.html")


@app.route("/check", methods=["GET", "POST"])
def check():

    # Route is reached via GET
    if request.method == "GET":
        print(0)
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
            print(3)
            return jsonify(succes=False)


@app.route("/logout")
def logout():

    # clear session
    session.clear()

    # return to homescreen
    return redirect("/")


@app.route("/leaderboard")
def leaderboard():
    "Show the leaderboard of the 50 best players"
    highscores = db.execute("SELECT * FROM users ORDER BY highscore DESC, date;")
    return render_template("game/leaderboard.html", highscores=highscores)


@app.route("/triviagame", methods=["GET", "POST"])
def triviagame():
    if request.method == "GET":
        # Returns a dict within a list within a dict!!!
        with urllib.request.urlopen("https://opentdb.com/api.php?amount=1&difficulty=easy") as url:
            data = json.loads(url.read().decode())
        question = data['results'][0]["question"]
        lives=4
        return render_template("game/main.html", lives=lives, question=question)