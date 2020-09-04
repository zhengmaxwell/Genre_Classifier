from pywinauto import Application, mouse
from pywinauto.keyboard import send_keys
import time



def auto(genre: str) -> None:

    for page in range(1, 21):
    
        Application(backend="uia").start(f"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe https://www.goodreads.com/shelf/show/{genre}?page={page}") #pylint: disable=anomalous-backslash-in-string
        Application(backend="uia").connect(path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

        time.sleep(5)

        _scroll_right()

        y = 370
        x = 60

        for i in range(50):  

            if i == 25:
                time.sleep(1)
                y -= 480
                for _ in range(6):
                    _scroll_down()

            mouse.click(coords=(x, y))

            _scroll_down()

            y += 16



def _scroll_right():
    
    send_keys("{VK_RIGHT 13}")


def _scroll_down():

    # Moving down moves 40
    # Each book is 96 away
    # Move down two then move y down 16

    send_keys("{VK_DOWN 2}")



if __name__ == "__main__":
    print('starting')

    genres = ["fantasy", "sci-fi", "horror", "mystery"]

    for genre in genres:
        auto(genre)

    print('done')