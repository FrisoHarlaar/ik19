import os, urllib.request, json, urllib.parse, requests, random
from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):

    # make route require login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/index")
        return f(*args, **kwargs)
    return decorated_function

def new_question():

        # Gets a question from the opentdb database.
        with urllib.request.urlopen("https://opentdb.com/api.php?amount=1") as url:
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