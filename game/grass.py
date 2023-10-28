from pico2d import load_image

class Grass1:
    def __init__(self):
        self.image = load_image('beachbkg.png')

    def draw(self):
        self.image.draw(400,300,800,600)

    def update(self):
        pass

class Grass2:
    def __init__(self):
        self.image = load_image('beachbkg.png')

    def draw(self):
        self.image.draw(400, 50)

    def update(self):
        pass