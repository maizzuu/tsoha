from app import app
from flask import abort, render_template, redirect, request, session
from adequacy import check_date, check_time
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

@app.route("/")
def index():
	db.create_all()
	return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]
	sql = "SELECT password FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if user == None:
		return render_template("wrong_username.html")
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
			return render_template("wrong_password.html")

@app.route("/new_login", methods=["POST"])
def new_login():
	username = request.form["username"]
	password = request.form["password"]
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
	if not session["user_type"] == "user":
		abort(403)
	username = session["username"]
	sql = "SELECT g.id, g.date, g.comment, go.date, go.offer, go.username FROM give g, give_offers go WHERE g.id=go.give_id AND g.username = :username AND go.user_visibility=1 AND go.date >= :today ORDER BY g.date"
	result = db.session.execute(sql, {"username":username, "today":today})
	give_offers = result.fetchall()
	sql = "SELECT t.id, t.date, t.start_time, t.end_time, t.post, t.comment, tko.username FROM take t, take_offers tko WHERE t.id=tko.take_id AND t.username = :username AND tko.user_visibility=1 AND t.date >= :today ORDER BY t.date"
	result = db.session.execute(sql, {"username":username, "today":today})
	take_offers = result.fetchall()
	sql = "SELECT s.id, s.date, s.start_time, s.end_time, s.post, s.comment, so.date, so.offer, so.username FROM swap s, swap_offers so WHERE s.id=so.swap_id AND s.username = :username AND so.user_visibility=1 AND so.date >= :today ORDER BY s.date"
	result = db.session.execute(sql, {"username":username, "today":today})
	swap_offers = result.fetchall()
	return render_template("offers.html", give_offers=give_offers, take_offers=take_offers, swap_offers=swap_offers)

# esimies

@app.route("/waiting")
def waiting():
	db.create_all()
	if not session["user_type"] == "admin":
		abort(403)
	#give
	result = db.session.execute("SELECT g.date, go.offer, g.username, go.username, g.id FROM give_offers go, give g WHERE go.give_id = g.id AND go.admin_visibility = 1 ORDER BY g.date")
	offers_give = result.fetchall()
	#take
	result = db.session.execute("SELECT t.date, t.start_time, t.end_time, t.post, t.username, tko.username, t.id FROM take t, take_offers tko WHERE t.id=tko.take_id AND tko.admin_visibility = 1 ORDER BY t.date")
	offers_take = result.fetchall()
	#swap
	result = db.session.execute("SELECT s.date, s.start_time, s.end_time, s.post, s.username, so.date, so.offer, so.username, s.id FROM swap s, swap_offers so WHERE s.id=so.swap_id AND so.admin_visibility = 1 ORDER BY s.date")
	offers_swap = result.fetchall()
	return render_template("waiting.html", offers_give=offers_give, offers_take=offers_take, offers_swap=offers_swap)

@app.route("/confirm", methods=["POST"])
def confirm():
	if not session["user_type"] == "admin":
		abort(403)
	form = request.form["id"]
	form = form.split(",")
	id_value = form[0]
	action = form[1]
	name = form[2]
	table = request.form["table"]
	if table == "give":
		if action == "confirm":
			sql = "DELETE FROM give_offers WHERE give_id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
			sql = "DELETE FROM give WHERE id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
		if action == "decline":
			sql = "UPDATE give SET visibility = 1 WHERE id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
			sql = "DELETE FROM give_offers WHERE give_id = :id AND username = :name"
			db.session.execute(sql, {"id":id_value, "name":name})
			db.session.commit()
			sql = "UPDATE give_offers SET user_visibility = 1 WHERE give_id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
	elif table == "take":
		if action == "confirm":
			sql = "DELETE FROM take_offers WHERE take_id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
			sql = "DELETE FROM take WHERE id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
		if action == "decline":
			sql = "UPDATE take SET visibility = 1 WHERE id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
			sql = "DELETE FROM take_offers WHERE take_id = :id AND username = :name"
			db.session.execute(sql, {"id":id_value, "name":name})
			db.session.commit()
			sql = "UPDATE take_offers SET user_visibility = 1 WHERE take_id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
	elif table == "swap":
		if action == "confirm":
			sql = "DELETE FROM swap_offers WHERE swap_id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
			sql = "DELETE FROM swap WHERE id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
		if action == "decline":
			sql = "UPDATE swap SET visibility = 1 WHERE id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
			sql = "DELETE FROM swap_offers WHERE swap_id = :id AND username = :name"
			db.session.execute(sql, {"id":id_value, "name":name})
			db.session.commit()
			sql = "UPDATE swap_offers SET user_visibility = 1 WHERE swap_id = :id"
			db.session.execute(sql, {"id":id_value})
			db.session.commit()
	return redirect("/waiting")

# otetaan vastaan

@app.route("/give")
def give():
	if not session["user_type"] == "user":
		abort(403)
	db.create_all()
	result = db.session.execute("SELECT id, date, comment, username FROM give WHERE visibility = 1 and date >= :today ORDER BY date", {"today":today})
	offers = result.fetchall()
	result = db.session.execute("SELECT id FROM give WHERE visibility = 1 and date >= :today ORDER BY date", {"today":today})
	id_list = result.fetchall()
	user = session["username"]
	result = db.session.execute("SELECT id FROM give WHERE username = :username and date >= :today and visibility=1 ORDER BY id", {"username":user, "today":today})
	drop_list = result.fetchall()
	return render_template("give.html", offers=offers, id_list=id_list, today=today, your_offers=drop_list)

@app.route("/new_give")
def new_give():
	if not session["user_type"] == "user":
		abort(403)
	return render_template("new_give.html", today=today)

@app.route("/send_give", methods=["POST"])
def send_give():
	if not session["user_type"] == "user":
		abort(403)
	date = request.form["date"]
	if not check_date(date):
		return render_template("incorrect_date.html")
	comment = request.form["comment"]
	sql = "INSERT INTO give (date, comment, username, visibility) VALUES (:date, :comment, :username, 1)"
	db.session.execute(sql, {"date":date, "comment":comment, "username":session["username"]})
	db.session.commit()
	return redirect("/give")

@app.route("/offer_give", methods=["POST"])
def offer_give():
	if not session["user_type"] == "user":
		abort(403)
	give_id = request.form["id"]
	pvm = request.form["pvm"]
	offer = request.form["offer"]
	sql = 'INSERT INTO give_offers (give_id, offer, username, date, admin_visibility, user_visibility) VALUES (:id, :offer, :username, :pvm, 0, 1)'
	db.session.execute(sql, {"id":give_id, "offer":offer, "username":session["username"], "pvm":pvm})
	db.session.commit()
	return redirect("/give")

@app.route("/accept_give", methods=["POST"])
def accept_give():
	if not session["user_type"] == "user":
		abort(403)
	ok = request.form["ok"]
	ok = ok.split(",")
	give_id = ok[0]
	name = ok[1]
	status = ok[2]
	offer = ok[3]
	if status == "confirm":
		sql = "UPDATE give_offers SET user_visibility = 0, admin_visibility = 1 WHERE give_id = :id AND username = :name AND offer = :offer"
		db.session.execute(sql, {"id":give_id, "name":name, "offer":offer})
		db.session.commit()
		sql = "UPDATE give_offers SET user_visibility = 0 WHERE give_id = :id"
		db.session.execute(sql, {"id":give_id})
		db.session.commit()
		sql = "UPDATE give SET visibility = 0 WHERE id = :give_id"
		db.session.execute(sql, {"give_id":give_id})
		db.session.commit()
	else:
		sql = "UPDATE give_offers SET user_visibility = 0 WHERE give_id = :id AND username = :username AND offer = :offer"
		db.session.execute(sql, {"id":give_id, "username":name, "offer":offer})
		db.session.commit()
	return redirect("/offers")

@app.route("/delete_give", methods=["POST"])
def delete_give():
	if not session["user_type"] == "user":
		abort(403)
	drop_ids = request.form.getlist("drop")
	for drop_id in drop_ids:
		sql = "UPDATE give SET visibility = 0 WHERE id = :id"
		db.session.execute(sql, {"id":int(drop_id)})
		db.session.commit()
	return redirect("/give")

# annetaan pois

@app.route("/take")
def take():
	if not session["user_type"] == "user":
		abort(403)
	db.create_all()
	result = db.session.execute("SELECT id, date, start_time, end_time, post, comment, username FROM take WHERE visibility = 1 and date >= :today ORDER BY date", {"today":today})
	offers = result.fetchall()
	result = db.session.execute("SELECT id FROM take WHERE visibility = 1 and date >= :today ORDER BY date", {"today":today})
	id_list = result.fetchall()
	user = session["username"]
	result = db.session.execute("SELECT id FROM take WHERE username = :username and date >= :today and visibility=1 ORDER BY id", {"username":user, "today":today})
	drop_list = result.fetchall()
	return render_template("take.html", offers=offers, id_list=id_list, your_offers=drop_list)

@app.route("/new_take")
def new_take():
	if not session["user_type"] == "user":
		abort(403)
	return render_template("new_take.html", today=today)

@app.route("/send_take", methods=["POST"])
def send_take():
	if not session["user_type"] == "user":
		abort(403)
	date = request.form["date"]
	start_time = request.form["start_time"]
	end_time = request.form["end_time"]
	if not check_time(start_time):
		return render_template("incorrect_start_time.html")
	if not check_time(end_time):
		return render_template("incorrect_end_time.html")
	post = request.form["post"]
	comment = request.form["comment"]
	sql = "INSERT INTO take (date, start_time, end_time, post, comment, username, visibility) VALUES (:date, :start_time, :end_time, :post, :comment, :username, 1);"
	db.session.execute(sql, {"date":date, "start_time":start_time, "end_time":end_time, "post":post, "comment":comment, "username":session["username"]})
	db.session.commit()
	return redirect("/take")

@app.route("/offer_take", methods=["POST"])
def offer_take():
	if not session["user_type"] == "user":
		abort(403)
	take_id = request.form["id"]
	sql = 'INSERT INTO take_offers (take_id, username, admin_visibility, user_visibility) VALUES (:id, :username, 0, 1)'
	db.session.execute(sql, {"id":take_id, "username":session["username"]})
	db.session.commit()
	return redirect("/take")

@app.route("/accept_take", methods=["POST"])
def accept_take():
	if not session["user_type"] == "user":
		abort(403)
	ok = request.form["ok"]
	ok = ok.split(",")
	take_id = ok[0]
	name = ok[1]
	status = ok[2]
	if status == "confirm":
		sql = "UPDATE take_offers SET user_visibility = 0, admin_visibility = 1 WHERE take_id = :id AND username = :name"
		db.session.execute(sql, {"id":take_id, "name":name})
		db.session.commit()
		sql = "UPDATE take_offers SET user_visibility = 0 WHERE take_id = :id"
		db.session.execute(sql, {"id":take_id})
		db.session.commit()
		sql = "UPDATE take SET visibility = 0 WHERE id = :take_id"
		db.session.execute(sql, {"take_id":take_id})
		db.session.commit()
	else:
		sql = "UPDATE take_offers SET user_visibility = 0 WHERE take_id = :id AND username = :username"
		db.session.execute(sql, {"id":take_id, "username":name})
		db.session.commit()
	return redirect("/offers")

@app.route("/delete_take", methods=["POST"])
def delete_take():
	if not session["user_type"] == "user":
		abort(403)
	drop_ids = request.form.getlist("drop")
	for drop_id in drop_ids:
		sql = "UPDATE take SET visibility = 0 WHERE id = :id"
		db.session.execute(sql, {"id":int(drop_id)})
		db.session.commit()
	return redirect("/take")

# vaihdetaan

@app.route("/swap")
def swap():
	if not session["user_type"] == "user":
		abort(403)
	db.create_all()
	result = db.session.execute("SELECT id, date, start_time, end_time, post, comment, username FROM swap WHERE visibility = 1 and date >= :today ORDER BY date", {"today":today})
	offers = result.fetchall()
	result = db.session.execute("SELECT id FROM swap WHERE visibility = 1 and date >= :today ORDER BY date", {"today":today})
	id_list = result.fetchall()
	user = session["username"]
	result = db.session.execute("SELECT id FROM swap WHERE username = :username and date >= :today and visibility=1 ORDER BY id", {"username":user, "today":today})
	drop_list = result.fetchall()
	return render_template("swap.html", offers=offers, id_list=id_list, today=today, your_offers=drop_list)

@app.route("/new_swap")
def new_swap():
	if not session["user_type"] == "user":
		abort(403)
	return render_template("new_swap.html", today=today)

@app.route("/send_swap", methods=["POST"])
def send_swap():
	if not session["user_type"] == "user":
		abort(403)
	date = request.form["date"]
	if not check_date(date):
		return render_template("incorrect_date.html")
	start_time = request.form["start_time"]
	end_time = request.form["end_time"]
	if not check_time(start_time):
		return render_template("incorrect_start_time_swap.html")
	if not check_time(end_time):
		return render_template("incorrect_end_time_swap.html")
	post = request.form["post"]
	comment = request.form["comment"]
	sql = "INSERT INTO swap (date, start_time, end_time, post, comment, username, visibility) VALUES (:date, :start_time, :end_time, :post, :comment, :username, 1);"
	db.session.execute(sql, {"date":date, "start_time":start_time, "end_time":end_time, "post":post, "comment":comment, "username":session["username"]})
	db.session.commit()
	return redirect("/swap")

@app.route("/offer_swap", methods=["POST"])
def offer_swap():
	if not session["user_type"] == "user":
		abort(403)
	swap_id = request.form["id"]
	pvm = request.form["pvm"]
	offer = request.form["offer"]
	sql = 'INSERT INTO swap_offers (swap_id, username, offer, date, admin_visibility, user_visibility) VALUES (:id, :username, :offer, :pvm, 0, 1)'
	db.session.execute(sql, {"id":swap_id, "username":session["username"], "offer":offer, "pvm":pvm})
	db.session.commit()
	return redirect("/swap")

@app.route("/accept_swap", methods=["POST"])
def accept_swap():
	if not session["user_type"] == "user":
		abort(403)
	ok = request.form["ok"]
	ok = ok.split(",")
	swap_id = ok[0]
	name = ok[1]
	status = ok[2]
	offer = ok[3]
	if status == "confirm":
		sql = "UPDATE swap_offers SET user_visibility = 0, admin_visibility = 1 WHERE swap_id = :id AND username = :name"
		db.session.execute(sql, {"id":swap_id, "name":name})
		db.session.commit()
		sql = "UPDATE swap_offers SET user_visibility = 0 WHERE swap_id = :id"
		db.session.execute(sql, {"id":swap_id})
		db.session.commit()
		sql = "UPDATE swap SET visibility = 0 WHERE id = :swap_id"
		db.session.execute(sql, {"swap_id":swap_id})
		db.session.commit()
	else:
		sql = "UPDATE swap_offers SET user_visibility = 0 WHERE swap_id = :id AND username = :name AND offer = :offer"
		db.session.execute(sql, {"id":swap_id, "name":name, "offer":offer})
		db.session.commit()
	return redirect("/offers")

@app.route("/delete_swap", methods=["POST"])
def delete_swap():
	if not session["user_type"] == "user":
		abort(403)
	drop_ids = request.form.getlist("drop")
	for drop_id in drop_ids:
		sql = "UPDATE swap SET visibility = 0 WHERE id = :id"
		db.session.execute(sql, {"id":int(drop_id)})
		db.session.commit()
	return redirect("/swap")
