from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager



app = Flask(__name__)
app. config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

import os.path
def mkpath (p):
    return os.path. normpath(
            os.path.join(
            os.path.dirname( __file__ ), p))
    
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../tuto.db'))
app.config['SECRET_KEY'] = "3d22093e-231a-4f4a-ad9b-4d8fdf8500d7"
db = SQLAlchemy(app)

