from citations import form_citations_library
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

def create_bibtex():
    all_citations = get_all_citations()
    try:
        for citation in all_citations.values():
            bibtex_string = (f'@{citation["type"]}\u007b{citation["shorthand"]},\n')
            for key in citation.keys():
                if key not in ["type", "shorthand"]:
                    if citation[key]:
                        bibtex_string +=(f'{key} = "{citation[key]}",\n')
            bibtex_string += "}\n"    
            bibtex = open("bibtex.bib", "a")
            bibtex.write(bibtex_string)
            bibtex.close()
    except:
        return False        
    return True
