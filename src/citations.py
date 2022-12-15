from db import db
from random import choice
from string import ascii_letters, digits
from flask import session
import re


def add_citation(fields):
    if not session or fields["title"] == "" or not fields["year"].isdigit():
        return False
    user_id = session.get("user_id")
    characters = ascii_letters + digits
    shorthand = "".join(choice(characters) for i in range(8))
    if fields["citationtype"] == "Book":
        try:
            sql = "INSERT INTO entries (author, title, year, shorthand, user_id, citationtype) VALUES (:author, :title, :year, :shorthand, :user_id, :citationtype)"
            db.session.execute(sql, {
                "author":fields["authors"],
                "title":fields["title"],
                "year":fields["year"],
                "shorthand":shorthand,
                "user_id":user_id,
                "citationtype":fields["citationtype"]
                })
            db.session.commit()
            return True
        except:
            return False
    if fields["citationtype"] == "Article":
        try:
            sql = "INSERT INTO entries (author, title, year, shorthand, user_id, citationtype, journal) VALUES (:author, :title, :year, :shorthand, :user_id, :citationtype, :journal)"
            db.session.execute(sql, {
                "author":fields["authors"],
                "title":fields["title"],
                "year":fields["year"],
                "shorthand":shorthand,
                "user_id":user_id,
                "citationtype":fields["citationtype"],
                "journal":fields["journal"]
                })
            db.session.commit()
            return True
        except:
            return False
    if fields["citationtype"] == "Misc":
        try:
            sql = "INSERT INTO entries (author, title, year, shorthand, user_id, citationtype, howpublished, note) VALUES (:author, :title, :year, :shorthand, :user_id, :citationtype, :howpublished, :note)"
            db.session.execute(sql, {
                "author":fields["authors"],
                "title":fields["title"],
                "year":fields["year"],
                "shorthand":shorthand,
                "user_id":user_id,
                "citationtype":fields["citationtype"],
                "howpublished":fields["howpublished"],
                "note":fields["note"]
                })
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
            citations_library[citation[0]]["howpublished"] = citation[14]
            citations_library[citation[0]]["note"] = citation[15]
    return citations_library

def form_citations_list():
    citation_list = []
    if not session:
        return False
    citations = get_citations()
    for citation in citations:
        (citation_id, author, title, publisher, year,
        doi, isbin, editor, pages, shorthand, user_id, citationtype, journal, tag, howpublished, note) = citation
        section = [citationtype, author, title, publisher, year, doi, isbin, editor, pages, shorthand, journal, howpublished, note]
        citation_list.append((add_section_to_citation(section), citation_id))
    return citation_list

def add_section_to_citation(section):

    info = ["Viitteen tyyppi", "Kirjoittaja", "Otsikko", "Julkaisija",
     "Vuosi", "Doi", "Isbn", "Editor", "Sivut", "Shorthand", "Journal"]

    citation_text = ""

    for x in range(11):
        if section[x] != "None" and section[x] != None:
            citation_text += f"{info[x]}: {section[x]}, "
    
    return citation_text[:-2]

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
    authors = form_authors(author)
    if check_correct_user(id) == session.get("user_id"):
        try:
            sql = """UPDATE entries SET author=:author, title=:title,
            publisher=:publisher, year=:year, doi=:doi, isbn=:isbn, editor=:editor,
            pages=:pages, shorthand=:shorthand WHERE id=:id"""

            db.session.execute(sql, {"id":id, "author":authors, "title":title,
            "publisher":publisher, "year":year, "doi":doi, "isbn":isbn,
            "editor":editor, "pages":pages, "shorthand":shorthand})

            db.session.commit()
        except:
            return False

def form_authors(author):
    full_names = arrange_authors(author)
    result = ""
    for i in range(0, len(full_names)):
        for j in range(0, len(full_names[i])):
            if j == len(full_names[i])-1 and i != len(full_names)-1:
                result += f"{full_names[i][j]}, "
            elif i == len(full_names)-1 and j == len(full_names[i])-1:
                result += f"{full_names[i][j]}"
            else:
                result += f"{full_names[i][j]} "
    return result

def arrange_authors(author):
    authors = re.split(r"\s*;\s*|\s*,\s*", author)
    full_names = []
    for author in authors:
        names = author.split(" ")
        full_names.append(names)
    full_names.sort(key=lambda s: s[len(s)-1].lower())
    return full_names