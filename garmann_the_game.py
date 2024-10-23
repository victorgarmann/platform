from uib_inf100_graphics.event_app import run_app
import random
from uib_inf100_graphics.helpers import load_image, scaled_image
from PIL import Image
from pathlib import Path
from os.path import isfile, join
from PIL import Image, ImageTk, ImageEnhance
from tkinter import PhotoImage, Tk
from blokker import Block, get_blocks
from player import *

TIMER = 0
def app_started(app):
    app.height = 912
    app.width = 1200
    app.background_width, app.background_height =  app.width, app.height
    app.start = 0
    app.info_mode = "play" #må endre den til menu
    app.timer_delay = 17
    app.screen = (app.width, app.height)
    app.background = get_background("victor_background","bane1.png")
    app.scale_x = 1
    app.scale_y = 1
    app.player = Player(app.screen)
    app.my_blocks = get_blocks(app)
    app.current_level = 0
    

def timer_fired(app):
    global TIMER 
    TIMER+= 1
    handle_vertical_collision(app)
    handle_horizontal_collision(app)
    if app.player.on_ground == False:
        app.player.fall_time += 1
        gravity(app.player)
    elif app.player.fall_time > 3:
        gravity_landed(app.player)
    if app.player.space_pressed:
        charge_jump(app.player)
    level_checker(app, app.player)
    move(app.player)
   


    
def key_pressed(app,event):
        if event.key == "Escape":
            if app.info_mode == "play":
                app.info_mode = "menu"
        if event.key == "Space":
            if app.player.player_vel_y < 1:
                app.player.jump_released = False
                app.player.space_pressed = True
                charge_jump(app.player)
        if (event.key == "Right"):
            if app.player.on_ground == True:
                    app.player.right_pressed = True   
            app.player.player_direction = "east"
        if (event.key == "Up"):
            app.player.player_direction = "north"
        if (event.key == "Left"):
            if app.player.on_ground == True:
                app.player.left_pressed = True   
            app.player.player_direction = "west"
def key_released(app,event):
        if event.key == "Space":
            
            if app.player.player_vel_y < 1:
                app.player.jump_released = True

        if (event.key == "Right"):
            if app.player.on_ground == True:
                app.player.right_pressed = False 
        if (event.key == "Left"):
            if app.player.on_ground == True:
                app.player.left_pressed = False 


def get_background(dir1,dir2):
    path = join( "assets",dir1,dir2)
    image_background1 = load_image(path)
    return image_background1

def draw_background(app, canvas):
    app.background 
    
    #canvas.create_image(app.width/2, app.height/2, pil_image = app.background)
        

def draw_player(screen, app):
    screen.blit(app.player.player, (app.player.player_x, app.player.player_y))
    

def redraw_all(app,canvas):
    
    
    draw_background(app, canvas)
    (x0, y0, x1, y1) = get_player_bounds(app.player)
    canvas.create_rectangle(x0, y0 , x1, y1 , fill="cyan")
    for block in app.my_blocks[app.current_level]:
        block.draw(canvas)
    
    

    
    

        
    
    

    

if __name__ == '__main__':    
    width, height = 1200, 912 
    run_app(width=width, height=height, title='Garmann')
    
        



