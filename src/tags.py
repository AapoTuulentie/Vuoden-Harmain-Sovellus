from db import db
from flask import session

def new_tag(tag):
    if not session or tag == "":
        return False
    user_id = session.get("user_id")
    try:
        sql = "INSERT INTO tags (user_id, tag) VALUES (:user_id, :tag)"
        db.session.execute(sql, {"user_id":user_id, "tag":tag})
        db.session.commit()
        return True
    except:
        return False

def get_tags():
    if not session:
        return False
    user_id = session.get("user_id")
    try:
        sql = "SELECT tag FROM tags WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        return result.fetchall()
    except:
        return False
        