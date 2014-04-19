import sys
sys.path.insert(0, 'app')
sys.path.insert(0, 'app/models')

from flask import render_template, redirect, url_for, request, flash
from app import app, lm
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from forms import LoginForm, CreateAccountForm
'''from user import User'''

@lm.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login",  methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    username = form.username.data
    password = form.password.data
    if User.validate(username, password):
        login_user(User.get(username))
    return redirect(url_for("index"))

@app.route("/logout")
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

#Create Account routing
@app.route('/CreateAccount.html', methods=["GET","POST"])
def createAccount():
    form = CreateAccountForm(request.form)
    username = form.username.data
    password = form.password.data
    print(username)
    print(password)
    if current_user.get_id():
        return redirect(url_for("index"))
    return render_template("CreateAccount.html")

#Suggestions routing
@app.route('/Suggestions.html',  methods=["GET", "POST"])
def suggestions():
    return render_template("Suggestions.html", name=current_user.get_id(), submittedBooks=filter(None, request.form.getlist("book")),submittedShows=filter(None, request.form.getlist("show")),submittedMovies=filter(None, request.form.getlist("movie")),submittedGames=filter(None, request.form.getlist("game")))





