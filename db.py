from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


# MUISTA MUUTTAA SECRET KEY JA DB_URL ENNEN HEROKUUN PUSHAAMISTA!!!!!!

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")
