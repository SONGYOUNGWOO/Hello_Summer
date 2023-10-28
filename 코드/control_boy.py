from pico2d import *

from grass import Grass1
from grass import Grass2

from boy import Boy
import game_world

# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)


def create_world():
    global running
    global grass
    global grass2
    global team
    global boy

    running = True

    grass = Grass1()
    grass2 = Grass2()
    game_world.add_objects(grass, 1)
    game_world.add_objects(grass2, 0)

    boy = Boy()
    game_world.add_objects(boy, 0)



def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

open_canvas()
create_world()

# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
