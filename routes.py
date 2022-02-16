from app import app
from flask import render_template, request, redirect
import users,restaurants,reviews,restaurantInfo

@app.route("/")
def index():
	list_of_reviewed_restaurants = restaurants.get_reviewed_restaurants()
	list_of_all_visible_restaurants = restaurants.get_all_visible_restaurants()
	return render_template("index.html",reviewed_restaurants=list_of_reviewed_restaurants,all_restaurants=list_of_all_visible_restaurants)

@app.route("/result",methods=["GET"])
def result():
	query = request.args["query"]
	results = restaurantInfo.info_query(query)
	return render_template("result.html",results=results)

@app.route("/new-restaurant",methods=["GET","POST"])
def new_restaurant():
	if users.is_admin():
		if request.method == "GET":
			return render_template("new-restaurant.html")
		if request.method == "POST":
			name = request.form["name"]
			if restaurants.add_restaurant(name):
				return redirect("/")
			else:
				return render_template("error.html",error="jokin meni vikaan")

@app.route("/delete-restaurants",methods=["GET","POST"])
def delete_restaurants():
	if users.is_admin():
		if request.method == "GET":
			list_of_all_restaurants = restaurants.get_all_restaurants()
			return render_template("delete-restaurants.html", restaurants = list_of_all_restaurants)
		if request.method == "POST":
			id = int(request.form["id"])
			visible = request.form["action"]
			if restaurants.hide_restaurant(id,visible):
				return redirect("/delete-restaurants")
			else:
				return render_template("error.html", error = "Virheellinen id numero")
	else:
		return render_template("error.html", error = "Sinulla ei ole oikeuksia nähdä tätä sivua")

@app.route("/restaurant/<string:name>",methods=["GET","POST"])
def restaurant(name):
	if request.method == "GET":
		r_reviews = reviews.get_visible_reviews(name)
		v_info = restaurantInfo.get_visible_info(name)
		return render_template("restaurant.html",restaurant_name=name,reviews=r_reviews,v_info=v_info)

	if request.method == "POST":
		stars = request.form["stars"]
		review = request.form["review"]
		id = users.user_id()
		if 1<= len(review) <=200:
			reviews.review(stars,review,id,name)
			return redirect(f"/restaurant/{name}")
		else:
			return render_template("error.html", error = "Sanallisen arvion tulee olla 1-200 merkkiä!")

@app.route("/modify-reviews/<string:name>", methods = ["GET","POST"])
def modify_reviews(name):
	if users.is_admin():
		if request.method == "GET":
			all_reviews = reviews.get_all_reviews(name)
			return render_template("modify-reviews.html",reviews = all_reviews, name = name)
		if request.method == "POST":
			if request.form["id"] != "":
				id = int(request.form["id"])
				visible = request.form["action"]
				if reviews.modify_review(id,visible):
					return redirect(f"/modify-reviews/{name}")
				else:
					return render_template("error.html",error="Virheellinen id numero")
			else:
				return render_template("error.html", error = "Syötä id numero.")
	else:
		return render_template("error.html", error = "Sinulla ei ole oikeuksia nähdä tätä sivua.")

@app.route("/info/<string:name>",methods = ["GET","POST"])
def info(name):
	if users.is_admin():
		if request.method == "GET":
			v_info = restaurantInfo.get_visible_info(name)
			return render_template("info.html",restaurant_name=name,v_info=v_info)
		if request.method == "POST":
			title = request.form["title"]
			info = request.form["info"]
			r_id = restaurants.get_id(name)
			restaurantInfo.add_info(r_id,title,info)
			return redirect(f"/info/{name}")
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
