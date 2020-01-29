import os, urllib.request, json, urllib.parse, requests, random
from flask import redirect, render_template, request, session, jsonify
from functools import wraps
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///brainbrawlers.db")

def login_required(f):

    # make route require login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/index")
        return f(*args, **kwargs)
    return decorated_function

def new_question(difficulty):

        # Gets a question from the opentdb database.
        with urllib.request.urlopen(f"https://opentdb.com/api.php?amount=1&difficulty={difficulty}") as url:
            rows = json.loads(url.read().decode())

        # Takes the question and answers from the data
        data = dict()
        data["question"] = rows['results'][0]["question"]
        data["incorrect_answers"] = rows['results'][0]["incorrect_answers"]
        data["correct_answer"] = rows['results'][0]["correct_answer"]

        # Makes one list with all possible answers and shuffles it.
        data["all_answers"] = data["incorrect_answers"] + [data["correct_answer"]]
        random.shuffle(data["all_answers"])
        return data

def setup(load=False):
    # Returns the required data for the question.
    if session["score"] <= 10:
        data = new_question("easy")
    elif session["score"] <= 20:
        data = new_question("medium")
    else:
        data = new_question("hard")

    # Takes the question and answers from the data
    session["correct_answer"] = data["correct_answer"]

    # The player gains a life and the time window shrinks after 10 questions.
    if session["duration"] >= 10000 and session["score"] % 10 == 0 and session["score"] != 0:
        session["duration"] -= 5000
        if session["lives"] < 4:
            session["lives"] += 1
    return jsonify(lives=session["lives"], question=data["question"], answers=data["all_answers"], score=session["score"], duration=session["duration"], load=load)


# Function to easily get data from the database.
# Items need to be a list of the requested item(s).
def get_db(items, table, key, value, order=None):
    string = "SELECT "

    if order == "friends":
        return db.execute("SELECT friendname FROM friends WHERE user_id= :user_id AND friendname= :friendname"
        , user_id=value[0], friendname=value[1])

    for item in items:
        if item != items[0]:
            string += ", "

        string += str(item)

    string += " FROM " + table

    if key != None and value != None:
        string += " WHERE " + key + "= :key"

    if order != None:
        string += " ORDER BY"
        for item in order:
           string += " " + item
           if item != order[-1]:
               string += ","
        string += ";"

    if key != None:
        return db.execute(string, key=str(value))
    return db.execute(string)

def update_db(command, key1=None, key2=None):
    if command == "username":
        return db.execute("UPDATE users SET username = :username WHERE id = :user_id", user_id=key1, username=key2)
    elif command == "hash":
        return db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=key1, hash=key2)
    elif command == "highscore":
        return db.execute("UPDATE users SET highscore = :score, date = CURRENT_DATE WHERE id = :user_id",
                    user_id=key1, score=key2)
    elif command == "highscore_mirror":
        return db.execute("UPDATE users SET highscore_mirror = :score, date = CURRENT_DATE WHERE id = :user_id",
                    user_id=key1, score=key2)
    pass

def insdel_db(command, key1=None, key2=None):
    if command == "available":
        return db.execute("INSERT INTO users (username, hash, highscore, highscore_mirror) VALUES (:username, :password, :hs, :hs)",
                    username=key1, password=key2, hs=0)
    elif command == "del_friends":
        return db.execute("DELETE FROM friends WHERE user_id= :user_id AND friendname= :friendname", user_id=key1, friendname=key2)
    elif command == "ins_friends":
        return db.execute("INSERT INTO friends (user_id, friendname) VALUES (:user_id, :friendname)", user_id=key1, friendname=key2)