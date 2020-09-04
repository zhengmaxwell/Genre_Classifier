import xmltodict, json
import urllib.request
from typing import List, Dict
import csv
import string
import re



def getData():

    bookInfos = []

    url = f"https://www.goodreads.com/review/list/118544785.xml?key=rC5pZbFY8SiSaEdXFDuzlA&v=2"

    pageLimit = 200 # max page limit
    pages = int(_getRequest(url)["GoodreadsResponse"]["reviews"]["@total"]) // pageLimit + 2

    for page in range(1, pages):

        data = _getRequest(f"https://www.goodreads.com/review/list/118544785.xml?key=rC5pZbFY8SiSaEdXFDuzlA&v=2&per_page={pageLimit}&page={page}")

        books = data["GoodreadsResponse"]["reviews"]["review"]

        for book in books:

            try:

                book_id = book["book"]["id"]["#text"]
                genre = _checkGenre(book_id)

                title= book["book"]["title_without_series"]
                author = book["book"]["authors"]["author"]["name"]
                description = _cleanData(title, author, book["book"]["description"])

                if not description:
                    continue

                bookInfo = {"title": title, "description": description, "genre": genre}
                bookInfos.append(bookInfo)
            except:
                pass

    return bookInfos


def toCSV(data: List[Dict[str, str]]) -> None:

    keys = data[0].keys()

    outputFile = open(r"src\Project\goodreadsData.csv", 'w', newline='', encoding="utf-8")

    writer = csv.DictWriter(outputFile, keys)
    writer.writeheader()
    writer.writerows(data) 



def _getRequest(url: str) -> Dict[str, str]:
    
    request = urllib.request.urlopen(url)
    xml = request.read().decode()
    parse = xmltodict.parse(xml)
    string = json.dumps(parse)
    data = json.loads(string)

    return data


def _checkGenre(book_id: int) -> str:

    genres = ["romance", "mystery", "sci-fi", "horror", "fantasy"]

    url = f"https://www.goodreads.com/book/show/{book_id}.xml?key=rC5pZbFY8SiSaEdXFDuzlA"

    data = _getRequest(url)

    shelves = data["GoodreadsResponse"]["book"]["popular_shelves"]["shelf"]

    for shelf in shelves:        
        if shelf["@name"] in genres:
            return shelf["@name"]
        

def _cleanData(title: str, author: str, description: str) -> str:

    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    printable = set(string.printable)

    badWords = f"{author}|isbn|{title}|new york times|bestseller"

    cleanString = ''.join(filter(lambda x: x in printable, re.sub('<[^<]+?>', '', description.translate(translator)))) # data cleaning HTML tags and non-ASCII 128 chars

    cleanDescription = []

    for sentence in cleanString.split("."): # removes sentences containing bad words
        if not (re.search(badWords, sentence, flags=re.IGNORECASE)):
            cleanDescription.append(sentence)

    cleanDescription = " ".join(cleanDescription)

    return cleanDescription

    

if __name__ == "__main__":
    print("starting")

    toCSV(getData())

    print("done")