from app import app
from flask import render_template, request, redirect
import users,restaurants

@app.route("/")
def index():
	list = restaurants.get_restaurants()
	return render_template("index.html",reviewed_restaurants=list)

@app.route("/restaurant/<string:name>")
def restaurant(name):
	r_name = restaurants.get_restaurant_name(name)
	reviews = restaurants.get_reviews(name)
	return render_template("restaurant.html",restaurant_name=r_name,reviews=reviews)

@app.route("/login", methods=["GET","POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(username,password):
			return redirect("/")
		else:
			return render_template("error.html", error = "Virheellinen tunnus tai salasana")

@app.route("/register", methods=["GET","POST"])
def register():
	if request.method =="GET":
		return render_template("register.html")
	if request.method =="POST":
		username = request.form["username"]
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		if password1 != password2:
			return render_template("error.html",error ="Salasanat eivät ole samat!")
		if users.register(username,password1):
			return redirect("/")
		else:
			return render_template("error.html",error="Käyttäjänimi on jo käytössä, ole hyvä ja valitse toinen käyttäjänimi")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")
