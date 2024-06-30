import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):  # This taken From CS50 finance/helper.py
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")  # TODO The index of the page
@login_required
def index():
    tasks = db.execute(
        "SELECT * FROM tasks WHERE id = ?", session["user_id"]
    )
    return render_template("index.html", tasks=tasks)


@app.route("/login", methods=["GET", "POST"])  # TODO login function -- DONE --
def login():

    # make sure no session is active
    session.clear()

    # confirm appropriate input
    if request.method == "POST":
        name = request.form.get("username")
        if not name:
            error = "MISSING NAME!"
            return render_template("error.html", error=error)
        password = request.form.get("password")
        if not password:
            error = "MISSING PASSWORD!"
            return render_template("error.html", error=error)

        # query database for the user's data
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", name
        )

        # check correct password
        if len(user) != 1 or not check_password_hash(
            user[0]['hash'], password
        ):
            error = "invalid user name and/or password!"
            return render_template("error.html", error=error)

        # logging in
        session["user_id"] = user[0]['id']

        # redirect to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")  # TODO logout function -- DONE --
def logout():

    # clear the session will logout
    session.clear()

    # redirect to the index to login cause it is required
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])  # TODO register function -- DONE --
def register():

    if request.method == "POST":

        # confirm appropriate input
        name = request.form.get("username")
        if not name:
            error = "MISSING NAME!"
            return render_template("error.html", error=error)
        password = request.form.get("password")
        if not password:
            error = "MISSING PASSWORD!"
            return render_template("error.html", error=error)
        confirmation = request.form.get("confirmation")
        if not confirmation:
            error = "MISSING PASSWORD!"
            return render_template("error.html", error=error)
        elif password != confirmation:
            error = "Password and Confirmation don't match!"
            return render_template("error.html", error=error)

        # confirm new account and add it to the database
        else:
            try:
                db.execute(
                    "INSERT INTO users (username, hash) VALUES (?, ?)", name, generate_password_hash(password)
                )

                session["user_id"] = db.execute(
                    "SELECT id FROM users WHERE username = ?", name
                )[0]['id']
                # print ("DONE")
                return redirect("/")
            except (KeyError, IndexError, ValueError):
                error = "NAME IS NOT AVAILABLE"
                return render_template("error.html", error=error)
    else:
        return render_template("register.html")


@app.route("/addtask", methods=["GET", "POST"])  # TODO generate TO-DO function
@login_required
def todo():
    if request.method == "POST":
        task = request.form.get("task")
        if not task:
            error = "Must Enter a task"
            return render_template("error.html", error=error)
        db.execute(
            "INSERT INTO tasks (id, task) VALUES (?, ?)", session["user_id"], task
        )
        return redirect("/")
    else:
        return render_template("add.html")


@app.route("/check_state", methods=["POST"])
@login_required
def check_state():
    if request.method == "POST":
        checkboxs = request.form.getlist("checkbox")
        print(checkboxs)
        if checkboxs != ['']:
            if len(checkboxs) == 2:
                db.execute(
                    "UPDATE tasks SET checked = 1 WHERE task_id = ?", checkboxs[0]
                )
            elif len(checkboxs) == 1:
                db.execute(
                    "UPDATE tasks SET checked = 0 WHERE task_id = ?", checkboxs[0]
                )
            return redirect("/")
        else:
            return redirect("/")


@app.route("/edit_task", methods=["Get", "POST"])
@login_required
def edit():
    if request.method == "POST":
        task_id = request.form.get("task_id")
        if not task_id:
            error = "NO WAY YOU HACKER!!1"
            return render_template("error.html", error=error)
        taskids = db.execute(
            "SELECT task_id FROM tasks WHERE id = ?", session["user_id"]
        )
        print(taskids)
        task_list = []
        for taskid in taskids:
            task_list.append(taskid['task_id'])
        if int(task_id) not in task_list:
            error = "NO WAY YOU HACKER!!2"
            return render_template("error.html", error=error)
        task = request.form.get("task")
        print(task)
        if not task:
            error = "MUST CONTAIN A TASK!!3"
            return render_template("error.html", error=error)
        db.execute(
            "UPDATE tasks SET task = ? WHERE task_id = ?", task, task_id
        )
        return redirect("/")
    
    else:
        task_id = request.args.get('task_id')
        task = db.execute(
            "SELECT task FROM tasks WHERE task_id = ?", task_id
        )[0]['task']
        print(task)
        return render_template("edit.html", task=task, task_id=task_id)



@app.route("/edit", methods=["POST"])
@login_required
def hand():
    task_id = request.form.get("task_id")
    print(task_id)
    if not task_id:
        error = "NO WAY YOU HACKER!!"
        return render_template("error.html", error=error)
    tasks = db.execute(
        "SELECT task_id FROM tasks WHERE id = ?", session["user_id"]
    )
    print(tasks)
    task_list = []
    for task in tasks:
        task_list.append(task['task_id'])
    print(task_list)
    if int(task_id) not in task_list:
        error = "NO WAY YOU HACKER!!"
        return render_template("error.html", error=error)
    print("task_id is " + task_id)
    return redirect("/edit_task?task_id=" + task_id )
