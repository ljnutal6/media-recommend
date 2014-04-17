from flask import render_template, redirect, url_for, request, flash
from app import app, lm
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from forms import LoginForm

@lm.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login",  methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    username = form.username.data
    password = form.password.data
    print username
    print password
    flash("Logged in successfully.")
    return redirect(request.args.get("next") or url_for("index"))
    

#Index Routing
@app.route('/')
@app.route('/index.html')
@app.route('/Index.html')
def index():
    return render_template("Index.html")

#Try It Now routing
@app.route('/TryItNow.html')
def tryItNow():
    return render_template("TryItNow.html")

#Create Account routing
@app.route('/CreateAccount.html')
def createAccount():
    return render_template("CreateAccount.html")

#Edit Media routing
@app.route('/EditMedia.html')
def editMedia():
    return render_template("EditMedia.html")

#Suggestions routing
@app.route('/Suggestions.html')
def suggestions():
    return render_template("Suggestions.html")

#More Suggestions routing
@app.route('/MoreSuggestions.html')
def moreSuggestions():
    return render_template("MoreSuggestions.html")





