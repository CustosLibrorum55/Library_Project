# Created by Brant

import requests
from os import path
import json
import pandas as pd
book_path = 'Book1.xlsx'

xls = pd.ExcelFile(book_path)
sheet_names = xls.sheet_names

searchTerm = "Grammatical Man"
count = 10
authorFirst = "Jeremy"
authorLast = "campbell"

params = {
    "fo": "json",
    "q": searchTerm,
    "c": count,
    "at": "results",
    "fa": f"contributor:{authorFirst}, {authorLast}"
}
base_url = "https://www.loc.gov/books/"
count = 10
title = ""
author_first = "jeremy"
author_last = "campbell"
# search_url = path.join(base_url, search_term, json_string)

url = f'https://www.loc.gov/books/?q={title}&fo=json&c={count}&at=results&fa=contributor:{author_last}, {author_first}'
# url = f'https://www.loc.gov/search/?q=campbell, jeremy&fo=json&c={count}&at=results'
# with open("test.json", "r") as file:
#     r = json.load(file)

def clean(response):
    try:
        content = str(response.content)
        headers = response.headers.__dict__
        respjson = response.json()

        with open("headers.json", "w") as head:
            json.dump(headers, head, indent=4)
        with open("test.json", "w") as test:
            json.dump(respjson, test, indent=4)
    except Exception as e:
        print(f"STATUS: {response.status_code}")
        print(f"Encoding: {response.apparent_encoding}")
        print(e)

    finally:
        return respjson

resp = requests.get(base_url,params=params)
print(resp.url)
r = clean(resp)

# print(type(r))
# results = r["results"]
# num_hits = r["search"]["hits"]
# print(num_hits)
# for result in results:
#     print(result["title"], end="\n\n")


