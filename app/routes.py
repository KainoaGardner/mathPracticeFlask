from flask import render_template, redirect, flash, url_for, session, request
from datetime import date

from app import app, db
from app.forms import User


@app.route("/")
@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    user = User.query.filter_by(username=username).first()

    return render_template("home.html", user=user)


@app.route("/play", methods=["GET", "POST"])
def play():
    if "score" in session:
        score = session["score"]
    else:
        score = [0, 0, 0]

    return render_template("play.html", score=score)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.permanent = True
    if "username" in session:
        flash(f"You are already logged in")
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        foundUser = User.query.filter_by(username=username).first()
        if foundUser and (
            foundUser.username == username and foundUser.password == password
        ):
            session["username"] = username
            flash(f"You logged in as {username}")
            return redirect(url_for("home"))
        else:
            flash("User not found")
    return render_template("login.html")


@app.route("/logout")
def logout():

    if "username" in session:
        session.pop("username", None)
        flash(f"You have been logged out")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username and password:
            foundUser = User.query.filter_by(username=username).first()
            if foundUser:
                flash(f"There is already a user named {username}")
                return render_template("register.html")

            registerDate = date.today()
            user = User(username, password, registerDate, 0, 0)
            db.session.add(user)
            db.session.commit()

    return render_template("register.html")


@app.route("/clearDB")
def clearDB():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)
