from pico2d import load_image
import game_world
import random

class Boll:
    image = None

    def __init__(self):
        if Boll.image == None:
            Boll.image = load_image('./ball/ballRoll.png') # 120x 70
        self.x, self.y = random.randint(0, 800), 599
        self.frame = 0


    def update(self):
        self.frame = (self.frame + 1) % 8
        if self.y > 70:
            self.y -= random.randint(1, 30)


    def draw(self):
        self.image.clip_draw(self.frame * 15, 0, 15, 70, self.x, self.y, 15, 70)






