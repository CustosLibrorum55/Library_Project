import sqlite3
import pandas as pd
from pprint import pprint
import name_cleaner
import Wiki_Author_Data
import os
import openpyxl

# Load the main book
book_path = 'Book1.xlsx'
xls = pd.ExcelFile(book_path)
sheet_names = xls.sheet_names
conn = sqlite3.connect('books.db')
invalids = []


"""
need to first check is book or author name is already present in the db
then assign book a new book_id & author new author_id
filter out misc authors and create custom behavior  
    create new csv for misc authors & remove from main excel
    Author, Title, Subtitle, Publisher, Date, COllection, Edition, Box
! figure out many to many relationship and create link between books and authors 
search book info and fill out book table entry
search author nfo and fill out author table entry

"""

def load_excel():
    errors = []
    # Iterate through the different sheets & open dataframes
    for sheet_name in sheet_names[3:7]:
        print(f"Sheet Name: {sheet_name}")
        df = pd.read_excel(xls, sheet_name=sheet_name)
        sheet_authors = df["Author"]
    return df

def author_info(df):
	# List out all the authors and clean the names
        for sauth in df["Author"][:3]:
            print(sauth)
            full_name = name_cleaner.main(sauth)
            for name in full_name:
                print(name)
                last = name["last"]
                if last != "misc" and last != None:
                    path = f"AuthorData/{last}"
                    
                    try:
                        os.mkdir(path)
                    except FileExistsError as fe:
                        pass
                        
                    author = Wiki_Author_Data.Author(full_name=name, author_folder=path)
                    page_found = author.get_page() 
                    print(f"ID: {author.wikidata_ID}")
                    if author.wikidata_ID:
                        dob = author.get_bday()
                        print(dob)

                    if not page_found:
                        invalids.append(sauth)
            #if p != "error": 
             #   author.get_gender()
            #print(f'GENDER: {author.gender}')
        # Create a table name based on the sheet name, or use a custom naming scheme
        table_name = sheet_name.replace(' ', '_') # Example: replace spaces with underscores
        #df.to_sql(table_name, conn, if_exists='replace', index=False)
load_excel()
print("DONE")
print(invalids)
