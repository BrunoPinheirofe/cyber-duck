from pgzero.actor import Actor
import math
import random



class Enemy:
    def __init__(self, pos):
        self.x, self.y = pos
        start_pos = self.get_random_spawn_pos()
        
        self.actor = Actor("wolf.png", pos=start_pos)
        self.speed = 3

    def update(self, player_pos):
        dx = player_pos[0] - self.actor.x
        dy = player_pos[1] - self.actor.y
        angle = math.atan2(dy, dx)
        self.actor.x += math.cos(angle) * self.speed
        self.actor.y += math.sin(angle) * self.speed
        
    def draw(self):
        self.actor.draw()
        
    def get_random_spawn_pos(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top': return (random.randint(0, self.x), -30)
        if side == 'bottom': return (random.randint(0, self.x), self.y + 30)
        if side == 'left': return (-30, random.randint(0, self.y))
        if side == 'right': return (self.x + 30, random.randint(0, self.y))
