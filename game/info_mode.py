from pico2d import *
import game_framework
import title_mode
import logo_mode

global win_w, win_h
win_w, win_h = 1000, 600

def init():
    global image
    global imagestart
    global imagesui
    global imageexit
    global ocean_sound
    image = load_image('./background/info2.png')
    ocean_sound = load_music('./sound/ocean.mp3')  # 동시에 여러 음악 재생시 wav로 진행
    ocean_sound.repeat_play()



def finish():
    global image
    del image


def update():
    pass
def draw():
    clear_canvas()
    image.draw(win_w / 2, win_h / 2, win_w +20, win_h +20)
    update_canvas()


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
