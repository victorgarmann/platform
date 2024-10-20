from uib_inf100_graphics.event_app import run_app
import random
from uib_inf100_graphics.helpers import load_image, scaled_image
from PIL import Image
from pathlib import Path
from os.path import isfile, join
from PIL import Image, ImageTk, ImageEnhance
from tkinter import PhotoImage, Tk
PLAYER_VELOCITY = 5
GRAVITY = 1

def app_started(app):
    app.height = 480
    app.width = 640
    app.background_width, app.background_height =  app.width, app.height
    app.player_direction = "north"
    app.start = 0
    app.player_x = app.width/2
    app.player_vel_x = 0
    app.player_vel_y = 0
    app.player_y = 0
    app.player_height = 20
    app.player_width = 10
    app.on_ground = False
    app.info_mode = "play" #må endre den til menu
    app.scroll_y = 0
    app.collide_left = False
    app.collide_right = False 
    app.fall_time = 0
    app.charge_time = 0
    app.max_charge_count = 5
    app.jump_power = 0
    app.jump_released = False
    app.space_pressed = False
    app.left_pressed = False
    app.right_pressed = False
    app.timer_delay = 17
    app.screen = (app.width, app.height)
    app.background = get_background()
    app.scale_x = convert_coordinates_x(app)
    app.scale_y = convert_coordinates_y(app)
    app.my_blocks = get_blocks(app)
    
def get_blocks(app):

    return_value = []
    app.scale_x = convert_coordinates_x(app)
    app.scale_y = convert_coordinates_y(app)
    return_value.append(Block(0, (app.height - app.player_height)*app.scale_y, app.width, app.player_height, None))
    return return_value
    ...
def convert_coordinates_x(app):
    app.scale_x = 1
    if app.width > 640:
        app.scale_x = app.width // 640
    return app.scale_x
def convert_coordinates_y(app):
    app.scale_y = 1
    if app.height > 640:
        app.scale_y = app.width // 480
    return app.scale_y

def key_pressed(app, event):
    if event.key == "Escape":
        if app.info_mode == "play":
            app.info_mode = "menu"
    if event.key == "Space":
        print("Jump pressed")
        if app.player_vel_y < 1:
            app.jump_released = False
            app.space_pressed = True
            charge_jump(app)
    if (event.key == "Right"):
        if app.on_ground == True:
                app.right_pressed = True   
        app.player_direction = "east"
    if (event.key == "Up"):
        app.player_direction = "north"
    if (event.key == "Left"):
        if app.on_ground == True:
            app.left_pressed = True   
        app.player_direction = "west"
        
def key_released(app, event):
    if event.key == "Space":
        print("Jump released")
        if app.player_vel_y < 1:
            app.jump_released = True
            
    if (event.key == "Right"):
        #if app.on_ground == True:
        app.right_pressed = False 
    if (event.key == "Left"):
        if app.on_ground == True:
            app.left_pressed = False 

def charge_jump(app):
    #animate jump  
    if app.charge_time != 0:
        app.player_vel_x = 0
        
    if app.jump_released == False:
        app.charge_time += 1
        app.jump_power = min(5, app.charge_time * 1/10)
    else:
        release_jump(app)
        app.charge_count = 0
        app.charge_time = 0
        app.space_pressed = False
def release_jump(app):
    app.player_vel_y = -(app.jump_power*3)
    if app.player_direction == "east":
        app.player_vel_x = app.jump_power*3
    elif app.player_direction == "west":
        app.player_vel_x = -app.jump_power*3
    app.on_ground = False
    app.jump_power = 0

    
def gravity(app):
    if app.on_ground == False:
        app.fall_time += 1
        app.player_vel_y += min(1,app.fall_time * GRAVITY*2)
        
def gravity_landed(app):
        app.fall_time = 0
        app.on_ground = True
        app.player_vel_y = 0
        app.player_vel_x = 0
        app.player_y = app.height - app.player_height
def move(app):
    app.player_y += app.player_vel_y
    app.player_x += app.player_vel_x
    print(app.player_x)
    

def timer_fired(app):
    app.on_ground = handle_vertical_collision(app)
    if app.on_ground == False:
        app.fall_time += 1
        gravity(app)
    elif app.fall_time > 3:
        gravity_landed(app)

    if app.space_pressed:
        charge_jump(app)

    # Continuous movement when holding arrow keys
    if app.right_pressed:
        app.player_vel_x = PLAYER_VELOCITY
    elif app.left_pressed:
        app.player_vel_x = -PLAYER_VELOCITY
    elif app.right_pressed == False and app.left_pressed == False:
        app.player_vel_x = 0  # Stop when no key is pressed
    move(app)
    
def get_background():
    path = join( "assets","victor_background","background_1.png")
    image_background1 = load_image(path)
    return image_background1

def draw_background(app, canvas):
    app.background 
    canvas.create_image(app.width/2, app.height/2, pil_image = app.background)

def draw_player(app, screen):
    screen.blit(app.player, (app.player_x, app.player_y))
    

def redraw_all(app, canvas):
    draw_background(app, canvas)
    sy = app.scroll_y
    (x0, y0, x1, y1) = get_player_bounds(app)
    canvas.create_rectangle(x0, y0 - sy, x1, y1 - sy, fill="cyan")
    for block in app.my_blocks:
        block.draw(canvas)
    canvas.create_text(100, 10, text=f"({app.player_vel_x}, {app.right_pressed})", fill="white")
    
def get_player_bounds(app):
    (x0, y1) = (app.player_x, app.player_y)
    (x1, y0) = (x0 + app.player_width, y1 - app.player_height)
    return (x0, y0, x1, y1)
def get_floor_bounds(app):
    return (0, app.height - app.player_height, app.width, app.height - app.player_height)


    
    
def handle_vertical_collision(app):
    (px0,py0, px1, py1) = get_player_bounds(app)
    fy0 = app.height - app.player_height
    for block in app.my_blocks:
        if (px0 <= block.x + block.width and px1 >= block.x and
            py1 > block.y + block.height + 5 and py1 < block.y):
            app.player_vel_y = 0
            app.player_y = block.y - app.player_height
            return True
    if py1 < fy0 :
        app.on_ground = False
    else:
        app.on_ground = True
    
    return app.on_ground

class Block():
    def __init__(self,x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill="green")
        #canvas.create_image(self.x+self.width/2, self.y+self.height/2, image=self.image)
    

if __name__ == '__main__':    
    width, height = 640, 480 
    run_app(width=width, height=height, title='Garmann')
    
        



