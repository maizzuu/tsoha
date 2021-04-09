from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://maijapajumaa1@localhost"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = "a0b66cfd66233307e11b6c30633acc5c"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]
	sql = "SELECT password FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if user == None:
		return "Väärä käyttäjänimi"
	else:
		hash_value = user[0]
		if check_password_hash(hash_value,password):
			session["username"] = username
			return redirect("/")
		else:
			return "Väärä salasana"

@app.route("/new_login", methods=["POST"])
def new_login():
	username = request.form["username"]
	password = request.form["password"]
	hash_value = generate_password_hash(password)
	sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
	db.session.execute(sql, {"username":username, "password":hash_value})
	db.session.commit()
	session["username"] = username
	return redirect("/")

@app.route("/logout")
def logout():
	del session["username"]
	return redirect("/")

@app.route("/create")
def create():
	return render_template("create.html")

# otetaan vastaan

@app.route("/give")
def give():
	db.create_all()
	result = db.session.execute("SELECT date, comment FROM give")
	offers = result.fetchall()
	return render_template("give.html", offers=offers)

@app.route("/new_give")
def new_give():
	return render_template("new_give.html")

@app.route("/send_give", methods=["POST"])
def send_give():
	date = request.form["date"]
	comment = request.form["comment"]
	sql = "INSERT INTO give (date, comment) VALUES (:date, :comment)"
	db.session.execute(sql, {"date":date, "comment":comment})
	db.session.commit()
	return redirect("/give")


# annetaan pois

@app.route("/take")
def take():
	db.create_all()
	result = db.session.execute("SELECT date, start_time, end_time, post, comment FROM take")
	offers = result.fetchall()
	return render_template("take.html", offers=offers)

@app.route("/new_take")
def new_take():
	return render_template("new_take.html")

@app.route("/send_take", methods=["POST"])
def send_take():
	date = request.form["date"]
	start_time = request.form["start_time"]
	end_time = request.form["end_time"]
	post = request.form["post"]
	comment = request.form["comment"]
	sql = "INSERT INTO take (date, start_time, end_time, post, comment) VALUES (:date, :start_time, :end_time, :post, :comment);"
	db.session.execute(sql, {"date":date, "start_time":start_time, "end_time":end_time, "post":post, "comment":comment})
	db.session.commit()
	return redirect("/take")


# vaihdetaan

@app.route("/swap")
def swap():
	db.create_all()
	result = db.session.execute("SELECT date, start_time, end_time, post, comment FROM swap")
	offers = result.fetchall()
	return render_template("swap.html", offers=offers)

@app.route("/new_swap")
def new_swap():
	return render_template("new_swap.html")

@app.route("/send_swap")
def send_swap():
	date = request.form["date"]
	start_time = request.form["start_time"]
	end_time = request.form["end_time"]
	post = request.form["post"]
	comment = request.form["comment"]
	sql = "INSERT INTO swap (date, start_time, end_time, post, comment) VALUES (:date, :start_time, :end_time, :post, :comment);"
	db.session.execute(sql, {"date":date, "start_time":start_time, "end_time":end_time, "post":post, "comment":comment})
	db.session.commit()
	return redirect("/swap")
