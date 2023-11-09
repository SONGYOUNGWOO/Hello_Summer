from pico2d import load_image, get_time , delay

class Beach:
    def __init__(self):
        self.image_grass = load_image('./background/beachbkg.png')

    def draw(self):
        self.image_grass.draw(400, 300, 800, 600)

    def update(self):
        pass


class Net:
    def __init__(self):
        self.bool = False
        self.frame = 0
        self.x, self.y = 400, 270
        self.image = load_image('./background/net.png') #270 x450 :6
    def update(self):
        if self.bool:
            self.frame = (self.frame + 1) % 6
            self.bool = False
        else:
            self.bool = True

    def draw(self):
        self.image.clip_composite_draw(self.frame * 45, 0, 45, 450,  - 3.141592 / 100, '', self.x, self.y, 45, 510)
