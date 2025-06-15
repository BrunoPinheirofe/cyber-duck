from pgzero.actor import Actor
import math
import random


class Enemy:
    def __init__(self, pos):
        # The 'pos' argument is the intended spawn position.
        # The get_random_spawn_pos logic was redundant and incorrectly using
        # the components of 'pos' as boundaries.
        self.actor = Actor("wolf-atack.png", pos=pos)
        self.speed = 1.5 # Adjusted speed
        self.damage_output = 20 # Dano que este inimigo causa ao jogador
        self.max_health = 30
        self.health = self.max_health

    def update(self, player_pos):
        dx = player_pos[0] - self.actor.x
        dy = player_pos[1] - self.actor.y
        angle = math.atan2(dy, dx)
        self.actor.x += math.cos(angle) * self.speed
        self.actor.y += math.sin(angle) * self.speed

    def draw(self):
        self.actor.draw()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True # Inimigo derrotado
        return False # Inimigo ainda vivo
