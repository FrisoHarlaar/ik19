import os, urllib.request, json, urllib.parse, requests, random
from flask import redirect, render_template, request, session
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

# Function to easily get data from the database.
# Items need to be a list of the requested item(s).
def get_db(items, table, key, value):
    string = "SELECT "

    for item in items:
        if item != items[0]:
            string += ", "

        string += str(item)
    string += " FROM " + table + " WHERE " + key + "= :key"
    return db.execute(string, key=str(value))