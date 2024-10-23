import math


PLAYER_VELOCITY = 3
GRAVITY = 1

class Player:
    def __init__(self, screen):
        self.width, self.height = screen 
        self.player_x = self.width/2
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.player_y = 3
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
    player.player_vel_y = -(player.jump_power*6)
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
        player.jump_power = min(5, player.charge_time * 1/8)
    else:
        release_jump(player)
        player.charge_count = 0
        player.charge_time = 0
        player.space_pressed = False
def gravity(player):
    if player.on_ground == False:
        player.fall_time += 1
        player.player_vel_y += min(1,player.fall_time * GRAVITY)
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
def get_player_bounds(player):
    (x0, y1) = (player.player_x, player.player_y)
    (x1, y0) = (x0 + player.player_width, y1 - player.player_height)
    return (x0, y0, x1, y1)
def handle_vertical_collision(app):
    (pxL,pyU, pxR, pyD) = get_player_bounds(app.player)
    
    for block in app.my_blocks[app.current_level]:
        if (pxL < block.xR and pxR > block.xL):
            
            
            
            if (app.player.player_vel_y > 0 and pyD > block.yU and pyD <= block.yD and pyU < block.yU):
                app.player.player_vel_y = 0
                app.player.player_y = block.yU 
                app.player.on_ground = True
                
               
               #sjekker kollisjon fra under
            if (app.player.player_vel_y < 0) and (pyU <= block.yD +2) and (pyU >= block.yU +2) and (pyD > block.yD-2):
                if ((pxL > block.xL) and (pxL < block.xR)) or ((pxR > block.xL) and (pxR < block.xR)):
                    app.player.player_vel_y = -app.player.player_vel_y *1/2
                    app.player.player_y = block.yD 
                
    
    for block in app.my_blocks[app.current_level]:
        
        if pyD == block.yU and (abs(app.player.player_vel_y) < 1):
            if pxL > block.xR or pxR < block.xL:
                app.player.on_ground = False
                return
            

                
                
        
def handle_horizontal_collision(app):
    (pxL,pyU, pxR, pyD) = get_player_bounds(app.player)
    
    for block in app.my_blocks[app.current_level]:
        
        if ((pyD) < block.yD + 10) and ((pyD) > block.yU - 10):
            if  ((pyU) < block.yD + 10) and ((pyU) > block.yU - 10):   
                #sjekker kollisjon fra høyre 
                if pxL <= block.xR and pxL > block.xL:
                    if app.player.on_ground == False:
                        app.player.player_vel_x = -(app.player.player_vel_x * 7/10)
                    else:
                        app.player.player_vel_x = -app.player.player_vel_x
                    return
                #sjekker kollisjon fra venstre
                if pxR >= block.xL and pxR < block.xR:
                    if app.player.on_ground == False:
                        app.player.player_vel_x = -(app.player.player_vel_x * 7/10)
                    else:
                        app.player.player_vel_x = -app.player.player_vel_x
                        
                    return
def level_checker(app,player):
    if player.player_y < 0:
        app.current_level +=1
        player.player_y = app.height - 5
    if player.player_y > app.height:
        app.current_level -= 1
        player.player_y = 5