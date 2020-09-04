from typing import List, Dict
import urllib.request
import json
import csv



def getData(genres: List[str]) -> List[Dict[str, str]]: # TODO: assumes books don't repeat

    books = [] # holds book objects
    for genre in genres:

        data = _getRequest(genre)

        totalItems = data["totalItems"]

        startIndex = 0
        while startIndex < totalItems:

            data = _getRequest(genre, startIndex=startIndex)

            try: # sometimes the totalItems value is a lie

                for item in data["items"]:

                    try: # some don't have full description

                        if item["volumeInfo"]["language"] == "en": # only use English books

                            title = item["volumeInfo"]["title"]
                            description = item["volumeInfo"]["description"]
                            
                            book = {"title": title, "description": description, "genre": genre}
                            books.append(book)

                    except KeyError:
                        pass

            except KeyError:
                pass

            startIndex += 40

    return books


def toCSV(data: List[Dict[str, str]]) -> None:

    keys = data[0].keys()

    outputFile = open(r"Project\data.csv", 'w', newline='', encoding="utf-8")

    writer = csv.DictWriter(outputFile, keys)
    writer.writeheader()
    writer.writerows(data)




def _getRequest(genre: str, startIndex: int=None) -> Dict[str, str]:

    if ' ' in genre:

        words = genre.split()
        numWords = len(words)
        genreUrl=""

        for i in range(numWords):
            genreUrl = words[i] + "%"

        genreUrl = genreUrl[:-1]

        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genreUrl}&printType=books" if not startIndex else f"https://www.googleapis.com/books/v1/volumes?q=subject:{genreUrl}&maxResults=40&startIndex={startIndex}&printType=books"

    else:

        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&printType=books" if not startIndex else f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults=40&startIndex={startIndex}&printType=books"
    
    request = urllib.request.urlopen(url)
    data = json.loads(request.read().decode())

    return data



if __name__ == "__main__":
    print("starting")

    data = getData(["science fiction", "mystery", "fantasy", "romance", "horror"])
    toCSV(data)

    print("done")