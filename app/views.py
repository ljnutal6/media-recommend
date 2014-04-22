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
import urllib.request as urllib2
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
        print(get_by_username(username))
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

#Index Routing
@app.route('/')
@app.route('/index.html')
@app.route('/Index.html')
def index():
    #logout_user()
    print(current_user)
    if current_user.get_id():
        books = []
        shows = []
        movies = []
        games = []
        for ID in get(current_user._id)["favorites"]:
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
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' 
    +'v=1.0&q=barack%20obama')

    request = urllib2.Request(url, None, {'Referer': "http://localhost:5000/"})
    response = urllib2.urlopen(request)

    # Process the JSON string.
    results = simplejson.load(response)
	
    data = results['responseData']
    dataInfo = data['results']
    imageObject = dataInfo[0]
    imageUrl = imageObject['unescapedUrl']    
    print(imageUrl)

    return render_template("Index.html", name=None, imageName=imageUrl)

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
            bookSearch = "book " + book["title"]
            #bookUrls.append(getImageUrl(bookSearch))

        recShows = recommend_by_type(current_user._id, "tv show")        
        for ID in recShows:
            show = find(ID)
            shows.append(show["title"])
            showSearch = "show " + show["title"]
            #showUrls.append(getImageUrl(showSearch))

        recMovies = recommend_by_type(current_user._id, "movie")        
        for ID in recMovies:
            movie = find(ID)
            movies.append(movie["title"])
            movieSearch = "movie " + movie["title"]
            #movieUrls.append(getImageUrl(movieSearch))

        recGames = recommend_by_type(current_user._id, "videogame")        
        for ID in recGames:
            game = find(ID)
            games.append(game["title"])
            gameSearch = "game " + movie["title"]
            #gameUrls.append(getImageUrl(gameSearch))


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
            bookSearch = "book " + book["title"]
            #bookUrls.append(getImageUrl(bookSearch))

        recShows = recommend_anon_by_type(media_list, "tv show")        
        for ID in recShows:
            show = find(ID)
            shows.append(show["title"])
            showSearch = "show " + show["title"]
            #showUrls.append(getImageUrl(showSearch))

        recMovies = recommend_anon_by_type(media_list, "movie")        
        for ID in recMovies:
            movie = find(ID)
            movies.append(movie["title"])
            movieSearch = "movie " + movie["title"]
            #movieUrls.append(getImageUrl(movieSearch))

        recGames = recommend_anon_by_type(media_list, "videogame")  
        for ID in recGames:
            game = find(ID)
            games.append(game["title"])
            gameSearch = "game " + game["title"]
            #gameUrls.append(getImageUrl(gameSearch))

        return render_template("Suggestions.html", name=None, books=books, bookUrls=bookUrls, shows=shows, showUrls=showUrls, movies=movies, movieUrls=movieUrls, games=games, gameUrls=gameUrls, submittedBooks=filter(None, request.form.getlist("book")),submittedShows=filter(None, request.form.getlist("show")),submittedMovies=filter(None, request.form.getlist("movie")),submittedGames=filter(None, request.form.getlist("game")))

#Rest Service used through Google API that returns a JSON file for image search
def getImageUrl(bookSearch):
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' 
    +'v=1.0&q=' + bookSearch)
    imageRequest = urllib2.Request(url, None, {'Referer': "http://localhost:5000/"})
    response = urllib2.urlopen(imageRequest)
    # Process the JSON string.
    results = simplejson.load(response)
    data = results['responseData']
    dataInfo = data['results']
    imageObject = dataInfo[0]
    imageUrl = imageObject['unescapedUrl']    
    print(imageUrl)
    return imageUrl


