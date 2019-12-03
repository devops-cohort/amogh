import os
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://"+os.getenv("MYSQL_USER")+":"+os.getenv("MYSQL_PASSWORD")+"@"+os.getenv("MYSQL_URL")+"/"+os.getenv("MYSQL_DB")
app.config["SECRET_KEY"] = os.getenv("MYSQL_KEY")
db = SQLAlchemy(app)


from application import routes
