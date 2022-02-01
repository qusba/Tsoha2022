from db import db

def get_restaurants():
	sql = "SELECT a.name,sum(r.stars)/count(r.stars) FROM restaurants a, reviews r WHERE a.id = r.restaurant_id GROUP BY a.name ORDER BY sum(r.stars)/count(r.stars) DESC"
	result = db.session.execute(sql)
	return result.fetchall()

def get_restaurant_name(name):
	sql = "SELECT name FROM restaurants WHERE name=:name"
	result = db.session.execute(sql,{"name":name})
	return result.fetchone()

def get_reviews(name):
	sql = "SELECT review,stars FROM reviews WHERE restaurant_id = (SELECT id FROM restaurants WHERE name=:name) AND visible=TRUE"
	result = db.session.execute(sql, {"name":name})
	return result.fetchall()
