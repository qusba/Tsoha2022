from db import db

def get_groups():
	sql = "SELECT name,id,visible FROM groups"
	result = db.session.execute(sql)
	return result

def get_visible_groups():
	sql = "SELECT name FROM groups WHERE visible = TRUE"
	result = db.session.execute(sql)
	return result

def add_group(name):
	try:
		sql = "INSERT INTO groups (name, visible) VALUES (:name,TRUE)"
		db.session.execute(sql,{"name":name})
		db.session.commit()
		return True
	except:
		return False

def delete_group(id,action):
	sql = "SELECT count(name) FROM groups WHERE id=:id"
	result = db.session.execute(sql,{"id":id})
	result = result.fetchone()
	if result != 0:
		sql ="UPDATE groups SET visible = :action WHERE id = :id"
		db.session.execute(sql,{"id":id,"action":action})
		db.session.commit()
		return True
	else:
		return False
