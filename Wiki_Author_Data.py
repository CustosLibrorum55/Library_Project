import requests 
import json
import os
import datetime
from dateutil import parser
import time
import bs4
from numpy import datetime64

with open('creds/wikidata_keys.json', "r") as file:
    creds = json.load(file)
    access_token = creds["Access_Token"]

base_url = "https://en.wikipedia.org/w/api.php"

class Author:
    """
    Creates an Author object to determina and hold key bio attrs
    """

    def __init__(self, author_folder="AuthorData", **kwargs):
        self.full_name = kwargs["full_name"]
        self.clean_name = ""
        for value in self.full_name.values():
            if value:
                self.clean_name += f"{value} "
        self.clean_name = self.clean_name.strip()
        print(f'Name: {self.clean_name}\n----------------------------------------------------------')
        
        self.wikidata_ID = None
        self.author_folder = author_folder
        self.base_url = "https://www.wikidata.org/w/api.php"

        self.pob = None
        self.dob = None
        self.dod = None
        self.cob = None
        self.gender = None
        self.occupation = None

        self.codes = {
            "DOB": "P569",
            "DOD": "P570",
            "POB": "P19",
            "Country": "P17",
            "town": "P373",
            "country": "P27",
            "gender": "P21"
        }
        
    # Write an obj to file; format= file_name_%M_%S
    def write_file(self, j, file_name):
        file_name = f"{file_name}_{time.strftime('%M_%S')}.json"
        cwd = os.getcwd()
        file_path = os.path.join(cwd, self.author_folder, file_name)
        try:
            with open(file_path, "w") as file:
                json.dump(j, file, indent=4)
        except FileNotFoundError as e:
            with open(file_path, "x") as file:
                json.dump(j, file)

    # Gets the entity json response from wiki
    def get_entities(self, params, fileName="get"):
            resp = requests.get(self.base_url, params=params)
            json_resp = resp.json()
            status_code = resp.status_code
            print(str(status_code) + " Getting")
            self.wikidata_ID = list(json_resp["entities"].keys())[0]
            if self.wikidata_ID == "-1":
                return False
            else:
                self.json_resp = json_resp["entities"][self.wikidata_ID]["claims"]
                self.write_file(json_resp, file_name=fileName)

    # Returns a list of search results
    def search_ent(self, params, fileName="search"):
        occupations = [
            "writer",
            "professor",
            "philosopher",
            "historian",
            "author",
            "playwright",
            "poet",
            "psychiatrist",
            "economist",
            "sociologist",
            "researcher",
        ]
        resp = requests.get(self.base_url, params=params)
        json_search_resp = resp.json()
        numResults = len(json_search_resp["search"])
        self.write_file(json_search_resp, fileName)
        if numResults == 1:
            self.wikidata_ID = json_search_resp["search"][0]["id"]   
            return self.wikidata_ID
        elif numResults != 0:
            for result in json_search_resp["search"]:
                desc = result["display"]["description"]["value"].lower()
                in_occ = any(ele in desc for ele in occupations)
                if in_occ:
                    self.wikidata_ID = result["id"]
                    return self.wikidata_ID
        else:
            return False

    def get_page(self):
        # Full info from wikipedia
        get_params = {
            "action": "wbgetentities",
            "titles": self.clean_name,
            "sites": "enwiki",
            "props": "claims",
            "format": "json"
        }

        # Returns list of possible IDs
        search_params = {
            "action": "wbsearchentities",
            "search": self.clean_name,
            "language": "en",
            "format" : "json" 
        }
        
        if not self.get_entities(get_params, "entTest"):
            t = get_params.pop("titles")
        
            self.wikidata_ID = self.search_ent(search_params, "search_test")
            
            if self.wikidata_ID != False:
                get_params["ids"] = self.wikidata_ID 
                self.get_entities(get_params, "newGet")
        
    # May need to check if date is pos or neg, whichever parser is used. Currently using numpy datetime64 but datetime.datetime has the same problems
    # Could also just create new behavior for ancient authors
    def get_bday(self):
        try:
            bday_obj = self.json_resp[self.codes["DOB"]]
        except Exception as e:
            print("NO BDAY")
            return None
        raw_bday = bday_obj[0]["mainsnak"]["datavalue"]["value"]["time"]
        bday = datetime64(raw_bday.split("T")[0])
        self.dob = bday
        return bday
    
    def get_dday(self):
        dday_obj = self.json_resp[self.codes["DOD"]]
        raw_dday = dday_obj[0]["mainsnak"]["datavalue"]["value"]["time"]
        dday = datetime64(raw_dday.split("T")[0], format="%Y-%M-%D")
        self.dod = dday
        return dday
    
    def get_place_of_birth(self):
        countries_of_citizenship = []

        # Get the country/countries of citizenship from list
        countries = self.json_resp[self.codes["country"]]
        for country in countries:
            country_id = country["mainsnak"]["datavalue"]["value"]["id"]
            country_url = f"https://www.wikidata.org/wiki/{country_id}"
            
            country_response = requests.get(country_url)
            if country_response.status_code == 200:
                # Run BS$ to get country name from wiki page
                soup = bs4.BeautifulSoup(country_response.content, features="html.parser")
                country_name = soup.find(attrs={"class":"wikibase-title-label"}).text
                countries_of_citizenship.append(country_name)
            
        try:
            cob_id = self.json_resp[self.codes["POB"]][0]["qualifiers"]["P17"][0]["datavalue"]["value"]["id"]

            cob_url = f"https://www.wikidata.org/wiki/{cob_id}"
            cob_resp = requests.get(cob_url)
            soup = bs4.BeautifulSoup(cob_resp.content, features="html.parser")
            cob_name = soup.find(attrs={"class":"wikibase-title-label"}).text
            self.cob = cob_name
        except Exception as e:
            print(e)

        # Get town/city of birth name from new wiki page
        pob_obj = self.json_resp[self.codes["POB"]][-1]
        pob_id = pob_obj["mainsnak"]["datavalue"]["value"]["id"]
        params = {
            "action": "wbgetentities",
            "ids": pob_id,
            "sites": "enwiki",
            "props": "claims",
            "format": "json"
        }

        # Get Town/City Name
        resp = requests.get(self.base_url, params=params)
        json_resp = resp.json()
        file_name = f"{pob_id}_{self.full_name['last']}"
        self.write_file(json_resp, file_name)

        town_obj = json_resp["entities"][pob_id]["claims"][self.codes["town"]][0]["mainsnak"]["datavalue"]
        if town_obj["type"] == "string":
            town_name = town_obj["value"]
            print(town_name)

    def get_gender(self):
        gender_id = self.json_resp[self.codes["gender"]][0]["mainsnak"]["datavalue"]["value"]["id"]
        if gender_id == "Q6581097":
            self.gender == 1
        elif gender_id == "Q6581072":
            self.gender == 0

def test_one():

    name = {
        "first": "Nikola",
        "middle": None,
        "last": "Tesla",
        "suffix": None
    }

    au = Author(full_name = name)
    page = au.get_page()
    dob = au.get_bday()
    pob = au.get_place_of_birth()

def test_many():

    test_authors = [
        {
            "first": "Plato",
            "middle": None,
            "last": None,
            "suffix": None  
        },
        {
            "first": "Nikola",
            "middle": None,
            "last": "Tesla",
            "suffix": None
        },
        {
            "first": "T.",
            "middle": "S.",
            "last": "Elliot",
            "suffix": None
        }
    ]
    

    for author in test_authors:
        a = Author(full_name = author)
        page = a.get_page()
        bday = a.get_bday()
        dday = a.get_dday()
        pob = a.get_place_of_birth()
        print("----------------------------------------------------------------------------")


#test_many()