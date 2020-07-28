import csv
import re
import string
from typing import List, Dict



def _cleanData(title: str, author: str, description: str) -> str:

    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    printable = set(string.printable)

    badWords = f"{author}|isbn|{title}|new york times|bestseller|provided"

    cleanString = ''.join(filter(lambda x: x in printable, re.sub('<[^<]+?>', '', description.translate(translator)))) # data cleaning HTML tags and non-ASCII 128 chars
    cleanString = re.sub(r"[,;@#?!&$-]+\ *", " ", cleanString) # removes punctuation
    cleanString = cleanString.replace("\'\'", '') # removes quotes
    cleanString = cleanString.replace('\"', '')

    cleanDescription = []

    for sentence in cleanString.split("."): # removes sentences containing bad words
        if not (re.search(badWords, sentence, flags=re.IGNORECASE)):
            cleanDescription.append(sentence.lower())

    cleanDescription = " ".join(cleanDescription)

    return cleanDescription


def toCSV(data: List[Dict[str, str]]) -> None:

    keys = data[0].keys()

    outputFile = open(r"data\openLibraryData.csv", 'w', newline='', encoding="utf-8")

    writer = csv.DictWriter(outputFile, keys)
    writer.writeheader()
    writer.writerows(data) 


if __name__ == "__main__":

    reader = csv.DictReader(open(r"C:\Users\Maxwell\OneDrive\Desktop\openLIbraryData.csv", encoding="utf8"))

    cleanedData = []

    for row in reader:
        description = _cleanData(row["title"], row["author"], row["description"])
        if description:
            book = {"title": row["title"].lower(), "description": description, "genre": row["genre"]}
            cleanedData.append(book)

    toCSV(cleanedData)


