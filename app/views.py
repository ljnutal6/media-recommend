import sys
sys.path.insert(0, 'app')
sys.path.insert(0, 'app/models')

from flask import render_template, redirect, url_for, request, flash
from app import app, lm
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from forms import LoginForm, CreateAccountForm
from user import User
import re

@lm.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    username = form.username.data
    password = form.password.data
    if User.validate(username, password):
        login_user(User.get(username))
    return redirect(url_for("index"))

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))

#Index Routing
@app.route('/')
@app.route('/index.html')
@app.route('/Index.html')
def index():
    return render_template("Index.html", name=current_user.get_id())

#Try It Now routing
@app.route('/TryItNow.html')
def tryItNow():
    return render_template("TryItNow.html", name=current_user.get_id())

@app.route('/DoneWithAccount', methods=["GET","POST"])
def doneWithAccount():
    username = request.form["username"]
    password = request.form["password"]
    if (re.match("^[A-Za-z0-9_-]+$", username) and re.match("^[A-Za-z0-9_-]+$", password)):
        #add_user(username, password)
        #We'll have to add favorites here
        login_user(User.get(username))
        return redirect(url_for("index"))
    return render_template("CreateAccount.html", books=request.form.getlist("book"), shows=request.form.getlist("show"), movies=request.form.getlist("movie"), games=request.form.getlist("game"))

#Create Account routing
@app.route('/CreateAccount.html', methods=["GET","POST"])
def createAccount():
    form = CreateAccountForm(request.form)
    username = form.username.data
    password = form.password.data
    books = filter(None, request.form.getlist("book"))
    shows = filter(None, request.form.getlist("show"))
    movies = filter(None, request.form.getlist("movie"))
    games = filter(None, request.form.getlist("game"))
    if current_user.get_id():
        return redirect(url_for("index"))
    return render_template("CreateAccount.html", books=books, shows=shows, movies=movies, games=games)

#Suggestions routing
@app.route('/Suggestions.html',  methods=["GET", "POST"])
def suggestions():
    return render_template("Suggestions.html", name=current_user.get_id(), submittedBooks=filter(None, request.form.getlist("book")),submittedShows=filter(None, request.form.getlist("show")),submittedMovies=filter(None, request.form.getlist("movie")),submittedGames=filter(None, request.form.getlist("game")))





