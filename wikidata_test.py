#!/usr/bin/python3

import requests
import json
import wikipedia
from pprint import pprint
from bs4 import BeautifulSoup

with open('creds/wikidata_keys.json', "r") as file:
    creds = json.load(file)
    access_token = creds["Access_Token"]

def write_file(j, file_name = str()):
    try:
        with open(f"wikifiles/{file_name}.json", "w") as file:
            json.dump(j, file, indent=4)
    except requests.exceptions.JSONDecodeError() as je:
        g = j.content
        print(j.apparent_encoding)
        print(type(j))
    except Exception as e:
        with open(f"wikifiles/{file_name}.json", "x") as file:
            json.dump(j, file)

base_url = "https://en.wikipedia.org/w/api.php"
url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=Colin Turnbull&formatversion=2&rvprop=content&rvslots=*"
action = "query"
headers = {
    "Authorization": f"Bearer {access_token}"
}


def search(name):
    
    
    sr_params = {
    "action": "query",
    "format": "json",
    "list": "search",
    "formatversion": "1",
    "srsearch": name
}
    resp = requests.get(base_url, params=sr_params)
    rj = resp.json()
    result = rj["query"]["search"][0]   
    result["totalhits"] = rj["query"]["searchinfo"]["totalhits"]
    write_file(rj, name)
    return result

auth_name = "obama"
result = search(auth_name)
result_id=result["pageid"]
print(result_id)

a_params = {
    "action": "query",
    "format": "json",
    "pageids": result_id,
    "prop": "info|pageprops|pageterms"
}

op_params = {
    "action": "opensearch",
    "format": "json",
    "search": "Colin Turnbull"
}

# Some kind of ID
filler = "Q11"

entities_params = {
    "action": "wbgetentities",
    "entity": filler
}
query = "T S Elliot"

claims_params = {
    "action": "wbgetclaims",
    "titles": query,
    "sites": "enwiki",
    # "ids": "P17",

   # "props": "claims",
    "format": "json"

}

limit = 5
params = {
    "action": "opensearch",
    "search": query,
    "language": "en",
    "format" : "json",
    "limit": limit, 
}

resp = requests.get(base_url, params=params)        # page_id = rj["query"]["search"][0]["pageid"]
json_resp = resp.json()

print(resp.url)
print(type(json_resp))
status_code = resp.status_code
print(status_code)                                 # # print(status)
write_file(json_resp, "blah")
page_url = json_resp[-1][0]
print(page_url)
print(type(page_url)) 

search_resp = requests.get(page_url, params={"redirects": "return"})        # page_id = rj["query"]["search"][0]["pageid"]
#print(search_json)
print(search_resp.status_code)
print(search_resp.apparent_encoding)
search_json = search_resp.json()

write_file(search_json, "search_json")





# wikidata_ID = list(json_resp["entities"].keys())[0]# author_names = [
# print(f"WIKIDATA_ID: {wikidata_ID}")               #     "D. H. Lawrence",

# name = "D. H. Lawrence"

# page = wikipedia.WikipediaPage(title=name)
# j = page.json()

# def get_page(name):
#     page = wikipedia.WikipediaPage(title=name)
#     wiki_page = BeautifulSoup(page.html(), features="html.parser")
#     return wiki_page


# def get_birthday(wiki_page):
#     page = wikipedia.WikipediaPage(title=name)
#     # page = wikipedia.page(title="joe biden")
#     # print(page.section())

#     bday = wiki_page.find(attrs={"class": "bday"}).text
#     print(bday)


# def get_deathday(wiki_page):
#     pass

# for name in author_names:
#     get_birthday(name)

# # with open("test.html", "w") as file:
# #     file.write(page.html())
# # print(page.content)