from typing import List, Dict
import urllib.request
import json
import csv



def getData(genres: List[str]):

    books = []

    for genre in genres:

        url = f"https://openlibrary.org/subjects/{genre}.json"

        pageLimit = 1000
        pages = _getRequest(url)["ebook_count"] // pageLimit

        for i in range(pages):

            offset = pageLimit*i

            subject_url = f"https://openlibrary.org/subjects/{genre}.json?limit={pageLimit}&offset={offset}"

            subjectData = _getRequest(subject_url)
            
            for work in subjectData["works"]:

                try: # some don't have openlibrary_edition
                
                    olid = work["availability"]["openlibrary_edition"]

                    book_url = f"https://openlibrary.org/api/books?bibkeys=OLID:{olid}&jscmd=details&format=json"

                    bookData = _getRequest(book_url)

                    try: # some don't have description

                        bookDetails = bookData[f"OLID:{olid}"]["details"]
                        description = bookDetails["description"]["value"]
                        title = bookDetails["title"]
                        author = bookDetails["authors"][0]["name"]
                        lang = bookDetails["languages"][0]["key"]

                        if lang == "/languages/eng":
                            
                            if genre == "mystery_and_detective_stories":
                                genre = "mystery"

                            book = {"title": title, "author": author, "description": description, "genre": genre}
                            books.append(book)

                    except:
                        pass
                except:
                    pass

    return books


def toCSV(data: List[Dict[str, str]]) -> None:

    keys = data[0].keys()

    outputFile = open(r"src\Project\openLibraryData.csv", 'w', newline='', encoding="utf-8")

    writer = csv.DictWriter(outputFile, keys)
    writer.writeheader()
    writer.writerows(data) 
            
        
        
def _getRequest(url: str) -> Dict[str, str]:

        request = urllib.request.urlopen(url)
        data = json.loads(request.read().decode())

        return data

    

if __name__ == "__main__":
    print("asdf")
    genres = ["romance", "horror", "science_fiction", "mystery_and_detective_stories", "fantasy"]
    toCSV(getData(genres))