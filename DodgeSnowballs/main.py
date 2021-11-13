
from ursina import *
from random import randint
import time

def update():
    global snowballs, eggs, score, text, counter, real, okay, nope, player

    if (counter < 500):
        counter += 1
        real.y = 10
        real = Text(text = f"{nope}", position = (.65, .4), origin = (0, 0), scale = 2, color = color.yellow, background = True)

    if counter == 500:
       real.y = 10
       real = Text(text = f"{okay}", position = (.65, .4), origin = (0, 0), scale = 2, color = color.yellow, background = True)

    player.x += held_keys['right arrow'] * time.dt * player.dx
    player.x -= held_keys['left arrow'] * time.dt * player.dx

    for snowball in snowballs:
        snowball.y += time.dt * snowball.dy
        if snowball.y < -5:
          snowball.y = 7
          snowball.x = randint(-6, 6)
          snowball.dy -= 0.5
          score += 1
          text.y = 10
          text = Text(text = f"Score: {score}", position = (-.65, .4), origin = (0, 0), scale = 2, color = color.yellow, background = True)
          snowball.color = color.white
          snowball.collider = 'box'

    if player.x < -6:
       if held_keys['left arrow']:
            player.x = -6
            
    if player.x > 6:
        if held_keys['right arrow']:
            player.x = 6

    hit_info = player.intersects()
    if hit_info.hit:
        Entity(model = "quad", scale = 60, color = color.gray)
        player.y =10
        Text(text = "You Lost ;-;", origin = (0,0), scale = 2, color = color.yellow, background = True)
        Audio('sad')
        for snowball in snowballs:
            snowball.dy = 0

    for egg in eggs:
        egg.y += time.dt * egg.dy
        hit_info = egg.intersects()
        if hit_info.hit:
            egg.x = 10
            if hit_info.entity in snowballs:
                hit_info.entity.collider = None
                hit_info.entity.color = color.rgba(255, 255, 255, 0)
                
def input(key):
    global eggs, counter 
    if (key == 'space') and (counter == 500):
      egg = Egg()
      eggs.append(egg)
      counter = 0

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'cube'
        self.scale_y = 1
        self.scale_x = 0.5
        self.color = color.orange
        self.position = (0, -2.5)
        self.collider = 'box'
        self.dx = 5

class Snowball(Entity):
    def __init__(self):
        super().__init__()
        self.model = "sphere"
        self.texture = "Snowball"
        self.color = color.white
        self.scale = 0.7
        self.position = (randint(-6,6), 7)
        self.collider = 'box'
        self.dy = -3


class Egg(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'sphere'
        self.texture = 'Egg'
        #self.color = color.green
        self.scale = 0.9
        self.position = player.position
        self.y = player.y + 1
        self.collider = 'box' 
        self.dy = 4

app=Ursina()

field_size = 19
Entity(model='quad', scale = (18, 12), texture = 'clouds')
field = Entity(model = 'quad', color= color.rgba(255, 255, 255, 0), scale = (12, 18), position = (field_size//2, field_size//2, -.01))
player= Player()
snowballs = []
eggs = []
counter = 500
score = 0 
text=Text(text="")
real = Text(text="")
okay = "egg is ready"
nope = "wait for egg"

for i in range(15):
    snowball = Snowball()
    snowballs.append(snowball)

app.run()
