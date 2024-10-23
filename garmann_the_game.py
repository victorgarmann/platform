from uib_inf100_graphics.event_app import run_app
import random
from uib_inf100_graphics.helpers import load_image, scaled_image
from PIL import Image
from pathlib import Path
from os.path import isfile, join
from PIL import Image, ImageTk, ImageEnhance
from tkinter import PhotoImage, Tk
from blokker import Block, get_blocks
from player import Player, gravity, gravity_landed, move, charge_jump, get_player_bounds, handle_vertical_collision, handle_horizontal_collision


def app_started(app):
    app.height = 912
    app.width = 1200
    app.background_width, app.background_height =  app.width, app.height
    app.start = 0
    app.info_mode = "play" #må endre den til menu
    app.timer_delay = 17
    app.screen = (app.width, app.height)
    app.background = get_background()
    app.scale_x = 1
    app.scale_y = 1
    app.player = Player(app.screen)
    app.my_blocks = get_blocks(app)
    

def timer_fired(app):
    
    handle_vertical_collision(app)
    handle_horizontal_collision(app)
    if app.player.on_ground == False:
        app.player.fall_time += 1
        gravity(app.player)
    elif app.player.fall_time > 3:
        gravity_landed(app.player)
    if app.player.space_pressed:
        charge_jump(app.player)
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
            print("Jump released")
            if app.player.player_vel_y < 1:
                app.player.jump_released = True

        if (event.key == "Right"):
            if app.player.on_ground == True:
                app.player.right_pressed = False 
        if (event.key == "Left"):
            if app.player.on_ground == True:
                app.player.left_pressed = False 
def convert_coordinates_x(app):
    if app.width > 640:
        app.scale_x = app.width // 640
        
    return app.scale_x
def convert_coordinates_y(app):
    if app.height > 640:
        app.scale_y = app.width // 480
    return app.scale_y

def get_background():
    path = join( "assets","victor_background","bane1.png")
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
    for block in app.my_blocks:
        block.draw(canvas)
    #canvas.create_text(100, 10, text=f"({app.player_vel_x}, {app.right_pressed})", fill="white")
    

    
    

        
    
    

    

if __name__ == '__main__':    
    width, height = 1200, 912 
    run_app(width=width, height=height, title='Garmann')
    
        



