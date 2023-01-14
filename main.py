import time

import easyocr
import numpy
from PIL import ImageGrab

from pymouse import PyMouse
from pykeyboard import PyKeyboard

DEBUG = True

# 请自行修改为屏幕分辨率！
# Modify this!
screen_x = 3840
screen_y = 2160


class Window:
    m = PyMouse()
    k = PyKeyboard()
    x_dim = 1920
    y_dim = 1080
    reader = easyocr.Reader(['ch_sim', 'en'])

    def __init__(self):
        self.x_dim, self.y_dim = self.m.screen_size()

    def resume_game(self):
        self.m.click(int(self.x_dim / 2 / 2), int(self.y_dim / 2 / 3))

    def right_click(self):
        self.m.click(int(self.x_dim / 2 / 2), int(self.y_dim / 2 / 2), button=2)

    def right_item(self):
        self.m.scroll(vertical=-1)

    def left_item(self):
        self.m.scroll(vertical=1)

    def eat(self):
        x, y = int(self.x_dim / 2 / 2), int(self.y_dim / 2 / 2)
        self.m.press(x, y, button=2)
        time.sleep(2)
        self.m.release(x, y, button=2)

    def get_sound(self) -> dict:
        image = ImageGrab.grab(bbox=(screen_x * 3 / 8, screen_y / 4, screen_x / 2, screen_y / 2))
        data = numpy.asarray(image)
        return self.osr(data)

    def osr(self, data):
        result = self.reader.readtext(data, detail=0)
        print(result)
        return result


class GameState:
    PAUSE = 1
    HALT = 2
    FISHING = 3


if __name__ == '__main__':
    window = Window()
    game_state = GameState.PAUSE

    while True:
        if game_state == GameState.PAUSE:
            window.resume_game()
            window.right_click()
            game_state = GameState.FISHING

        if game_state == GameState.FISHING:
            sounds = window.get_sound()
            if sounds.__contains__('Fishine Bohher splashes') or sounds.__contains__('Fishine Bobher splashes') \
                    or sounds.__contains__('Fishine Bobber splashes'):
                print("Fish!")
                window.right_click()
                game_state = GameState.HALT

        if game_state == GameState.HALT:
            time.sleep(4)
            window.right_click()
            game_state = GameState.FISHING