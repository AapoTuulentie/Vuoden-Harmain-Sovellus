from citations import form_citations_library
from flask import session

def get_all_citations():
    return form_citations_library()

def create_bibtex_from_all_citations():
    username = session.get("user_name")

    all_citations = get_all_citations()
    bibtex_string = ""
    try:
        for citation in all_citations.values():
            bibtex_string += (f'@{citation["type"]}\u007b{citation["shorthand"]},\n')
            for key in citation.keys():
                if key not in ["type", "shorthand", "user_id"]:
                    if citation[key] and citation[key] != "None":
                        bibtex_string +=(f'{key} = "{citation[key]}",\n')
            bibtex_string += "}\n"
        bibtex = open(f"{username}.bib", "w")
        bibtex.write(bibtex_string)
        bibtex.close()
    except:
        return False
    return True

def create_bibtex_from_checked_citations(id_list):
    username = session.get("user_name")
    all_citations = get_all_citations()
    bibtex_string = ""

    try:
        for one_id in id_list:
            citation = all_citations[int(one_id)]
            bibtex_string += (f'@{citation["type"]}\u007b{citation["shorthand"]},\n')
            for key in citation.keys():
                if key not in ["type", "shorthand", "user_id"]:
                    if citation[key]:
                        bibtex_string +=(f'{key} = "{citation[key]}",\n')
            bibtex_string += "}\n"
        bibtex = open(f"{username}.bib", "w")
        bibtex.write(bibtex_string)
        bibtex.close()
    except:
        return False
    return True
