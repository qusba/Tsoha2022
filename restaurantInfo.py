from db import db

def add_info(restaurant_id,title,info):
	sql = "INSERT INTO restaurantInfo (restaurant_id,title,info,visible) VALUES (:restaurant_id, :title, :info, TRUE)"
	db.session.execute(sql, {"restaurant_id":restaurant_id,"title":title,"info":info})
	db.session.commit()
