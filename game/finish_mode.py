import random

from pico2d import *
import game_framework
import play_mode
import logo_mode
import info_mode

global win_w, win_h
win_w, win_h = 1000, 600
game_state = '진행 중'

def init():
    global image_won
    global image_victory
    global image_defeat
    global bkg
    global defeat_sound
    global victory_sound

    bkg = load_image('./background/sky.png')
    image_won = load_image('./background/won.png')
    image_victory = load_image('./background/victory.png')
    image_defeat = load_image('./background/defeat.png')
    defeat_sound = load_music('./sound/defeat.mp3')  # 동시에 여러 음악 재생시 wav로 진행
    defeat_sound.set_volume(24)
    victory_sound = load_music('./sound/victory.mp3')  # 동시에 여러 음악 재생시 wav로 진행
    victory_sound.set_volume(24)
    if play_mode.ally_score >= 5:
        victory_sound.play()
    else:
        defeat_sound.play()



def finish():
    global image_won
    global image_victory
    global image_defeat
    del image_won
    del image_victory
    del image_defeat

def update():
    pass

def draw():
    clear_canvas()
    bkg.draw(win_w / 2, win_h / 2, win_w , win_h )
    #print(play_mode.ally_score, play_mode.enemy_score)
    if play_mode.ally_score >= 5:
        image_victory.draw(win_w / 2, win_h / 2, 300, 100)
    if play_mode.enemy_score >= 5:
        image_defeat.draw(win_w / 2, win_h / 2 , 300, 100)
    update_canvas()

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN,SDLK_SPACE):
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            game_framework.change_mode(play_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # Get mouse click coordinates
            mouse_x, mouse_y = event.x, win_h - 1 - event.y  # Adjust for SDL coordinate system if necessary
            print(mouse_x, mouse_y)
            # Check if click is within the imagestart area
            if (90 <= mouse_x <= 250) and (270 <= mouse_y <= 330):
                game_framework.change_mode(info_mode)
            if (415 <= mouse_x <= 580) and (270 <= mouse_y <= 330):
                game_framework.change_mode(play_mode)
            if (750 <= mouse_x <= 910 ) and (270<= mouse_y <= 330):
                game_framework.change_mode(logo_mode)
