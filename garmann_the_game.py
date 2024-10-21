from uib_inf100_graphics.event_app import run_app
import random
from uib_inf100_graphics.helpers import load_image, scaled_image
from PIL import Image
from pathlib import Path
from os.path import isfile, join
from PIL import Image, ImageTk, ImageEnhance
from tkinter import PhotoImage, Tk
PLAYER_VELOCITY = 3
GRAVITY = 1

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
    
    

class Player:
    def __init__(self, screen):
        self.width, self.height = screen 
        self.player_x = self.width/2
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.player_y = 0
        self.player_height = 40
        self.player_width = 20
        self.on_ground = False
        self.jump_released = False
        self.space_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.jump_power = 0
        self.scroll_y = 0
        self.collide_left = False
        self.collide_right = False 
        self.fall_time = 0
        self.charge_time = 0
        self.max_charge_count = 5
        self.player_direction = "north"

def release_jump(player):
    player.player_vel_y = -(player.jump_power*3)
    if player.player_direction == "east":
        player.player_vel_x = player.jump_power
    elif player.player_direction == "west":
        player.player_vel_x = -player.jump_power
    player.on_ground = False
    player.jump_power = 0
def charge_jump(player):
    #animate jump  
    if player.charge_time != 0:
        player.player_vel_x = 0
    if player.jump_released == False:
        player.charge_time += 1
        player.jump_power = min(5, player.charge_time * 1/10)
    else:
        release_jump(player)
        player.charge_count = 0
        player.charge_time = 0
        player.space_pressed = False
def gravity(player):
    if player.on_ground == False:
        player.fall_time += 1
        player.player_vel_y += min(1,player.fall_time * GRAVITY*2)
def gravity_landed(player):
        player.fall_time = 0
        player.on_ground = True
        player.player_vel_y = 0
        player.player_vel_x = 0
        player.right_pressed = False
        player.left_pressed = False
        
def move(player):

    player.player_y += player.player_vel_y
    player.player_x += player.player_vel_x
    if player.right_pressed and player.on_ground == True:
        player.player_vel_x = PLAYER_VELOCITY
    if player.left_pressed and player.on_ground == True:
        player.player_vel_x = -PLAYER_VELOCITY
    if player.left_pressed == False and player.right_pressed == False and player.on_ground == True:
        player.player_vel_x = 0
    if player.charge_time == 0:
        player.player_x += player.player_vel_x

def timer_fired(app):
    if app.player.on_ground == False:
        handle_vertical_collision(app)
    if app.player.on_ground == False:
        app.player.fall_time += 1
        gravity(app.player)
    elif app.player.fall_time > 3:
        gravity_landed(app.player)
    if app.player.space_pressed:
        charge_jump(app.player)
    move(app.player)
    convert_coordinates_x(app)
    convert_coordinates_y(app)


    
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
    canvas.create_image(app.width/2, app.height/2, pil_image = app.background)

def draw_player(screen, app):
    screen.blit(app.player.player, (app.player.player_x, app.player.player_y))
    

def redraw_all(app,canvas):
    draw_background(app, canvas)
    
    (x0, y0, x1, y1) = get_player_bounds(app.player)
    canvas.create_rectangle(x0, y0 , x1, y1 , fill="cyan")
    for block in app.my_blocks:
        block.draw(canvas)
    #canvas.create_text(100, 10, text=f"({app.player_vel_x}, {app.right_pressed})", fill="white")
    
def get_player_bounds(player):
    (x0, y1) = (player.player_x, player.player_y)
    (x1, y0) = (x0 + player.player_width, y1 - player.player_height)
    return (x0, y0, x1, y1)
def get_floor_bounds(app):
    return (0, app.height - app.player.player_height, app.width, app.height - app.player.player_height)


    
    
def handle_vertical_collision(app):
    (pxL,pyD, pxR, pyU) = get_player_bounds(app.player)
    for block in app.my_blocks:
        if (pxL < block.xR and pxR > block.xL):
            
            if (pyD >= block.yU and pyD <= block.yU + app.player.player_vel_y):
            
                app.player.player_vel_y = 0
                app.player.player_y = block.yU 
                app.player.on_ground = True
                break
        
        if pyD >= app.height:
            app.player.player_vel_y = 0
            app.player.player_y = app.height - app.player.player_height
            app.player.on_ground = True
            break
        app.player.on_ground = False
        
    
    
def get_blocks(app):
    player_height = app.player.player_height
    return_value = []
    return_value.append(Block(0, (app.height), app.width, app.height - player_height*2, None))
    return return_value
class Block():
    def __init__(self,xL, yD, xR, yU, image):
        self.xL = xL
        self.xR = xR
        self.yD= yD
        self.yU = yU
        self.image = image
    def draw(self, canvas):
        canvas.create_rectangle(self.xL, self.yD, self.xR, self.yU, fill="green")
        #canvas.create_image(self.x+self.width/2, self.y+self.height/2, image=self.image)
    

if __name__ == '__main__':    
    width, height = 1200, 912 
    run_app(width=width, height=height, title='Garmann')
    
        



