from db import db

def add_restaurant(name):
	sql = "INSERT INTO restaurants (name,visible) VALUES (:name,TRUE)"
	try:
		db.session.execute(sql,{"name":name})
		db.session.commit()
		return True
	except:
		return False

def hide_restaurant(id,visible):
	sql = "SELECT count(name) FROM restaurants WHERE id=:id"
	result = db.session.execute(sql,{"id":id})
	result = result.fetchone()
	if result != 0:
		sql = "UPDATE restaurants SET visible=:visible WHERE id=:id"
		db.session.execute(sql,{"id":id,"visible":visible})
		db.session.commit()
		return True
	else:
		return False

def get_reviewed_restaurants():
	sql = "SELECT a.name,sum(r.stars)/count(r.stars) FROM restaurants a, reviews r WHERE a.id = r.restaurant_id AND r.visible = TRUE GROUP BY a.name ORDER BY sum(r.stars)/count(r.stars) DESC"
	result = db.session.execute(sql)
	return result.fetchall()

def get_all_visible_restaurants():
	sql = "SELECT id,name FROM restaurants WHERE visible=True ORDER BY name"
	result = db.session.execute(sql)
	return result.fetchall()

def get_all_restaurants():
	sql = "SELECT id,name,visible FROM restaurants ORDER BY name"
	result = db.session.execute(sql)
	return result.fetchall()

def get_visible_reviews(name):
	id = get_id(name)
	sql = "SELECT review,stars,username,time FROM reviews WHERE restaurant_id = :id AND visible=TRUE"
	result = db.session.execute(sql, {"name":name,"id":id})
	return result.fetchall()

def get_id(name):
	sql = "SELECT id FROM restaurants WHERE name=:name"
	result = db.session.execute(sql,{"name":name})
	return result.fetchone()[0]
