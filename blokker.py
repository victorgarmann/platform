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
    return_value.append(Block(0, (app.height), app.width, app.height - player_height*2, None))
    return_value.append(Block(130, app.height - player_height*2, 200, app.height - player_height*4, None))
    return_value.append(Block(230, app.height - player_height*4, 400, app.height - player_height*6, None))
    return_value.append(Block(app.width, app.height, app.width + 20, 0, None))
    return return_value