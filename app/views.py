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
    if current_user.get_id():
        books = []
        shows = []
        movies = []
        games = []
        for ID in User.get(current_user.get_id())["favorites"]:
            media = find(ID)
            if media["type"] == "book":
                books.append(media["title"])
            if media["type"] == "tv show":
                shows.append(media["title"])
            if media["type"] == "movie":
                movies.append(media["title"])
            if media["type"] == "videogame":
                games.append(media["title"])
        return render_template("Index.html", name=current_user.username, books=books, shows=shows, movies=movies, games=games)
    return render_template("Index.html", name=None)

#Try It Now routing
@app.route('/TryItNow.html')
def tryItNow():
    if current_user.get_id():
        return redirect(url_for("index"))
    return render_template("TryItNow.html", name=None)

@app.route('/DoneWithAccount', methods=["GET","POST"])
def doneWithAccount():
    username = request.form["username"]
    password = request.form["password"]
    if (re.match("^[A-Za-z0-9_-]+$", username) and re.match("^[A-Za-z0-9_-]+$", password)):
        add_user(username, password)
        login_user(User.get(username))
        for book in filter(None, request.form.getlist("book")):
            add_favorite(get_userID(username, password), getID(book, "book"))
        for show in filter(None, request.form.getlist("show")):
            add_favorite(get_userID(username, password), getID(book, "tv show"))
        for movie in filter(None, request.form.getlist("movie")):
            add_favorite(get_userID(username, password), getID(book, "movie"))
        for game in filter(None, request.form.getlist("game")):
            add_favorite(get_userID(username, password), getID(book, "videogame"))
        return redirect(url_for("index"))
    return render_template("CreateAccount.html", books=filter(None, request.form.getlist("book")), shows=filter(None, request.form.getlist("show")), movies=filter(None, request.form.getlist("movie")), games=filter(None, request.form.getlist("game")))

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
    if current_user.get_id():
        current_user.add_books(filter(None, request.form.getlist("book")))
        current_user.add_shows(filter(None, request.form.getlist("show")))
        current_user.add_movies(filter(None, request.form.getlist("movie")))
        current_user.add_games(filter(None, request.form.getlist("game")))
        current_user.save()

        books = get_books(current_user.favorites)
        shows = get_shows(current_user.favorites)
        movies = get_movies(current_user.favorites)
        games = get_games(current_user.favorites)

        return render_template("Suggestions.html", name=current_user.username, books=books, shows=shows, movies=movies, games=games)
    else:
        books = get_books(current_user.favorites)
        shows = get_shows(current_user.favorites)
        movies = get_movies(current_user.favorites)
        games = get_games(current_user.favorites)

        return render_template("Suggestions.html", name=None, books=books, shows=shows, movies=movies, games=games, submittedBooks=filter(None, request.form.getlist("book")),submittedShows=filter(None, request.form.getlist("show")),submittedMovies=filter(None, request.form.getlist("movie")),submittedGames=filter(None, request.form.getlist("game")))





