from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from adequacy import check_date, check_password, check_time, check_username
from datetime import date


# MUISTA MUUTTAA SECRET KEY JA DB_URL ENNEN HEROKUUN PUSHAAMISTA!!!!!!
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
			sql = "SELECT type FROM users WHERE username=:username"
			result = db.session.execute(sql, {"username":username})
			user_type = result.fetchone()[0]
			session["user_type"] = user_type
			return redirect("/")
		else:
			return "Väärä salasana"

@app.route("/new_login", methods=["POST"])
def new_login():
	username = request.form["username"]
	if len(username) == 0:
		return render_template("empty_username.html")
	if not check_username(username):
		return render_template("wrong_username.html")
	password = request.form["password"]
	if len(password) == 0:
		return render_template("empty_password.html")
	if not check_password(password):
		return render_template("wrong_password.html")
	user_type = request.form["user_type"]
	sql = "SELECT username FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	users = result.fetchall()
	if len(users) > 0:
		return render_template("username_taken.html")
	hash_value = generate_password_hash(password)
	sql = "INSERT INTO users (username, password, type) VALUES (:username, :password, :type)"
	db.session.execute(sql, {"username":username, "password":hash_value, "type":user_type})
	db.session.commit()
	session["username"] = username
	session["user_type"] = user_type
	return redirect("/")

@app.route("/logout")
def logout():
	del session["username"]
	del session["user_type"]
	return redirect("/")

@app.route("/create")
def create():
	return render_template("create.html")

@app.route("/offers")
def offers():
	username = session["username"]
	sql = "SELECT g.id, g.date, g.comment, go.date, go.offer, go.username FROM give g, give_offers go WHERE g.id=go.give_id AND g.username = :username AND go.user_visibility=1"
	result = db.session.execute(sql, {"username":username})
	give_offers = result.fetchall()
	sql = "SELECT t.id, t.date, t.start_time, t.end_time, t.post, t.comment, tko.username FROM take t, take_offers tko WHERE t.id=tko.take_id AND t.username = :username AND tko.user_visibility=1"
	result = db.session.execute(sql, {"username":username})
	take_offers = result.fetchall()
	sql = "SELECT s.id, s.date, s.start_time, s.end_time, s.post, s.comment, so.date, so.offer, so.username FROM swap s, swap_offers so WHERE s.id=so.swap_id AND s.username = :username AND so.user_visibility=1"
	result = db.session.execute(sql, {"username":username})
	swap_offers = result.fetchall()
	return render_template("offers.html", give_offers=give_offers, take_offers=take_offers, swap_offers=swap_offers)

# esimies

@app.route("/waiting")
def waiting():
	db.create_all()
	#give
	result = db.session.execute("SELECT g.date, go.offer, g.username, go.username FROM give_offers go, give g WHERE go.give_id = g.id AND go.admin_visibility = 1 ORDER BY g.date")
	offers_give = result.fetchall()
	#take
	result = db.session.execute("SELECT t.date, t.start_time, t.end_time, t.post, t.username, tko.username FROM take t, take_offers tko WHERE t.id=tko.take_id AND tko.admin_visibility = 1 ORDER BY t.date")
	offers_take = result.fetchall()
	#swap
	result = db.session.execute("SELECT s.date, s.start_time, s.end_time, s.post, s.username, so.date, so.offer, so.username  FROM swap s, swap_offers so WHERE s.id=so.swap_id AND so.admin_visibility = 1 ORDER BY s.date")
	offers_swap = result.fetchall()
	return render_template("waiting.html", offers_give=offers_give, offers_take=offers_take, offers_swap=offers_swap)

# otetaan vastaan

@app.route("/give")
def give():
	db.create_all()
	result = db.session.execute("SELECT id, date, comment, username FROM give ORDER BY date")
	offers = result.fetchall()
	result = db.session.execute("SELECT id FROM give ORDER BY id")
	id_list = result.fetchall()
	today = date.today()
	return render_template("give.html", offers=offers, id_list=id_list, today=today)

@app.route("/new_give")
def new_give():
	return render_template("new_give.html", today=date.today())

@app.route("/send_give", methods=["POST"])
def send_give():
	date = request.form["date"]
	comment = request.form["comment"]
	if len(date) == 0:
		return render_template("empty_give.html")
	sql = "INSERT INTO give (date, comment, username) VALUES (:date, :comment, :username)"
	db.session.execute(sql, {"date":date, "comment":comment, "username":session["username"]})
	db.session.commit()
	return redirect("/give")

@app.route("/offer_give", methods=["POST"])
def offer_give():
	id = request.form["id"]
	pvm = request.form["pvm"]
	offer = request.form["offer"]
	sql = 'INSERT INTO give_offers (give_id, offer, username, date, admin_visibility, user_visibility) VALUES (:id, :offer, :username, :pvm, 0, 1)'
	db.session.execute(sql, {"id":id, "offer":offer, "username":session["username"], "pvm":pvm})
	db.session.commit()
	return redirect("/give")

# annetaan pois

@app.route("/take")
def take():
	db.create_all()
	result = db.session.execute("SELECT id, date, start_time, end_time, post, comment, username FROM take ORDER BY id")
	offers = result.fetchall()
	result = db.session.execute("SELECT id FROM take ORDER BY id")
	id_list = result.fetchall()
	return render_template("take.html", offers=offers, id_list=id_list)

@app.route("/new_take")
def new_take():
	return render_template("new_take.html", today=date.today())

@app.route("/send_take", methods=["POST"])
def send_take():
	date = request.form["date"]
	start_time = request.form["start_time"]
	end_time = request.form["end_time"]
	if len(date) == 0 or len(start_time) == 0 or len(end_time) == 0:
		return render_template("empty_take.html")
	if not check_time(start_time):
		return render_template("incorrect_start_time_take.html")
	if not check_time(end_time):
		return render_template("incorrect_end_time_take.html")
	post = request.form["post"]
	comment = request.form["comment"]
	sql = "INSERT INTO take (date, start_time, end_time, post, comment, username) VALUES (:date, :start_time, :end_time, :post, :comment, :username);"
	db.session.execute(sql, {"date":date, "start_time":start_time, "end_time":end_time, "post":post, "comment":comment, "username":session["username"]})
	db.session.commit()
	return redirect("/take")

@app.route("/offer_take", methods=["POST"])
def offer_take():
	id = request.form["id"]
	sql = 'INSERT INTO take_offers (take_id, username, admin_visibility, user_visibility) VALUES (:id, :username, 0, 1)'
	db.session.execute(sql, {"id":id, "username":session["username"]})
	db.session.commit()
	return redirect("/take")


# vaihdetaan

@app.route("/swap")
def swap():
	db.create_all()
	result = db.session.execute("SELECT id, date, start_time, end_time, post, comment, username FROM swap ORDER BY id")
	offers = result.fetchall()
	result = db.session.execute("SELECT id FROM swap ORDER BY id")
	id_list = result.fetchall()
	today = date.today()
	return render_template("swap.html", offers=offers, id_list=id_list, today=today)

@app.route("/new_swap")
def new_swap():
	return render_template("new_swap.html", today=date.today())

@app.route("/send_swap", methods=["POST"])
def send_swap():
	date = request.form["date"]
	start_time = request.form["start_time"]
	end_time = request.form["end_time"]
	if len(date) == 0 or len(start_time) == 0 or len(end_time) == 0:
		return render_template("empty_swap.html")
	if not check_time(start_time):
		return render_template("incorrect_start_time_swap.html")
	if not check_time(end_time):
		return render_template("incorrect_end_time_swap.html")
	post = request.form["post"]
	comment = request.form["comment"]
	sql = "INSERT INTO swap (date, start_time, end_time, post, comment, username) VALUES (:date, :start_time, :end_time, :post, :comment, :username);"
	db.session.execute(sql, {"date":date, "start_time":start_time, "end_time":end_time, "post":post, "comment":comment, "username":session["username"]})
	db.session.commit()
	return redirect("/swap")

@app.route("/offer_swap", methods=["POST"])
def offer_swap():
	id = request.form["id"]
	pvm = request.form["pvm"]
	offer = request.form["offer"]
	sql = 'INSERT INTO swap_offers (swap_id, username, offer, date, admin_visibility, user_visibility) VALUES (:id, :username, :offer, :pvm, 0, 1)'
	db.session.execute(sql, {"id":id, "username":session["username"], "offer":offer, "pvm":pvm})
	db.session.commit()
	return redirect("/swap")