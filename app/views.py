import sys
import time
sys.path.insert(0,'app')
sys.path.insert(0,'app/models')

from flask import render_template, redirect, url_for, request, flash
from app import app, lm
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from forms import LoginForm, CreateAccountForm
from user import User
import re
import time
import urllib2
import urllib
import simplejson
import dataMiner
from recommender import *
from Rule import *
from Users import *
from Media import *

last_mine_time = time.time()
last_mine_length = 0

@lm.user_loader
def load_user(username):
    return User(get_by_username(username))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    username = form.username.data
    password = form.password.data
    if validate(username, password):
        login_user(User(get_by_username(username)))
    return redirect(url_for("index"))

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/mine234785974890")
def mine_if_necessary():
    global last_mine_time
    global last_mine_length
    start = time.time()
    if start - last_mine_time > 10 * last_mine_length:
        dataMiner.dataMine()
        last_mine_time = start
        last_mine_length = time.time() - start
    return redirect(url_for("index"))	

@app.route("/Media.html", methods=["GET","POST"])
def media():
    try:
        if current_user.get_id():
            name = current_user.username
        else:
            name = None
        
        if request.method == "POST":
            print "POST"
            for input in request.form:
                if input != "name" and input != "type" and input != "last" and request.form[input] != "":
                    update(getID(request.form["name"], request.form["type"]), input.replace("_", " "), request.form[input])
            if getID(request.form["name"],request.form["type"], False) == None:
                raise
            update(getID(request.form["name"],request.form["type"], False), "url", getImageUrl(request.form["type"] + " " + request.form["name"]))
            return render_template("Media.html", name=name, media=find(getID(request.form["name"],request.form["type"], False)), last=request.form["last"])
        else:
            if getID(request.args["name"],request.args["type"], False) == None:
                raise
            return render_template("Media.html", name=name, media=find(getID(request.args["name"],request.args["type"], False)), last=request.args["last"])
    except:
        if "last" in request.args:
            if request.args["last"] == "Suggestions.html":
                return redirect(url_for("suggestions"))
        return redirect(url_for("index"))
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
        
        bookUrls = []
        showUrls = []
        movieUrls = []
        gameUrls = []
        
        for ID in get(current_user._id)["favorites"]:
            media = find(ID)
            if media["type"] == "book":
                books.append(media["title"])
                bookUrls.append(media["url"])
            if media["type"] == "tv show":
                shows.append(media["title"])
                showUrls.append(media["url"])
            if media["type"] == "movie":
                movies.append(media["title"])
                movieUrls.append(media["url"])
            if media["type"] == "videogame":
                games.append(media["title"])
                gameUrls.append(media["url"])
        return render_template("Index.html", name=current_user.username, books=books, bookUrls=bookUrls, shows=shows, showUrls=showUrls, movies=movies, movieUrls=movieUrls, games=games, gameUrls=gameUrls)   

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
    if (get_by_username(username) == None and re.match("^[A-Za-z0-9_-]+$", username) and re.match("^[A-Za-z0-9_-]+$", password)):
        add_user(username, password)
        login_user(User(get_by_username(username)))
        for book in filter(None, request.form.getlist("book")):
            add_favorite(get_userID(username), getID(book, "book"))
        for show in filter(None, request.form.getlist("show")):
            add_favorite(get_userID(username), getID(show, "tv show"))
        for movie in filter(None, request.form.getlist("movie")):
            add_favorite(get_userID(username), getID(movie, "movie"))
        for game in filter(None, request.form.getlist("game")):
            add_favorite(get_userID(username), getID(game, "videogame"))
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

@app.route('/Save', methods=["GET", "POST"])
@login_required
def save():
    for book in filter(None, request.form.getlist("book")):
        add_favorite(current_user._id, getID(book, "book"))
    for show in filter(None, request.form.getlist("show")):
        add_favorite(current_user._id, getID(show, "tv show"))
    for movie in filter(None, request.form.getlist("movie")):
        add_favorite(current_user._id, getID(movie, "movie"))
    for game in filter(None, request.form.getlist("game")):
        add_favorite(current_user._id, getID(game, "videogame"))
    return redirect(url_for("index"))
    
#Suggestions routing
@app.route('/Suggestions.html',  methods=["GET", "POST"])
def suggestions():

    books = []
    shows = []
    movies = []
    games = []

    bookUrls = []  
    showUrls = []
    movieUrls = []
    gameUrls = []

    if current_user.get_id():
        for book in filter(None, request.form.getlist("book")):
            add_favorite(current_user._id, getID(book, "book"))
        for show in filter(None, request.form.getlist("show")):
            add_favorite(current_user._id, getID(show, "tv show"))
        for movie in filter(None, request.form.getlist("movie")):
            add_favorite(current_user._id, getID(movie, "movie"))
        for game in filter(None, request.form.getlist("game")):
            add_favorite(current_user._id, getID(game, "videogame"))

        recBooks = recommend_by_type(current_user._id, "book") 
        bookUrls = []       
        for ID in recBooks:
            book = find(ID)
            books.append(book["title"])
            bookUrls.append(book["url"])

        recShows = recommend_by_type(current_user._id, "tv show")        
        for ID in recShows:
            show = find(ID)
            shows.append(show["title"])
            showUrls.append(show["url"])

        recMovies = recommend_by_type(current_user._id, "movie")        
        for ID in recMovies:
            movie = find(ID)
            movies.append(movie["title"])
            movieUrls.append(movie["url"])

        recGames = recommend_by_type(current_user._id, "videogame")        
        for ID in recGames:
            game = find(ID)
            games.append(game["title"])
            gameUrls.append(game["url"])

        return render_template("Suggestions.html", name=current_user.username, books=books, bookUrls=bookUrls, shows=shows, showUrls=showUrls, movies=movies, movieUrls=movieUrls, games=games, gameUrls=gameUrls)
    else:
        #create list of ID's
        media_list = []         
        for book in filter(None, request.form.getlist("book")):
            media_list.append(getID(book, "book"))
        for show in filter(None, request.form.getlist("show")):
            media_list.append(getID(show, "tv show"))
        for movie in filter(None, request.form.getlist("movie")):
            media_list.append(getID(movie, "movie"))
        for game in filter(None, request.form.getlist("game")):
            media_list.append(getID(game, "videogame"))

        recBooks = recommend_anon_by_type(media_list, "book")        
        for ID in recBooks:
            book = find(ID)
            books.append(book["title"])
            bookUrls.append(book["url"])

        recShows = recommend_anon_by_type(media_list, "tv show")        
        for ID in recShows:
            show = find(ID)
            shows.append(show["title"])
            showUrls.append(show["url"])

        recMovies = recommend_anon_by_type(media_list, "movie")        
        for ID in recMovies:
            movie = find(ID)
            movies.append(movie["title"])
            movieUrls.append(movie["url"])

        recGames = recommend_anon_by_type(media_list, "videogame")  
        for ID in recGames:
            game = find(ID)
            games.append(game["title"])
            gameUrls.append(game["url"])

        return render_template("Suggestions.html", name=None, books=books, bookUrls=bookUrls, shows=shows, showUrls=showUrls, movies=movies, movieUrls=movieUrls, games=games, gameUrls=gameUrls, submittedBooks=filter(None, request.form.getlist("book")),submittedShows=filter(None, request.form.getlist("show")),submittedMovies=filter(None, request.form.getlist("movie")),submittedGames=filter(None, request.form.getlist("game")))