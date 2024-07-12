import requests
import json

class Book:

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.baseUrl = "https://openlibrary.org/search.json"
        self.publishers = []

    def get_basic_info(self):
        headers = {
            "User-Agent": "PersonalLibraryBuilder/1.0 (brant.jolly@gmail.com)"
        }
        fields = [
            "author_name",
            "first_publish_year",
            "number_of_pages_median",
            "publisher",
            "title",
            "type",
            "subject",
            "language",
            "cover_edition_key",
            "subtitle",
            "editions",
        ]
        params = {
            "title": self.title,
            "author": self.author,
            "page/limit" : 20,
            "format": "json",
            "fields": ",".join(fields),
        }
        # Add Headers before final run
        resp = requests.get(self.baseUrl, params=params)
        with open("ol-test2.json", "w") as olFile:
            json.dump(resp.json(), olFile, indent=2)
        self.respJson = resp.json()["docs"][0]
        numFound = resp.json()["numFound"]
        self.cover_edition_key = self.respJson["cover_edition_key"]
        print(f"numFound: {numFound}")

    def get_subtitle(self):
        coverEditionUrl = f"https://openlibrary.org/works/{self.cover_edition_key}.json"
        covEdResp = requests.get(coverEditionUrl).json()
        with open("ed_test.json", "w") as ed:
            json.dump(covEdResp, ed, indent=2)



title = "Psycholinguisitics"
author = "Donald Foss"
b = Book(title=title, author=author)
b.get_basic_info()
b.get_subtitle()
#b.get_year()
#b.get_publishers()

