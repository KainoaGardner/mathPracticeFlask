from flask import render_template, redirect, flash, url_for, session, request
from datetime import date

from app import app, db
from app.forms import User
from app.game import makeEquation


@app.route("/", methods=["GET", "POST"])
@app.route("/user", methods=["GET", "POST"])
def user():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    user = User.query.filter_by(username=username).first()

    if request.method == "POST":
        if "light" in request.form:
            user.theme = "light"
        if "dark" in request.form:
            user.theme = "dark"

        db.session.commit()

        return redirect(url_for("user"))

    if user.totalProblems != 0:
        percent = int((user.totalCorrect / user.totalProblems) * 100)
    else:
        percent = 0
    user.totalPercent = percent

    return render_template("user.html", user=user)


@app.route("/play", methods=["GET", "POST"])
def play():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user = User.query.filter_by(username=username).first()

    if request.method == "POST":
        equation = session["equation"]
        score = session["score"].copy()
        history = session["history"].copy()
        if "answer" in request.form:
            input = request.form["input"]
            answer = round(eval(equation), 2)
            score[1] += 1

            user.totalProblems += 1
            if int(input) == answer:
                result = "Correct"
                score[0] += 1
                user.totalCorrect += 1
                history.insert(0, (f"{equation} = {answer}", 1))
            else:
                result = "Incorrect"
                history.insert(0, (f"{equation} = {answer}", 0))
            percent = int((score[0] / score[1]) * 100)
            score[2] = percent

            if len(history) > 10:
                history.pop()

            session["result"] = result
            session["score"] = score
            session["equation"] = equation
            session["answer"] = answer
            session["history"] = history

            return redirect(url_for("playAnswer"))

        elif "next" in request.form:
            result = session["result"]
            equation = session["equation"]
            answer = eval(equation)

            score[1] += 1
            user.totalProblems += 1

            if result == "Correct":
                score[0] += 1
                user.totalCorrect += 1
                history.insert(0, (f"{equation} = {answer}", 1))
            else:
                history.insert(0, (f"{equation} = {answer}", 1))
            percent = int((score[0] / score[1]) * 100)
            score[2] = percent

            if len(history) > 10:
                history.pop()

            session["score"] = score
            session["history"] = history
            db.session.commit()
            return redirect(url_for("play"))

        elif "apply" in request.form:

            print(request.form["problemType"])
            settings = {
                "digits": request.form["digits"],
                "problemType": request.form["problemType"],
            }
            session["settings"] = settings
            problemType = None
            return redirect(url_for("play"))

    score = session["score"]

    percent = 0
    if score[1] != 0:
        percent = int((score[0] / score[1]) * 100)

    score[2] = percent

    equation = makeEquation(
        int(session["settings"]["digits"]), session["settings"]["problemType"]
    )
    session["equation"] = equation
    history = session["history"]
    settings = session["settings"]
    username = session["username"]
    user = User.query.filter_by(username=username).first()

    return render_template(
        "play.html",
        score=score,
        equation=equation,
        history=history,
        settings=settings,
        user=user,
    )


@app.route("/playAnswer", methods=["GET", "POST"])
def playAnswer():
    if request.method == "POST":
        return redirect(url_for("play"))
    score = session["score"]
    equation = session["equation"]
    result = session["result"]
    answer = session["answer"]
    history = session["history"]

    return render_template(
        "playAnswer.html",
        score=score,
        equation=equation,
        result=result,
        answer=answer,
        history=history,
        user=user,
    )


@app.route("/playSetup")
def playSetup():

    score = [0, 0, 0]
    problemType = "+-"
    digits = 2
    session["score"] = score
    session["history"] = []
    settings = {
        "digits": "2",
        "problemType": "+-",
    }
    session["settings"] = settings

    return redirect(url_for("play"))


@app.route("/login", methods=["GET", "POST"])
def login():
    session.permanent = True
    if "username" in session:
        flash(f"You are already logged in")
        return redirect(url_for("user"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        foundUser = User.query.filter_by(username=username).first()
        if foundUser and (
            foundUser.username == username and foundUser.password == password
        ):
            session["username"] = username
            flash(f"You logged in as {username}")
            return redirect(url_for("user"))
        else:
            flash("User not found")
    return render_template("login.html")


@app.route("/logout")
def logout():

    if "username" in session:
        session.pop("username", None)
        session.pop("score", None)
        session.pop("equation", None)
        session.pop("result", None)
        flash(f"You have been logged out")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    username = session["username"]
    user = User.query.filter_by(username=username).first()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username and password:
            foundUser = User.query.filter_by(username=username).first()
            if foundUser:
                flash(f"There is already a user named {username}")
                return render_template("register.html")

            registerDate = date.today()
            user = User(username, password, registerDate)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user"))

    return render_template("register.html")


@app.route("/clearDB")
def clearDB():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
        db.session.commit()
    return redirect(url_for("user"))


@app.route("/resetStats")
def resetStats():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    user = User.query.filter_by(username=username).first()
    user.totalCorrect = 0
    user.totalProblems = 0
    user.totalPercent = 0
    db.session.commit()
    if "score" in session:
        session.pop("score", None)
        session.pop("equation", None)
        session.pop("result", None)

    return redirect(url_for("user"))


@app.route("/admin")
def admin():
    users = User.query.all()

    username = session["username"]
    user = User.query.filter_by(username=username).first()

    return render_template("admin.html", users=users)
