from pgzero.actor import Actor
import math
import random


class Enemy:
    def __init__(self, pos):
        # The 'pos' argument is the intended spawn position.
        # The get_random_spawn_pos logic was redundant and incorrectly using
        # the components of 'pos' as boundaries.
        self.actor = Actor("wolf-atack.png", pos=pos)
        self.speed = 1 # Adjusted speed for testing, can be 2 or other value
        self.damage = 20 # Amount of damage this enemy deals on collision
    def update(self, player_pos):
        dx = player_pos[0] - self.actor.x
        dy = player_pos[1] - self.actor.y
        angle = math.atan2(dy, dx)
        self.actor.x += math.cos(angle) * self.speed
        self.actor.y += math.sin(angle) * self.speed

    def draw(self):
        self.actor.draw()
