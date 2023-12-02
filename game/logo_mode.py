from pico2d import *
import game_framework
import play_mode
# import title_mode

global win_w, win_h
win_w, win_h = 1000, 600

def init():
    global image
    global running
    global logo_start_time

    image = load_image('./logo/HelloSummer.png')
    running = True
    logo_start_time = get_time()


def finish():
    global image
    del image


def update():
    pass
    # global logo_start_time
    # if get_time() - logo_start_time >= 2.0:
    #     game_framework.change_mode(title_mode)


def draw():
    clear_canvas()
    image.draw(win_w / 2, win_h / 2, win_w, win_h)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)

