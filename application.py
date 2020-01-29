import os, urllib.request
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, new_question, get_db, update_db, insdel_db, setup
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

# This is the main page where the user can pick a game mode.
def dashboard():

    # This is variable checks what game mode the player wants to play.
    # It's default value is set to false here.
    session["mirror"] = False

    # This variable stops the user from refreshing the page on the first question.
    # It gets set to true when the game is started.
    session["timer"] = False

    # Query database for userdata
    rows = get_db(["username", "highscore", "highscore_mirror"], "users", "id", session["user_id"])

    # Take the username and highscore
    username, highscore, highscore_mirror = rows[0]["username"], rows[0]["highscore"], rows[0]["highscore_mirror"]
    return render_template("dashboard.html", username=username, highscore=highscore, highscore_mirror=highscore_mirror)


@app.route("/index")

# Redirect to the index page if not logged in.
def index():

    # Loads the index page.
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])

# This function allows the user to log in.
def login():

    # Forget any user_id.
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect).
    if request.method == "GET":
        return render_template("auth/login.html")

    # User reached route via POST (as by submitting a form via POST).
    else:
        # Assign form input to local dict
        form = {"username": request.form.get("username"), "password": request.form.get("password")}

        # Ensure form was fully filled out.
        for form_item in form.items():
            if form_item[1] == '':
                message = "must provide " + form_item[0]
                return render_template("apology.html", message=message, code=400)

        # Query database for username.
        rows = get_db(["*"], "users", "username", form["username"])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], form["password"]):
            return render_template("apology.html", message="invalid username and/or password", code=400)

        # Remember which user has logged in.
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page,
        return redirect("/")


@app.route("/check_login", methods=["POST"])

# This function gives feedback to the user when logging in.
def check_login():

    # Grabs the user inputs.
    username = request.form.get("username")
    password = request.form.get("password")

    # look for username in database
    rows = get_db(["*"], "users", "username", username)

    # check if username exists and if password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/register", methods=["GET", "POST"])

# This function allows the user to register.
def register():

    # User reached route via POST.
    if request.method == "POST":

        # Assign form input to local dict.
        form = {"username": request.form.get("username"), "password": request.form.get("password"), "confirmation": request.form.get("confirmation")}

        # Ensure form was fully filled out.
        for form_item in form.items():
            if form_item[1] == '':
                message = "must provide " + form_item[0]
                return render_template("apology.html", message=message, code=400)

        # Ensure password and confirmation match.
        if not form["password"] == form["confirmation"]:
            return render_template("apology.html", message="password and confirmation do not match", code=400)

        # check if password contains any numbers.
        numbers = any([char.isdigit() for char in form["password"]])

        # check if password meets requirements.
        if len(form["password"]) < 6 or len(form["password"]) >= 20 or form["password"].find(" ") != -1 or not numbers:
            return render_template("apology.html", message="password does not meet the requirements", code=400)

        # hash password and insert data into database.
        hashed_password = generate_password_hash(form["password"])
        available = insdel_db("available", form["username"], hashed_password)

        # Give error if username is not available.
        if not available:
            return render_template("apology.html", message="username not available", code=400)

        session["user_id"] = (get_db(["id"], "users", "username", form["username"])[0]["id"])

        return redirect("/")

    # User reached route via GET.
    else:
        return render_template("auth/register.html")


@app.route("/check_username", methods=["GET"])

# This function gives feedback to the user when registering.
def check_username():

    # Get username from form.
    username = request.args.get("username")

    # Look for username in database.
    usernames = get_db(["username"], "users", "username", username)

    # Check if username is in database and longer than 1 character.
    if len(usernames) == 0 and len(username) > 1:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/logout")
@login_required

# This function allows the user to log out.
def logout():

    # clear session
    session.clear()

    # return to homescreen
    return redirect("/")


@app.route("/leaderboard")

# This function renders the main leaderboard.
def leaderboard():
    # Show the leaderboard of the 50 best players
    highscores = get_db(["*"], "users", None, None, ["highscore DESC", "date"])
    highscores = [(i+1, highscores[i]) for i in range(len(highscores))]
    # Only 50 best players on leaderboard
    if len(highscores) > 50:
        highscores = [(i, highscores[i]) for i in range(1, 51)]

    return render_template("game/leaderboard.html", highscores=highscores)


@app.route("/leaderboard_mirror")

# This function renders the mirrored leaderboard.
def leaderboard_mirror():
    "Show the leaderboard of the 50 best players in Mirror mode"
    highscores = get_db(["*"], "users", None, None, ["highscore_mirror DESC", "date"])
    highscores = [(i+1, highscores[i]) for i in range(len(highscores))]
    if len(highscores) > 50:
        highscores = [(i+1, highscores[i]) for i in range(50)]

    return render_template("game/leaderboard_mirror.html", highscores=highscores)


@app.route("/friends", methods=["GET"])
@login_required

# This function allows the user to add and delete friends.
# It also allows users to see their friend's highscores.
def friends():

    # get current users friends.
    friends = set([friend["friendname"] for friend in get_db(["friendname"], "friends", "user_id", session["user_id"])])

    # get highscores from every friend.
    highscores = sum([get_db(["username", "highscore", "date"], "users", "username", friend) for friend in friends], [])

    # sort friend highscores.
    highscores = sorted(highscores, key=lambda k:k["highscore"], reverse=True)

    # get users highscore and date.
    yourscore = get_db(["highscore", "date"], "users", "id", session["user_id"])
    return render_template("friends/friends.html", highscores=highscores, yourscore=yourscore[0])


@app.route("/friends_mirror", methods=["GET"])
@login_required

# Does the same as the above, but shows mirrored scored instead.
def friends_mirror():

    # get current users friends.
    friends = set([friend["friendname"] for friend in get_db(["friendname"], "friends", "user_id", session["user_id"])])

    # get highscores from every friend.
    highscores = sum([get_db(["username", "highscore_mirror", "date"], "users", "username", friend) for friend in friends], [])

    # sort friend highscores.
    highscores = sorted(highscores, key=lambda k:k["highscore_mirror"], reverse=True)

    # get users highscore and date.
    yourscore = get_db(["highscore_mirror", "date"], "users", "username", session["user_id"])
    return render_template("friends/friends_mirror.html", highscores=highscores, yourscore=yourscore[0])


@app.route("/delete_friend", methods=["GET", "POST"])
@login_required

# Allows the user to delete a friend.
def delete_friend():

    # User reached route via POST.
    if request.method == "POST":
        friendname = request.form.get("friendname")

        # Delete friend from database.
        insdel_db("del_friends", session["user_id"], friendname)

        return redirect("/friends")

    # User reached route via GET.
    else:

        # Get friends from database.
        friends = set([friend["friendname"] for friend in get_db(["friendname"], "friends", "user_id", session["user_id"])])

        return render_template("friends/delete_friend.html", friends=friends)


@app.route("/add_friend", methods=["GET", "POST"])
@login_required

# Allows the user to add a friend.
def add_friend():

    # User reached route via POST.
    if request.method == "POST":

        # Gets the filled in name and looks it up in the database.
        friendname = request.form.get("friendname")
        friend = get_db(["username"], "users", "username", friendname)

        # If the friend isn't found in the database, return an error.
        if not friend:
            return render_template("apology.html", message="Username does not exist!", code=400)
        friends = get_db([""], "", "", [session["user_id"], friendname], "friends")

        # If the user is already friends with this person, return an error.
        if friends:
            return render_template("apology.html", message="You already have this friend", code=400)

        # Else add the friend to the users friends list.
        insdel_db("ins_friends", session["user_id"], friendname)
        return redirect("/friends")

    # Render the html page before POSTing.
    else:
        return render_template("friends/add_friend.html")


@app.route("/check_friend", methods=["POST"])

# Gives feedback to the user when adding a friend.
def check_friend():

    # get friendname and user id
    friendname = request.form.get("friendname")
    user_id = session["user_id"]

    # check if friendname is already in friend database
    friends = get_db([""], "", "", [session["user_id"], friendname], "friends")

    # check if friendname is the current user
    username = get_db(["username"], "users", "id", user_id)[0]["username"]

    # friendname is already users friend
    if friends:
        return jsonify(False, True)

    # friendname is the current user
    elif friendname == username:
        return jsonify(True, False)

    # friendname is good
    else:
        return jsonify(True, True)

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    # Query database for user
    profiles = get_db(["username", "highscore"], "users", "id", session["user_id"])

    # Select for user: username and highscore
    for profile in profiles:
        username = profile["username"]
        highscore = profile["highscore"]

    users = get_db(["id"], "users", None, None, ["highscore DESC, date"])
    rank = 0
    for user in users:
        rank += 1
        if user["id"] == session["user_id"]:
            break

    return render_template("profile.html", username=username, highscore=highscore, rank=rank)


@app.route("/change_username", methods=["GET", "POST"])
@login_required
def change_username():
    """Change username user"""
    # User reached route via "GET"
    if request.method == "GET":
        return render_template("auth/change_username.html")

    # User reached route via POST
    else:

        # Assign form input to local dict
        new_username = request.form.get("new username")

        # Ensure form was fully filled out
        if new_username == '':
            return render_template("apology.html", message="must provide username", code=400)

        # Ensure new username does not already exists
        if get_db(["username"], "users", "username", new_username):
            return render_template("apology.html", message="new username not available", code=400)

        # Set new username in database
        update_db("username", session["user_id"], new_username)

        return render_template("index.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password user"""
    # User reached route via "GET"
    if request.method == "GET":
        return render_template("auth/change_password.html")

    # User reached route via POST
    else:

        # Assign form input to local dict
        form = {"password": request.form.get("password"),
                "new password": request.form.get("new password"),
                "password confirmation": request.form.get("password confirmation")}

        # Ensure form was fully filled out
        for form_item in form.items():
            if form_item[1] == '':
                message = "must provide " + form_item[0]
                return render_template("apology.html", message=message, code=400)

        # Ensure old password and new password are not the same
        if form["password"] == form["new password"]:
            return render_template("apology.html", message="old password and new password can't be the same", code=400)

        # Ensure new password and confirmation match
        if form["new password"] != form["password confirmation"]:
            return render_template("apology.html", message="new password and confirmation don't match", code=400)

        # Set new password in database
        hash = generate_password_hash(form["new password"])
        update_db("hash", session["user_id"], hash)

        return render_template("index.html")


@app.route("/check_changepass", methods=["POST"])
def check_changepass():

    # retrieve user input and id
    old_password = request.form.get("oldpassword")
    user_id = session["user_id"]

    # look for user_id in database
    old_hash = get_db(['hash'], "users", "id", user_id)[0]["hash"]

    # check if username exists and if password is correct
    if check_password_hash(old_hash, old_password):
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/triviagame", methods=["GET", "POST"])
@login_required
def triviagame():
    # When the user first starts up the game.
    if request.method == "GET" and session["timer"] == False:

        # Clears the session (except for the user ID) so the user can start a new game.
        user_id = session["user_id"]
        mirror = session["mirror"]
        session.clear()
        session["mirror"] = mirror
        session["user_id"] = user_id

        # Returns the required data for the question.
        data = new_question("easy")

        # Set standard variables for the start of the game.
        session["correct_answer"] = data["correct_answer"]
        session["lives"] = 4
        session["score"] = 0
        session["timer"] = True
        session["duration"] = 30000

        if session["mirror"] == True:
            return render_template("game/mainReverse.html",
            lives=session["lives"], question=data["question"], answers=data["all_answers"], score=session["score"], duration=session["duration"])
        return render_template("game/main.html",
        lives=session["lives"], question=data["question"], answers=data["all_answers"], score=session["score"], duration=session["duration"])

    # After answering the first answer.
    if request.method == "POST":

        # Checks if the user answered the question correctly.
        if request.form.get("answer") == "setup":
            return setup(True)
        elif request.form.get("answer") != session["correct_answer"]:
            session["lives"] -= 1

            # If the user is out of lives it's game over.
            if session["lives"] <= 0:
                return jsonify(False)
        session["score"] += 1
        return setup()

    # Activates when page is refreshed
    else:
        return redirect("/game_over")

@app.route("/reverseTriviagame", methods=["GET", "POST"])
@login_required
def reverseTriviagame():
    session["mirror"] = True
    return redirect("/triviagame")


@app.route("/game_over", methods=["GET", "POST"])
@login_required
def game_over():

    # stop game
    session["timer"] = False

    if session["mirror"] == False:
        # get users highscore
        highscore = get_db(["highscore"], "users", "id", session["user_id"])[0]["highscore"]
         # show new record screen if current score exceeds highscore
        if session["score"] > highscore:
            update_db("highscore", session["user_id"], session["score"])
            return render_template("game/newrecord.html", score=session["score"], mode="/triviagame")
        return render_template("game/game_over.html", mode="/triviagame")

    # Do the same as the above, but for mirror mode.
    else:
        highscore = get_db(["highscore_mirror"], "users", "id", session["user_id"])[0]["highscore_mirror"]
        if session["score"] > highscore:
            update_db("highscore_mirror", session["user_id"], session["score"])
            return render_template("game/newrecord.html", score=session["score"], mode="/reverseTriviagame")
        return render_template("game/game_over.html", mode="/reverseTriviagame")