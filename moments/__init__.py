from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_moment import Moment

moments = Flask(__name__)
moments.config.from_object('config')
db = SQLAlchemy(moments)
bcrypt = Bcrypt(moments)

login_manager = LoginManager()
login_manager.init_app(moments)
login_manager.login_view = "signin"

moment = Moment(moments)

from moments import views, models