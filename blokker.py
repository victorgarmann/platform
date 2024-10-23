from uib_inf100_graphics.helpers import load_image, scaled_image




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
def get_blocks(app):
    player_height = app.player.player_height
    return_value = []
    return_value.append([])
    return_value[0].append(Block(0, (app.height), app.width, app.height - player_height*2, None))
    return_value[0].append(Block(0,830, 300, 450, None))
    return_value[0].append(Block(880,830, 1200, 460, None))
    return_value[0].append(Block(app.width, app.height, app.width + 20, 0, None))
    return_value[0].append(Block(-20, app.height, 0, 0, None))
    return_value[0].append(Block(450, 220, 730, 100, None))
    return_value.append([])
    
    #return_value[1].append(Block(XL,YD,XR,YU, None))
    return_value[1].append(Block(app.width, app.height, app.width + 20, 0, None))
    return_value[1].append(Block(-20, app.height, 0, 0, None))
    return_value[1].append(Block(740,840, 990, 750, None))
    return_value[1].append(Block(1020,585, 1085, 500, None))
    return_value[1].append(Block(640, 590, 825, 510, None))
    return_value[1].append(Block(300, 420, 480, 260, None))
    return_value[1].append(Block(0, 420, 200, 190, None))
    return_value.append([])
    
    #return_value[1].append(Block(XL,YD,XR,YU, None))
    return_value[2].append(Block(app.width, app.height, app.width + 20, 0, None))
    return_value[2].append(Block(-20, app.height, 0, 0, None))
    return_value[2].append(Block(520,840,640, 770, None))
    return_value[2].append(Block(800,840, 920,773, None))
    return_value[2].append(Block(1061,690,1190, 650, None))
    return_value[2].append(Block(476, 640, 840, 560, None))
    return_value[2].append(Block(720,560, 840, 520, None))
    return_value[2].append(Block(400,420,520, 300, None))
    return_value[2].append(Block(0,280,160, 240, None))
    
    
    return return_value

