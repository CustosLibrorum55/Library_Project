#!/usr/bin/python3

import requests
import json
import wikipedia
from pprint import pprint

with open('creds/wikidata_keys.json', "r") as file:
    creds = json.load(file)
    access_token = creds["Access_Token"]

def write_file(j, file_name = str()):
    try:
        with open(f"wikifiles/{file_name}.json", "w") as file:
            json.dump(j, file, indent=4)
    except Exception as e:
        with open(f"wikifiles/{file_name}.json", "x") as file:
            json.dump(j, file)

base_url = "https://en.wikipedia.org/w/api.php"
url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=Colin Turnbull&formatversion=2&rvprop=content&rvslots=*"
action = "query"
headers = {
    "Authorization": f"Bearer {access_token}"
}


# def search(name):
    
    
#     sr_params = {
#     "action": "query",
#     "format": "json",
#     "list": "search",
#     "formatversion": "1",
#     "srsearch": name
# }
#     resp = requests.get(base_url, params=sr_params)
#     rj = resp.json()
#     result = rj["query"]["search"][0]   
#     result["titalhits"] = rj["query"]["searchinfo"]["totalhits"]
#     write_file(rj, name)
#     return result

# auth_name = "obama"
# result = search(auth_name)
# result_id=result["pageid"]

# a_params = {
#     "action": "query",
#     "format": "json",
#     "pageids": result_id,
#     "prop": "info|pageprops|pageterms"
# }

# op_params = {
#     "action": "opensearch",
#     "format": "json",
#     "search": "Colin Turnbull"
# }

# resp = requests.get(f"https://www.wikidata.org/w/api.php?action=wbgetentities&props=claims&ids={result_id}&format=json")
# status = resp.status_code
# rj = resp.json()
# write_file(rj, "blah")

# # page_id = rj["query"]["search"][0]["pageid"]


# print(status)


name = "Joe Biden"
page = wikipedia.WikipediaPage(title=name)
print(page)
pprint(page.sections)
# with open("test.html", "x") as file:
#     file.write(page.html())
# print(page.content)