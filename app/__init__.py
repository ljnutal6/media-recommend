from flask import Flask
from flask.ext.login import LoginManager

# generate with os.urandom(24) in a Python shell
SECRET_KEY = 'uE\xd3}\xf69\xb9\xd3\xe2\xd4\xc0m\\\x11\x01\x99\x9a#^s\r&&\xc2'

app = Flask(__name__)
app.secret_key = SECRET_KEY

lm = LoginManager()
lm.init_app(app)

from app import views
