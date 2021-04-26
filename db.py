from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


# MUISTA MUUTTAA SECRET KEY JA DB_URL ENNEN HEROKUUN PUSHAAMISTA!!!!!!

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL", "postgresql://maijapajumaa1@localhost")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY", "a0b66cfd66233307e11b6c30633acc5c")
