from secrets import token_hex
from flask import abort, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db

def login(name, password):
    sql = "SELECT id, name, password FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["csrf_token"] = token_hex(16)
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session ["csrf_token"]

def check_if_logged_in():
    return session.get("user_id")

def new_user(name, password):
    if name == "" or password == "":
        return False

    pwhash = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password)
                 VALUES (:name, :password)"""
        db.session.execute(sql, {"name":name, "password":pwhash})
        db.session.commit()
    except:
        return False
    return login(name, password)

def check_csrf(token):
    if session["csrf_token"] != token:
        abort(403)
