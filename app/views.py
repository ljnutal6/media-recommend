from flask import render_template
from app import app

#Index Routing
@app.route('/')
@app.route('/index')
@app.route('/Index')
def index():
    return render_template("Index.html")

@app.route('/Index_files/jquery.min.js')
def indexFilesJQuery():
    return render_template("Index_files/jquery.min.js")

@app.route('/Index_files/bootstrap.min.js')
def indexFilesBootStrap():
    return render_template("Index_files/bootstrap.min.js")

#Try It Now routing
@app.route('/TryItNow')
def tryItNow():
    return render_template("TryItNow.html")

@app.route('/TryItNow_files/bootstrap.min.js')
def tryItNowBootstrap():
    return render_template("/TryItNow_files/bootstrap.min.js")

@app.route('/TryItNow_files/jquery.min.js')
def tryItNowJQuery():
    return render_template("/TryItNow_files/jquery.min.js")

#Create Account routing
@app.route('/CreateAccount')
def createAccount():
    return render_template("CreateAccount.html")

@app.route('/CreateAccount_files/bootstrap.min.js')
def createAccountBootstrap():
    return render_template("/TryItNow_files/bootstrap.min.js")

@app.route('/CreateAccount_files/jquery.min.js')
def createAccountJQuery():
    return render_template("/TryItNow_files/jquery.min.js")

#Edit Media routing
@app.route('/EditMedia')
def editMedia():
    return render_template("EditMedia.html")

@app.route('/EditMedia_files/bootstrap.min.js')
def editMediaBootstrap():
    return render_template("/EditMedia_files/bootstrap.min.js")

@app.route('/EditMedia_files/jquery.min.js')
def editMediaJQuery():
    return render_template("/EditMedia_files/jquery.min.js")

#Suggestions routing
@app.route('/Suggestions')
def suggestions():
    return render_template("Suggestions.html")

@app.route('/Suggestions_files/bootstrap.min.js')
def suggestionsBootstrap():
    return render_template("/Suggestions_files/bootstrap.min.js")

@app.route('/Suggestions_files/jquery.min.js')
def suggestionsJQuery():
    return render_template("/Suggestions_files/jquery.min.js")

#More Suggestions routing
@app.route('/MoreSuggestions')
def moreSuggestions():
    return render_template("MoreSuggestions.html")

@app.route('/MoreSuggestions_files/bootstrap.min.js')
def moreSuggestionsBootstrap():
    return render_template("/MoreSuggestions_files/bootstrap.min.js")

@app.route('/MoreSuggestions_files/jquery.min.js')
def moreSuggestionsJQuery():
    return render_template("/MoreSuggestions_files/jquery.min.js")


#Bootstrap CSS routing
@app.route('/bootstrap/css/bootstrap.min.css')
def bootstrapCSS():
    return render_template("/bootstrap/css/bootstrap.min.css")



