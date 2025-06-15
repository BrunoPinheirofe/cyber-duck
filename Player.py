import math
from pgzero.actor import Actor
from pgzero.keyboard import keyboard

class Player:
    def __init__(self, pos):
        self.actor = Actor("duck.png",  pos=pos)
        self.speed = 3
        # Novos atributos para o sistema de XP e Nível
        self.level = 1
        self.experience = 0
        self.xp_to_next_level = 5 # Começa precisando de 5 XP para o primeiro nível
        self.enemy_kills = 0  # Contador de inimigos derrotados
        

    def update(self):
        self.handle_input()
        self.check_boundaries()
        self.check_level_up()

    def draw(self):
        self.actor.draw()

    def handle_input(self):
        dx, dy = 0, 0
        if keyboard.left or keyboard.a: dx -= 1
        if keyboard.right or keyboard.d: dx += 1
        if keyboard.up or keyboard.w: dy -= 1
        if keyboard.down or keyboard.s: dy += 1
        if dx != 0 and dy != 0:
            dx *=  0.707
            dy *= 0.707
        self.actor.x += dx * self.speed
        self.actor.y += dy * self.speed
        self.actor.angle = math.degrees(math.atan2(dy, dx))
        
    def check_boundaries(self):
        if self.actor.left < 0: self.actor.left = 0
        if self.actor.right > self.x: self.actor.right = self.x
        if self.actor.top < 0: self.actor.top = 0
        if self.actor.bottom > self.y: self.actor.bottom = self.y
        
    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= self.xp_to_next_level:
            self.experience -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level *= 1.5 # Aumenta a quantidade de XP necessária para o próximo nível
    def check_level_up(self):
        if self.experience >= self.xp_to_next_level:
            self.level += 1
            self.experience -= self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            print(f"LEVEL UP! Novo Nível: {self.level}")
            game_state = "level_up" # Pausa o jogo e entra no estado de level up
