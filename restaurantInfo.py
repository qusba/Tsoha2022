from db import db
import restaurants

def add_info(restaurant_id,title,info):
	sql = "INSERT INTO restaurantInfo (restaurant_id,title,info,visible) VALUES (:restaurant_id, :title, :info, TRUE)"
	db.session.execute(sql, {"restaurant_id":restaurant_id,"title":title,"info":info})
	db.session.commit()

def get_visible_info(name):
        id = restaurants.get_id(name)
        sql = "SELECT title,info FROM restaurantInfo WHERE restaurant_id = :id AND visible=TRUE"
        result = db.session.execute(sql, {"name":name,"id":id})
        return result.fetchall()

def info_query(query):
	sql = "SELECT * FROM restaurants a, restaurantInfo i WHERE a.id=i.restaurant_id AND i.info LIKE :query"
	result = db.session.execute(sql,{"query":"%"+query+"%"})
	return result.fetchall()
