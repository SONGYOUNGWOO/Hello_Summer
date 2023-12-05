from pico2d import *
import game_framework
import play_mode
import title_mode

global win_w, win_h
win_w, win_h = 1000, 600

def init():
    global imagelogo
    global running
    global logo_start_time
    global ocean_sound


    ocean_sound = load_music('./sound/ocean.mp3')  # 동시에 여러 음악 재생시 wav로 진행
    ocean_sound.repeat_play()

    imagelogo = load_image('./logo/HelloSummer.png')
    running = True
    logo_start_time = get_time()


def finish():
    global imagelogo
    del imagelogo


def update():
    global logo_start_time
    if get_time() - logo_start_time >= 10.0:
        game_framework.change_mode(title_mode)
    pass



def draw():
    clear_canvas()
    imagelogo.draw(win_w / 2, win_h / 2, win_w, win_h)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            else:
                game_framework.change_mode(title_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            game_framework.change_mode(title_mode)

