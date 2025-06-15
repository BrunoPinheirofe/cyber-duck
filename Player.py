import math
from pgzero.actor import Actor
from pgzero.keyboard import keyboard


class Player:
    def __init__(self, pos):
        self.actor = Actor("duck-idle1.png", pos=pos)
        self.speed = 3

        self.max_health = 100
        self.health = self.max_health # Vida do jogador
        self.level = 1
        self.experience = 0
        self.xp_to_next_level = 5  # Começa precisando de 5 XP para o primeiro nível
        self.enemies_killed = 0  # Contador de inimigos derrotados

        # animations
        self.idle_frames = ["duck-idle1.png", "duck-idle2.png"]
        self.walk_left_frames = ["duck-walk-left1.png", "duck-walk-left2.png"]
        self.walk_right_frames = ["duck-walk-right1.png", "duck-walk-right2.png"]

        self.animation_timer = 0.0
        self.animation_speed = 0.2  # Tempo entre as animações
        self.current_frame = 0
        self.is_moving = False
        self.face_right = True

    def update(self, dt, screen_width=800, screen_height=600):
        self.handle_input()
        self.check_boundaries(screen_width, screen_height)
        self.animate(dt)

    def draw(self):
        self.actor.draw()

    def handle_input(self):
        dx, dy = 0, 0
        if keyboard.left or keyboard.a:
            dx -= 1
            self.face_right = False # Update direction when moving left
        if keyboard.right or keyboard.d:
            dx += 1
            self.face_right = True  # Update direction when moving right
        if keyboard.up or keyboard.w:
            dy -= 1
        if keyboard.down or keyboard.s:
            dy += 1
        
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
        self.actor.x += dx * self.speed
        self.actor.y += dy * self.speed

        self.is_moving = dx != 0 or dy != 0
        # If dx is 0 (only vertical movement), self.face_right retains its last horizontal direction.

    def animate(self, dt):
        self.animation_timer += dt

        # Determine which set of frames to use
        if self.is_moving:
            if self.face_right:
                active_frames = self.walk_right_frames
            else:
                active_frames = self.walk_left_frames
        else: # Player is idle
            # Currently, idle frames are right-facing.
            active_frames = self.walk_left_frames

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(active_frames)

            self.actor.image = active_frames[self.current_frame]

            # The block below was causing issues by incorrectly overriding the image.
            # It has been removed as the active_frames logic above now correctly
            # selects the appropriate animation based on self.face_right and self.is_moving.
            # if not self.face_right:
            #     self.actor.image = (
            #         self.actor.image.replace("duck-walk-left", "duck-walk-right")
            #         if "walk-left" in self.actor.image
            #         else self.actor.image.replace("duck-idle", "duck-walk-right")
            #     )

    def check_boundaries(self, screen_width=800, screen_height=600):
        # Player's position is self.actor.x and self.actor.y
        # Use the screen_width and screen_height parameters directly for boundary checks.
        if self.actor.left < 0:
            self.actor.left = 0
        if self.actor.right > screen_width:
            self.actor.right = screen_width
        if self.actor.top < 0:
            self.actor.top = 0
        if self.actor.bottom > screen_height:
            self.actor.bottom = screen_height

    def add_experience(self, amount):
        self.experience += amount
        leveled_up_this_call = False
        while self.experience >= self.xp_to_next_level:
            self.experience -= self.xp_to_next_level
            self.level += 1
            # Aumenta a quantidade de XP necessária para o próximo nível
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            print(f"LEVEL UP! Novo Nível: {self.level}")
            leveled_up_this_call = True
        return leveled_up_this_call

    # def check_level_up(self): # This method is now redundant
    #     if self.experience >= self.xp_to_next_level:
    #         self.level += 1
    #         self.experience -= self.xp_to_next_level
    #         self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
    #         print(f"LEVEL UP! Novo Nível: {self.level}")
    #         # game_state = "level_up" # Player class should not directly modify global game_state
