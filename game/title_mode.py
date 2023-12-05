from pico2d import *
import game_framework
import play_mode
import logo_mode
import info_mode

global win_w, win_h
win_w, win_h = 1000, 600

def init():
    global image
    global imagestart
    global imagesui
    global imageexit
    global ocean_sound

    ocean_sound = load_music('./sound/ocean.mp3')  # 동시에 여러 음악 재생시 wav로 진행
    ocean_sound.repeat_play()

    image = load_image('./background/bkg3.png')
    imagestart = load_image('./Large Buttons/playui.png')  # 165 ,61
    imagesui = load_image('./Large Buttons/infoui.png')
    imageexit = load_image('./Large Buttons/Quit Button.png')


def finish():
    global image
    global imagestart
    global imagesui
    global imageexit
    del image
    del imagestart
    del imagesui
    del imageexit


def update():
    pass
def draw():
    clear_canvas()
    image.draw(win_w / 2, win_h / 2, win_w * 2, win_h * 2)
    imagesui.draw(win_w / 2 - 165 * 2, win_h / 2, 165, 61)
    imagestart.draw(win_w / 2, win_h / 2 , 165, 61)
    imageexit.draw(win_w / 2 + 165 * 2, win_h / 2 , 165, 61)

    update_canvas()


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN,SDLK_SPACE):
            game_framework.change_mode(play_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # Get mouse click coordinates
            mouse_x, mouse_y = event.x, win_h - 1 - event.y  # Adjust for SDL coordinate system if necessary
            #print(mouse_x, mouse_y)
            # Check if click is within the imagestart area
            if (90 <= mouse_x <= 250) and (270 <= mouse_y <= 330):
                game_framework.change_mode(info_mode)
            if (415 <= mouse_x <= 580) and (270 <= mouse_y <= 330):
                game_framework.change_mode(play_mode)
            if (750 <= mouse_x <= 910 ) and (270<= mouse_y <= 330):
                game_framework.change_mode(logo_mode)
