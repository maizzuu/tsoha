from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/page/<int:id>")
def page(id):
	return "You are on page "+str(id)

@app.route("/send", methods=["POST"])
def send():
	d = request.form["drink"]
	s = request.form.getlist("snack")
	return render_template("send.html", drink=d, snack=s)
