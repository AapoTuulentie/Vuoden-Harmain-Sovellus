from db import db
from flask import session

def add_citation(author, title, year):
    if not session or title == "" or not year.isdigit():
        return False
    user_id = session.get("user_id")
    try:
        sql = "INSERT INTO entries (author, title, year, user_id) VALUES (:author, :title, :year, :user_id)"
        db.session.execute(sql, {"author":author, "title":title, "year":year, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False
    
def get_citations():
    if not session:
        return False
    user_id = session.get("user_id")
    try:
        sql = "SELECT * FROM entries WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        return result.fetchall()
    except:
        return False

def delete_citation(id):
    if not session:
        return False
    try:
        sql = "DELETE FROM entries WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False

        
def form_citations_library():
    citations_library = {}
    if session:
        citations = get_citations()
        for citation in citations:
            if citation[0] not in citations_library.keys():
                citations_library[0] = {}
            citations_library[citation[0]]["author"] = citations[1]
            citations_library[citation[0]]["title"] = citations[2]
            citations_library[citation[0]]["publisher"] = citations[3]
            citations_library[citation[0]]["year"] = citations[4]
            citations_library[citation[0]]["doi"] = citations[5]
            citations_library[citation[0]]["isbn"] = citations[6]
            citations_library[citation[0]]["editor"] = citations[7]
            citations_library[citation[0]]["pages"] = citations[8]
            citations_library[citation[0]]["shorthand"] = citations[9]
            citations_library[citation[0]]["type"] = citations[10]
    return citations_library

def form_citations_list():
    citation_list = []
    if not session:
        return False
    citations = get_citations()
    for citation in citations:
        author = citation[1]
        title = citation[2]
        publisher = citation[3]
        year = citation[4]
        doi = citation[5]
        isbin = citation[6]
        editor = citation[7]
        pages = citation[8]
        shorthand = citation[9]
        section = [author, title, publisher, year, doi, isbin, editor, pages, shorthand]
        citation_list.append((add_section_to_citation(section), citation[0]))
    return citation_list

def add_section_to_citation(section):
    citation_text = ""
    if section[0] != "None" and section[0] != None:
        citation_text += f"Kirjoittaja: {section[0]}"
    if section[1] != "None" and section[1] != None:
        citation_text += f", Otsikko: {section[1]}"
    if section[2] != "None" and section[2] != None:
        citation_text += f", Julkaisija: {section[2]}"
    if section[3] != "None" and section[3] != None:
        citation_text += f", Vuosi: {section[3]}"
    if section[4] != "None" and section[4] != None:
        citation_text += f", Doi: {section[4]}"
    if section[5] != "None" and section[5] != None:
        citation_text += f", Isbin: {section[5]}"
    if section[6] != "None" and section[6] != None:
        citation_text += f", Editor: {section[6]}"
    if section[7] != "None" and section[7] != None:
        citation_text += f", Sivut: {section[7]}"
    if section[8] != "None" and section[8] != None:
        citation_text += f", Shorthand: {section[8]}"
    return citation_text

def get_one_citation(id):
    if not session:
        return False
    try:
        sql = "SELECT * FROM entries WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        return result.fetchall()[0]
    except:
        return False

def check_correct_user(id):
    if not session:
        return False
    try:
        sql = "SELECT user_id FROM entries WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        return result.fetchone()[0]
    except:
        return False

def modify_citation(id, author, title, publisher, year, doi, isbn, editor, pages, shorthand):
    if not session:
        return False
    if check_correct_user(id) == session.get("user_id"):
        try:
            sql = """UPDATE entries SET author=:author, title=:title,
            publisher=:publisher, year=:year, doi=:doi, isbn=:isbn, editor=:editor,
            pages=:pages, shorthand=:shorthand WHERE id=:id"""

            db.session.execute(sql, {"id":id, "author":author, "title":title,
            "publisher":publisher, "year":year, "doi":doi, "isbn":isbn,
            "editor":editor, "pages":pages, "shorthand":shorthand})

            db.session.commit()
        except:
            return False
            
