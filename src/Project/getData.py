from typing import List, Dict
import urllib.request
import json



def getData(genres: List[str]) -> Dict[str, str]: # TODO: assumes books don't repeat

    genreData = {}

    for genre in genres:

        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}"
        request = urllib.request.urlopen(url)
        data = json.loads(request.read().decode())

        totalItems = data["totalItems"]

        books = [] # holds book objects

        startIndex = 0
        while startIndex < totalItems:

            url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults=40&startIndex={startIndex}"
            request = urllib.request.urlopen(url)
            data = json.loads(request.read().decode())


            try: # some don't have items
                for item in data["items"]:
                    try: # some don't have full description
                        title = item["volumeInfo"]["title"]
                        description = item["volumeInfo"]["description"]
                        
                        book = {"title": title, "description": description, "genre": genre}
                        books.append(book)
                    except KeyError:
                        pass
            except KeyError:
                print(startIndex)

            startIndex += 40

        genreData[genre] = {"numBooks": len(books), "books": books}

    print(genreData)







if __name__ == "__main__":
    getData(["romance"])