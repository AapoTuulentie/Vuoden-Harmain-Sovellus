from db import db
from random import choice
from string import ascii_letters, digits
from flask import session
import re


def add_citation(fields):
    if not session or fields["title"] == "" or not fields["year"].isdigit():
        return False
    user_id = session.get("user_id")
    if fields["shorthand"] == "":
        characters = ascii_letters + digits
        shorthand = "".join(choice(characters) for i in range(8))
    else:
        shorthand = fields["shorthand"]
    if fields["citationtype"] == "Book":
        try:
            sql = """INSERT INTO entries (author,
                                        title,
                                        year,
                                        shorthand,
                                        user_id,
                                        citationtype)
                                    VALUES (:author,
                                            :title,
                                            :year,
                                            :shorthand,
                                            :user_id,
                                            :citationtype)"""
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
            sql = """INSERT INTO entries (author,
                                        title,
                                        year,
                                        shorthand,
                                        user_id,
                                        citationtype,
                                        journal)
                                VALUES (:author,
                                        :title,
                                        :year,
                                        :shorthand,
                                        :user_id,
                                        :citationtype,
                                        :journal)"""
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
            sql = """INSERT INTO entries (author,
                                        title,
                                        year,
                                        shorthand,
                                        user_id,
                                        citationtype,
                                        howpublished,
                                        note)
                                  VALUES (:author,
                                        :title,
                                        :year,
                                        :shorthand,
                                        :user_id,
                                        :citationtype,
                                        :howpublished,
                                        :note)"""
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
        sql = "SELECT * FROM entries WHERE user_id=:user_id ORDER BY author ASC"
        result = db.session.execute(sql, {"user_id":user_id})
        return result.fetchall()
    except:
        return False

def get_citations_ordred_by_type():
    if not session:
        return False
    user_id = session.get("user_id")
    try:
        sql = "SELECT * FROM entries WHERE user_id=:user_id ORDER BY citationtype, author ASC"
        result = db.session.execute(sql, {"user_id":user_id})
        return result.fetchall()
    except:
        return False

def get_citations_with_tag(tag):
    if not session:
        return False
    user_id = session.get("user_id")
    try:
        sql = "SELECT * FROM entries WHERE tag =:tag AND user_id=:user_id ORDER BY author ASC"
        result = db.session.execute(sql, {"tag":tag, "user_id":user_id})
        return result.fetchall()
    except:
        return False


def delete_citation(citation_id):
    if not session:
        return False
    user_id = session.get("user_id")
    try:
        sql = "DELETE FROM entries WHERE id=:id AND user_id=:user_id"
        db.session.execute(sql, {"id":citation_id, "user_id":user_id})
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

def form_citations_list(tag = None, order_by = None):
    citation_list = []
    if not session:
        return False
    if tag is None:
        if order_by:
            citations = get_citations_ordred_by_type()
        else:
            citations = get_citations()

    else:
        citations = get_citations_with_tag(tag)
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
        if section[x] != "None" and section[x] is not None:
            citation_text += f"{info[x]}: {section[x]}, "

    return citation_text[:-2]

def get_one_citation(citation_id):
    if not session:
        return False
    try:
        sql = "SELECT * FROM entries WHERE id=:id"
        result = db.session.execute(sql, {"id":citation_id})
        return result.fetchall()[0]
    except:
        return False

def check_correct_user(user_id):
    if not session:
        return False
    try:
        sql = "SELECT user_id FROM entries WHERE id=:id"
        result = db.session.execute(sql, {"id":user_id})
        return result.fetchone()[0]
    except:
        return False

def modify_citation(citation_id, fields):
    if not session:
        return False
    authors = form_authors(fields["author"])
    user_id = session.get("user_id")
    #Otin t??st?? check_correct_user tarkistamisen pois. K??ytt??j??n varmistamiseen riitt???? vain user_id=user_id sql-haun per??ss??
    if fields["type"] == "Book":
        try:
            sql = """UPDATE entries SET author=:author, title=:title,
            publisher=:publisher, year=:year, doi=:doi, isbn=:isbn, editor=:editor,
            pages=:pages, shorthand=:shorthand, note=:note WHERE id=:citation_id AND user_id=:user_id"""

            db.session.execute(sql, {"citation_id":citation_id, "user_id":user_id, "author":authors, "title":fields["title"],
            "publisher":fields["publisher"], "year":fields["year"], "doi":fields["doi"], "isbn":fields["isbn"],
            "editor":fields["editor"], "pages":fields["pages"], "shorthand":fields["shorthand"], "note":fields["note"]})

            db.session.commit()
        except:
            return False

    if fields["type"] == "Article":
        try:
            sql = """UPDATE entries SET author=:author, title=:title,
            year=:year, doi=:doi, isbn=:isbn, pages=:pages,
            shorthand=:shorthand, journal=:journal, note=:note WHERE id=:citation_id AND user_id=:user_id"""

            db.session.execute(sql, {"citation_id":citation_id, "user_id":user_id, "author":authors, "title":fields["title"],
            "year":fields["year"], "doi":fields["doi"], "isbn":fields["isbn"], "pages":fields["pages"],
            "shorthand":fields["shorthand"], "journal":fields["journal"], "note":fields["note"]})

            db.session.commit()
        except:
            return False
    
    else:
        try:
            sql = """UPDATE entries SET author=:author, title=:title,
            year=:year, shorthand=:shorthand, howpublished=:howpublished,
            note=:note WHERE id=:citation_id AND user_id=:user_id"""

            db.session.execute(sql, {"citation_id":citation_id, "user_id":user_id, "author":authors, "title":fields["title"],
            "year":fields["year"], "shorthand":fields["shorthand"], "howpublished":fields["howpublished"], "note":fields["note"]})

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
    for auth in authors:
        names = auth.split(" ")
        full_names.append(names)
    full_names.sort(key=lambda s: s[len(s)-1].lower())
    return full_names

def tag_citations(tag, id_list):
    if not session:
        return False
    user_id = session.get("user_id")
    id_list = tuple(id_list)
    print(id_list)
    try:
        sql = """UPDATE entries SET tag=:tag WHERE id IN :id_list AND user_id=:user_id"""
        db.session.execute(sql, {"tag":tag, "id_list":id_list, "user_id":user_id})
        db.session.commit()
    except:
        return False
