from pico2d import load_image, get_time , delay

class Grass1:
    def __init__(self):
        self.image_grass = load_image('beachbkg.png')

    def draw(self):
        self.image_grass.draw(400, 300, 800, 600)

    def update(self):
        pass


class Grass2:

    def __init__(self):
        self.frame = 0
        self.x, self.y = 400, 270
        self.image = load_image('net.png') #270 x450 :6
    def update(self):
        self.frame = (self.frame + 1) % 6

    def draw(self):
        self.image.clip_composite_draw(self.frame * 45, 0, 45, 450,  - 3.141592 / 100, '', self.x, self.y, 45, 510)
