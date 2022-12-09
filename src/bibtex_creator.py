from citations import form_citations_library
from flask import session
#This is as name implies for manual testing purposes,
#Will get deleted when proper tests are made

test = {"1":{
    "type": "book",
    "shorthand": "testi",
    "author" :       "Herra testaaja",
    "title":         "kirjan nimi",
    "pages" :        "1-2",
    "year" :         "1905"
},
"2":{
    "type": "book",
    "shorthand": "testi_TOINEN",
    "author" :       "Herra testaaja",
    "title":         "kirjan nimi",
    "pages" :        "1-2",
    "year" :         ""
}
}
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
                    if citation[key]:
                        bibtex_string +=(f'{key} = "{citation[key]}",\n')
            bibtex_string += "}\n"    
        bibtex = open(f"{username}.bib", "w")
        bibtex.write(bibtex_string)
        bibtex.close()
    except:
        return False        
    return True

def create_bibtex_from_one_citation(id):
    all_citations = get_all_citations()
    username = session.get("user_name")

    try:    
        citation = all_citations[id]

        bibtex_string = (f'@{citation["type"]}\u007b{citation["shorthand"]},\n')
        for key in citation.keys():
            if key not in ["type", "shorthand"]:
                if citation[key]:
                    bibtex_string +=(f'{key} = "{citation[key]}",\n')
        bibtex_string += "}\n"    
        bibtex = open(f'{username}_{citation["shorthand"]}.bib', "w")
        bibtex.write(bibtex_string)
        bibtex.close()
    except:
        return False        
    return True   

()