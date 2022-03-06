from app import app
from flask import render_template, request, redirect
import users,restaurants,reviews,restaurantInfo, groups

@app.route("/")
def index():
	list_of_reviewed_restaurants = restaurants.get_reviewed_restaurants()
	list_of_all_visible_restaurants = restaurants.get_all_visible_restaurants()
	list_of_visible_groups = groups.get_visible_groups()
	return render_template("index.html",reviewed_restaurants=list_of_reviewed_restaurants,all_restaurants=list_of_all_visible_restaurants,groups=list_of_visible_groups)

@app.route("/group/<string:name>", methods =["GET"])
def group(name):
	results = restaurantInfo.info_query(name)
	return render_template("group.html",results=results, restaurant_name=name)

@app.route("/new-group",methods=["GET","POST"])
def new_group():
	if users.is_admin():
		if request.method == "GET":
			return render_template("new-group.html")
		if request.method == "POST":
			if users.get_token() != request.form["csrf_token"]:
				abort(403)
			name = request.form["name"]
			if len(name) == 0:
				return render_template("error.html", error = "Nimessä tulee olla vähintään 1 merkki!")
			if groups.add_group(name):
				return redirect("/")
			else:
				return render_template("error.html",error="Jokin meni vikaan, ryhmä saattaa olla jo olemassa.")
	else:
		return render_template("error.html",error="Sinulla ei ole oikeutta nähdä tätä sivua.")

@app.route("/delete-groups",methods=["GET","POST"])
def delete_groups():
	if users.is_admin():
		if request.method == "GET":
			list_of_groups = groups.get_groups()
			return render_template("delete-groups.html",groups=list_of_groups)
		if request.method == "POST":
			if users.get_token() != request.form["csrf_token"]:
				abort(403)
			if request.form["id"] != "":
				id = int(request.form["id"])
				visible = request.form["action"]
				if visible == "bad":
					return render_template("error.html",error="Sinun täytyy valita piilota tai muuta näkyväksi")
				if groups.delete_group(id,visible):
					return redirect("/")
				else:
					return render_template("error.html",error="Virheellinen id numero")
			else:
                                return render_template("error.html",error="Syötä id numero")
	else:
		return render_template("error.html",error="Sinulla ei ole oikeutta nähdä tätä sivua.")

@app.route("/result",methods=["GET"])
def result():
	query = request.args["query"]
	if len(query) == 0:
		return render_template("error.html",error="Syötä vähintään 1 merkki")
	results = restaurantInfo.info_query(query)
	return render_template("result.html",results=results)

@app.route("/new-restaurant",methods=["GET","POST"])
def new_restaurant():
	if users.is_admin():
		if request.method == "GET":
			return render_template("new-restaurant.html")
		if request.method == "POST":
			if users.get_token() != request.form["csrf_token"]:
                                abort(403)

			name = request.form["name"]
			if len(name) == 0:
				return render_template("error.html", error="Nimessä tulee olla vähintään 1 merkki!")
			if restaurants.add_restaurant(name):
				return redirect("/")
			else:
				return render_template("error.html",error="jokin meni vikaan")
	else:
		return render_template("error.html", error = "Sinulla ei ole oikeutta nähdä tätä sivua.")

@app.route("/delete-restaurants",methods=["GET","POST"])
def delete_restaurants():
	if users.is_admin():
		if request.method == "GET":
			list_of_all_restaurants = restaurants.get_all_restaurants()
			return render_template("delete-restaurants.html", restaurants = list_of_all_restaurants)
		if request.method == "POST":
			if users.get_token() != request.form["csrf_token"]:
                                abort(403)
			if request.form["id"] != "":
				id = int(request.form["id"])
				visible = request.form["action"]
				if visible == "bad":
					return render_template("error.html",error="Sinun täytyy valita piilota tai muuta näkyväksi")
				if restaurants.hide_restaurant(id,visible):
					return redirect("/delete-restaurants")
				else:
					return render_template("error.html", error = "Virheellinen id numero")
			else:
				return render_template("error.html",error="Syötä id numero")
	else:
		return render_template("error.html", error = "Sinulla ei ole oikeutta nähdä tätä sivua")

@app.route("/restaurant/<string:name>",methods=["GET","POST"])
def restaurant(name):
	if request.method == "GET":
		r_reviews = reviews.get_visible_reviews(name)
		v_info = restaurantInfo.get_visible_info(name)
		return render_template("restaurant.html",restaurant_name=name,reviews=r_reviews,v_info=v_info)

	if request.method == "POST":
		if request.form["form"] == "2":
			if users.get_token() != request.form["csrf_token"]:
				abort(403)

			try:
				stars = request.form["stars"]
			except:
				return render_template("error.html",error="Anna vähintään yksi tähti.")
			review = request.form["review"]
			id = users.user_id()
			if 1<= len(review) <=200:
				reviews.review(stars,review,id,name)
				return redirect(f"/restaurant/{name}")
			else:
				return render_template("error.html", error = "Sanallisen arvion tulee olla 1-200 merkkiä!")
		if request.form["form"] == "1":
			if users.is_admin():
				if users.get_token() != request.form["csrf_token"]:
					abort(403)
				title = request.form["title"]
				info = request.form["info"]
				r_id = restaurants.get_id(name)
				if len(title) != 0 and len(info) != 0:
					restaurantInfo.add_info(r_id,title,info)
					return redirect(f"/restaurant/{name}")
				else:
					return render_template("error.html", error = "Informaation tyyppi tai sisältö eivät voi olla tyhjiä!")

@app.route("/modify-reviews/<string:name>", methods = ["GET","POST"])
def modify_reviews(name):
	if users.is_admin():
		if request.method == "GET":
			all_reviews = reviews.get_all_reviews(name)
			return render_template("modify-reviews.html",reviews = all_reviews, name = name)
		if request.method == "POST":
			if users.get_token() != request.form["csrf_token"]:
                                abort(403)

			if request.form["id"] != "":
				id = int(request.form["id"])
				visible = request.form["action"]
				if visible == "bad":
					return render_template("error.html",error="Sinun täytyy valita piilota tai muuta näkyväksi")
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
			all_info = restaurantInfo.get_all_info(name)
			return render_template("info.html",restaurant_name=name,all_info=all_info)
		if request.method == "POST":
			if users.get_token() != request.form["csrf_token"]:
                                abort(403)

			if request.form["id"] != "":
				id = int(request.form["id"])
				visible = request.form["action"]
				if visible == "bad":
					return render_template("error.html",error = "Sinun täytyy valita piilota tai muuta näkyväksi")
				if restaurantInfo.hide_info(id,visible):
					return redirect(f"/info/{name}")
				else:
					return render_template("error.html",error = "Virheellinen id numero")
			else:
				return render_template("error.html", error ="Syötä id numero")
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
		if len(password1) < 4:
			return render_template("error.html",error ="Salasanan tulee olla vähintään 4 merkkiä.")
		if users.register(username,password1):
			return redirect("/")
		else:
			return render_template("error.html",error="Käyttäjänimi on jo käytössä, ole hyvä ja valitse toinen käyttäjänimi")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")
