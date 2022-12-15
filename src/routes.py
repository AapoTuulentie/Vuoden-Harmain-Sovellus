from app import app
from bibtex_creator import create_bibtex_from_all_citations, create_bibtex_from_checked_citations
from flask import redirect, render_template, request, send_file, session
from os import getenv
import users
import citations
import actions
import tags

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    args = request.args
    colors = ["#B6DDFF", "#FFD6BC", "#FCC", "#B0FFA9"]
    if args:
        order_by_type = args.get("order")

        citations_list = citations.form_citations_list(None, order_by_type)
    else:
        citations_list = citations.form_citations_list()
    return render_template("frontpage.html", citations=citations_list, tags=tags.get_tags(), colors=colors)

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
        if len(username) > 30:
            return render_template("errors.html", error="Käyttäjänimessä saa olla enintään 30 merkkiä")
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
    fields = {}
    fields["citationtype"] = request.form["citationtype"]
    fields["title"] = request.form["title"]
    authors = citations.form_authors(request.form["author"])
    fields["authors"] = authors
    fields["year"] = request.form["year"]
    fields["shorthand"] = request.form["citekey"]

    if fields["citationtype"] == "Article":
        fields["journal"] = request.form["journal"]

    if fields["citationtype"] == "Misc":
        fields["howpublished"] = request.form["howpublished"]
        fields["note"] = request.form["note"]

    if not citations.add_citation(fields):
        return render_template("errors.html", error="Viitteen tallennus ei onnistunut")
    return redirect(request.referrer)

@app.route("/delete_citation", methods=["POST"])
def delete_citation():
    if not session:
        return render_template("errors.html", error="Et ole kirjautunut")
    citation_id = request.form["id"]
    citations.delete_citation(citation_id)
    return redirect("/")

@app.route("/modify_citation/<int:citation_id>", methods=["GET", "POST"])
def modify_citation(citation_id):
    if not session:
        return render_template("errors.html", error="Et ole kirjautunut")
    if request.method == "GET":
        return render_template("modify_citation.html", citation=citations.get_one_citation(citation_id))
    if request.method == "POST":
        fields = {}
        fields["type"] = request.form["citationtype"]
        fields["author"] = request.form["author"]
        fields["title"] = request.form["title"]
        fields["year"] = request.form["year"]
        fields["shorthand"] = request.form["shorthand"]
        fields["note"] = request.form["note"]

        if fields["type"] == "Book":
            fields["publisher"] = request.form["publisher"]
            fields["doi"] = request.form["doi"]
            fields["isbn"] = request.form["isbn"]
            fields["pages"] = request.form["pages"]
            fields["editor"] = request.form["editor"]

        if fields["type"] == "Article":
            fields["doi"] = request.form["doi"]
            fields["isbn"] = request.form["isbn"]
            fields["pages"] = request.form["pages"]
            fields["journal"] = request.form["journal"]

        if fields["type"] == "Misc":
            fields["howpublished"] = request.form["howpublished"]

        citations.modify_citation(citation_id, fields)
    return redirect("/")

@app.route("/bib", methods=["POST", "GET"])
def bib():
    username = session.get("user_name")
    id_list = request.form.getlist("check")
    if request.form["nappi"] == "Tarkastele valittujen viitteiden bib-tiedostoa:
        if create_bibtex_from_checked_citations(id_list):
            with open(f"{username}.bib", encoding="utf-8") as f:
                return render_template("bibfile.html", bib=f.read())
    if request.form["nappi"] == "Lataa bib-tiedosto valituista viitteistä":
        if create_bibtex_from_checked_citations(id_list):
            path = f"{username}.bib"
            return send_file(path, as_attachment=True)

@app.route("/tag_citations/<tag>", methods=["POST", "GET"])
def tag_citations(tag):
    if request.method == "POST":
        id_list = request.form.getlist("check")
        citations.tag_citations(tag, id_list)
        return redirect("/")

    citations_list = citations.form_citations_list()
    return render_template("tag_citations.html", citations=citations_list ,tag=tag)

@app.route("/new_tag", methods=["POST"])
def new_tag():
    tag = request.form["tag"]
    tags.new_tag(tag)
    return redirect("/tag_citations/"+tag)

@app.route("/tag/<tag>")
def citations_with_tag(tag):
    citations_list = citations.form_citations_list(tag)
    colors = ["#B6DDFF", "#FFD6BC", "#FCC", "#B0FFA9"]
    return render_template("frontpage.html", citations=citations_list, tags=tags.get_tags(), colors=colors, on_tag=tag)


@app.route("/dlbib")
def download_bib_file():
    if create_bibtex_from_all_citations():
        username = session.get("user_name")
        path = f"{username}.bib"
        return send_file(path, as_attachment=True)

@app.route("/copybib", methods=["GET"])
def display_bib():
    username = session.get("user_name")
    if create_bibtex_from_all_citations():
        with open(f"{username}.bib", encoding="utf-8") as f:
            return render_template("bibfile.html", bib=f.read())
