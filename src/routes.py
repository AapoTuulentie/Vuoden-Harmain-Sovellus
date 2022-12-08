from app import app

from flask import redirect, render_template, request, session
from os import getenv
import users
import citations
import actions

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    citations_list = citations.form_citations_list()
    return render_template("frontpage.html", citations=citations_list)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        return render_template("errors.html", error="Väärä käyttäjätunnus tai salasana")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("errors.html", error="Salasanat eivät ole samat")
        if len(password1) < 8:
            return render_template("errors.html",
                                   error="Salasanassa pitää olla vähintään 8 merkkiä")
        if len(password1) > 30:
            return render_template("errors.html", error="Salasanassa saa olla enintään 30 merkkiä")
        users.new_user(username, password1)
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/reset_database", methods=["POST"])
def reset_database():
    actions.reset_database()
    return redirect("/")

@app.route("/add_citation", methods=["POST"])
def add_citation():
    if not session:
        return render_template("errors.html", error="Et ole kirjautunut")
    title = request.form["title"]
    author = request.form["author"]
    year = request.form["year"]
    if not citations.add_citation(author, title, year):
        return render_template("errors.html", error="Ei onnistunut")
    return redirect(request.referrer)

@app.route("/delete_citation", methods=["POST"])
def delete_citation():
    if not session:
        return render_template("errors.html", error="Et ole kirjautunut")
    id = request.form["id"]
    citations.delete_citation(id)
    return redirect("/")

@app.route("/modify_citation/<int:id>", methods=["GET", "POST"])
def modify_citation(id):
    if not session:
        return render_template("errors.html", error="Et ole kirjautunut")
    if request.method == "GET":
        return render_template("modify_citation.html", citation=citations.get_one_citation(id))
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        publisher = request.form["publisher"]
        year = request.form["year"]
        doi = request.form["doi"]
        isbn = request.form["isbn"]
        editor = request.form["editor"]
        pages = request.form["pages"]
        shorthand = request.form["shorthand"]
        citations.modify_citation(id, author, title, publisher, year, doi, isbn, editor, pages, shorthand)
    return redirect("/")

    
