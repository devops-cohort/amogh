import os
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://"+os.getenv("MYSQL_USER")+":"+os.getenv("MYSQL_PASSWORD")+"@"+os.getenv("MYSQL_IP")+"/"+os.getenv("MYSQL_DB")
app.config["SECRET_KEY"] = os.getenv("MYSQL_KEY")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from application import routes
