from pico2d import open_canvas, delay, close_canvas
import game_framework
import logo_mode as start_mode
import play_mode

global win_w, win_h

win_w ,win_h = 1000, 600

open_canvas(win_w, win_h, sync=False)
game_framework.run(start_mode)
close_canvas()

