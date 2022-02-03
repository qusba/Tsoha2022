from db import db

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

