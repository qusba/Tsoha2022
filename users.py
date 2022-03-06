import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from flask import session

def register(username,password):
	hash_val = generate_password_hash(password)
	try:
		sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,FALSE)"
		db.session.execute(sql,{"username":username,"password":hash_val})
		db.session.commit()
	except:
		return False
	return login(username,password)

def login(username,password):
	sql = "SELECT username,id,password,admin FROM users WHERE username=:username"
	result = db.session.execute(sql,{"username":username})
	user = result.fetchone()
	if not user:
		return False
	else:
		if check_password_hash(user.password,password):
			session["user_id"] = user.id
			session["username"] = user.username
			session["csrf_token"] = secrets.token_hex(16)
			if user.admin == True:
				session["admin"] = user.admin
			return True
		else:
			return False
def get_token():
	return  session.get("csrf_token",0)

def user_id():
	return session.get("user_id",0)

def is_admin():
	return session.get("admin",False)

def logout():
	del session["user_id"]
	del session["username"]
	if is_admin():
		del session["admin"]
