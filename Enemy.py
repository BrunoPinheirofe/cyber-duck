import math
import random
from pgzero.actor import Actor
from abc import ABC, abstractmethod

class Enemy(ABC):
    """
    Abstract base class for all enemies.
    Handles common properties like health, damage, and movement.
    """
    def __init__(self, pos):
        # The actor is set by the subclass, so we can initialize it here.
        self.actor = Actor("enemy-placeholder.png", pos=pos)
        self.speed = 1.0
        self.damage_output = 10
        self.max_health = 20
        self.health = self.max_health
        
        # Animation state
        self.animation_timer = 0.0
        self.animation_speed = 0.25 # A slightly slower animation speed can look good on enemies
        self.current_frame = 0

    @abstractmethod
    def animate(self, dt):
        """
        Animate the enemy's sprites. This MUST be implemented by subclasses.
        """
        pass

    def move(self, player_pos):
        """
        Move the enemy towards the player's position.
        This can be overridden by subclasses for different movement patterns.
        """
        dx = player_pos[0] - self.actor.x
        dy = player_pos[1] - self.actor.y
        angle = math.atan2(dy, dx)
        self.actor.x += math.cos(angle) * self.speed
        self.actor.y += math.sin(angle) * self.speed

    def update(self, dt, player_pos):
        """
        Main update loop called every frame. Handles moving and animating.
        """
        self.move(player_pos)
        self.animate(dt)

    def draw(self):
        """Draw the enemy on the screen."""
        self.actor.draw()

    def take_damage(self, amount):
        """
        Reduce enemy health. Returns True if the enemy is defeated.
        """
        self.health -= amount
        return self.health <= 0

class Wolf(Enemy):
    """A standard ground-based enemy that chases the player."""
    def __init__(self, pos):
        super().__init__(pos)
        # Wolf-specific stats
        self.speed = random.uniform(1.2, 1.6)
        self.damage_output = 20
        self.max_health = 30
        self.health = self.max_health
        
        # Animation frames
        self.walk_frames = ["wolf-walk1.png", "wolf-walk2.png"]
        self.actor.image = self.walk_frames[0] # Set initial image
        
    def animate(self, dt):
        """Animate the wolf's walking frames."""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0 # Reset timer correctly
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            self.actor.image = self.walk_frames[self.current_frame]

class Bat(Enemy):
    """A faster but more fragile flying enemy with directional sprites."""
    def __init__(self, pos):
        super().__init__(pos)
        # Bat-specific stats
        self.speed = random.uniform(1.8, 2.2)
        self.damage_output = 15
        self.max_health = 20
        self.health = self.max_health
        
        # Directional animation frames
        self.fly_left_frames = ["bat-fly-left1.png", "bat-fly-left2.png"]
        self.fly_right_frames = ["bat-fly-right1.png", "bat-fly-right2.png"]
        self.facing_right = True # Track direction
        
        # Set initial image based on direction
        self.actor.image = self.fly_right_frames[0]
        
    def move(self, player_pos):
        """Override move to update the facing direction before moving."""
        # Determine direction based on player's position
        if player_pos[0] < self.actor.x:
            self.facing_right = False
        else:
            self.facing_right = True
        
        # Call the original move method from the parent class
        super().move(player_pos)

    def animate(self, dt):
        """Animate the bat based on its current facing direction."""
        active_frames = self.fly_right_frames if self.facing_right else self.fly_left_frames
        
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(active_frames)
            self.actor.image = active_frames[self.current_frame]