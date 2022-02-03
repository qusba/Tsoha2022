from app import app
from flask import render_template, request, redirect
import users,restaurants,reviews,restaurantInfo

@app.route("/")
def index():
	list = restaurants.get_restaurants()
	return render_template("index.html",reviewed_restaurants=list)

@app.route("/restaurant/<string:name>",methods=["GET","POST"])
def restaurant(name):
	if request.method == "GET":
		r_name = restaurants.get_restaurant_name(name)
		r_reviews = restaurants.get_visible_reviews(name)
		v_info = restaurants.get_visible_info(name)
		return render_template("restaurant.html",restaurant_name=r_name,reviews=r_reviews,v_info=v_info)
	if request.method == "POST":
		stars = request.form["stars"]
		review = request.form["review"]
		id = users.user_id()
		r_name = restaurants.get_restaurant_name(name)
		if 1<= len(review) <=200:
			reviews.review(stars,review,id,r_name[0])
			return redirect(f"/restaurant/{r_name[0]}")
		else:
			return render_template("error.html", error = "Sanallisen arvion tulee olla 1-200 merkkiä!")

@app.route("/info/<string:name>",methods = ["GET","POST"])
def info(name):
	if users.is_admin():
		if request.method == "GET":
			r_name = restaurants.get_restaurant_name(name)
			v_info = restaurants.get_visible_info(name)
			return render_template("info.html",restaurant_name=r_name,v_info=v_info)
		if request.method == "POST":
			r_name = restaurants.get_restaurant_name(name)
			title = request.form["title"]
			info = request.form["info"]
			r_id = restaurants.get_id(name)
			restaurantInfo.add_info(r_id,title,info)
			return redirect(f"/info/{r_name[0]}")
	else:
                return render_template("error.html", error = "Sinulla ei ole oikeuksia nähdä tätä sivua.")

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
