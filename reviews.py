from db import db
import restaurants

def review(stars,review,user_id,r_name):
	sql1 = "SELECT id FROM restaurants WHERE name=:r_name"
	restaurant_id = db.session.execute(sql1,{"r_name":r_name})
	restaurant_id = restaurant_id.fetchone()[0]

	sql2 = "SELECT username FROM users WHERE id=:user_id"
	username = db.session.execute(sql2,{"user_id":user_id})
	username = username.fetchone()[0]

	sql3 = "INSERT INTO reviews (restaurant_id,stars,review,visible,username,time) VALUES (:restaurant_id,:stars,:review,TRUE,:username,NOW())"
	result = db.session.execute(sql3,{"restaurant_id":restaurant_id,"stars":stars,"review":review,"username":username})
	db.session.commit()

def get_visible_reviews(name):
        id = restaurants.get_id(name)
        sql = "SELECT review,stars,username,time FROM reviews WHERE restaurant_id = :id AND visible=TRUE"
        result = db.session.execute(sql, {"id":id})
        return result.fetchall()

def get_all_reviews(name):
	id = restaurants.get_id(name)
	sql = "SELECT id,review,stars,username,visible FROM reviews WHERE restaurant_id = :id"
	result = db.session.execute(sql, {"id":id})
	return result.fetchall()

def modify_review(id,visible):
	sql = "SELECT count(review) FROM reviews WHERE id=:id"
	result=db.session.execute(sql,{"id":id})
	result = result.fetchone()
	if result[0] != 0:
		sql =  "UPDATE reviews SET visible=:visible WHERE id=:id"
		db.session.execute(sql, {"id":id, "visible":visible})
		db.session.commit()
		return True
	else:
		return False


