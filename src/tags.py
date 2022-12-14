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

#def delete_tag(tag):