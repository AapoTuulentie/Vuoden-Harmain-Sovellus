from db import db
from random import choice
from string import ascii_letters, digits
from flask import session


def add_citation(author, title, year, citationtype, journal):
    if not session or title == "" or not year.isdigit():
        return False
    user_id = session.get("user_id")
    characters = ascii_letters + digits
    shorthand = "".join(choice(characters) for i in range(8))
    if citationtype == "Book":
        try:
            sql = "INSERT INTO entries (author, title, year, shorthand, user_id, citationtype) VALUES (:author, :title, :year, :shorthand, :user_id, :citationtype)"
            db.session.execute(sql, {"author":author, "title":title, "year":year, "shorthand":shorthand, "user_id":user_id, "citationtype":citationtype})
            db.session.commit()
            return True
        except:
            return False
    if citationtype == "Article":
        try:
            sql = "INSERT INTO entries (author, title, year, shorthand, user_id, citationtype, journal) VALUES (:author, :title, :year, :shorthand, :user_id, :citationtype, :journal)"
            db.session.execute(sql, {"author":author, "title":title, "year":year, "shorthand":shorthand, "user_id":user_id, "citationtype":citationtype, "journal":journal})
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
    user_id = session.get("user_id")
    try:
        sql = "DELETE FROM entries WHERE id=:id AND user_id=:user_id"
        db.session.execute(sql, {"id":id, "user_id":user_id})
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
                citations_library[citation[0]] = {}

            citations_library[citation[0]]["author"] = citation[1]
            citations_library[citation[0]]["title"] = citation[2]
            citations_library[citation[0]]["publisher"] = citation[3]
            citations_library[citation[0]]["year"] = citation[4]
            citations_library[citation[0]]["doi"] = citation[5]
            citations_library[citation[0]]["isbn"] = citation[6]
            citations_library[citation[0]]["editor"] = citation[7]
            citations_library[citation[0]]["pages"] = citation[8]
            citations_library[citation[0]]["shorthand"] = citation[9]
            citations_library[citation[0]]["type"] = citation[11]
            citations_library[citation[0]]["journal"] = citation[12]
    return citations_library

def form_citations_list():
    citation_list = []
    if not session:
        return False
    citations = get_citations()
    user_id = session.get("user_id")
    for citation in citations:
        (citation_id, author, title, publisher, year,
        doi, isbin, editor, pages, shorthand, user_id, citationtype, journal) = citation
        section = [author, title, publisher, year, doi, isbin, editor, pages, shorthand, citationtype, journal]
        citation_list.append((add_section_to_citation(section), citation_id))
    return citation_list

def add_section_to_citation(section):
    citation_text = ""
    if section[9] != "None" and section[9] != None:
        citation_text += f"Viitteen tyyppi: {section[9]}, "
    if section[0] != "None" and section[0] != None:
        citation_text += f" Kirjoittaja: {section[0]}"
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
    if section[10] != "None" and section[10] != None:
        citation_text += f", Journal: {section[10]}"
    
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

