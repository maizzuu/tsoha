from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLAlCHEMY_DATABASE_URI"] = "postgres://maijapajumaa1"
db = SQLAlchemy(app)

@app.route("/")
def index():
	result = db.session.execute("SELECT date, comment FROM give")
	offers = result.fetchall()
	return render_template("index.html", offers=offers)

@app.route("/new")
def new():
	return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
	date = request.form["date"]
	comment = request.form["comment"]
	sql = "INSERT INTO give (date, comment) VALUES (:date, :comment)"
	db.session.execute(sql, {"date":date, "comment":comment})
	db.session.commit()
	return redirect("/")

