import math
from pgzero.actor import Actor
from pgzero.keyboard import keyboard

class Player:
    """Represents the player character, handling movement, stats, and animations."""
    def __init__(self, pos):
        self.actor = Actor("duck-idle1.png", pos=pos)
        
        self.speed = 3
        self.max_health = 100
        self.health = self.max_health
        self.level = 1
        self.experience = 0
        self.xp_to_next_level = 50
        self.projectile_base_damage = 25
        self.enemies_killed = 0

        # Gem-based healing attributes
        self.gems_collected_for_heal = 0
        self.gems_needed_for_hp_point = 20

        # Animation attributes
        self.idle_frames = ["duck-idle1.png", "duck-idle2.png"]
        self.walk_left_frames = ["duck-walk-left1.png", "duck-walk-left2.png"]
        self.walk_right_frames = ["duck-walk-right1.png", "duck-walk-right2.png"]
        self.animation_timer = 0.0
        self.animation_speed = 0.2
        self.current_frame = 0
        self.is_moving = False
        self.face_right = True

        # Orbital Weapon attributes
        self.orbital_weapon_active = False
        self.orbital_actor = None
        self.orbital_distance = 45
        self.orbital_angle = 0
        self.orbital_rotation_speed = 2.5
        self.orbital_damage = 15

    def update(self, dt, screen_width, screen_height):
        """Update player state each frame."""
        self.handle_input()
        self.check_boundaries(screen_width, screen_height)
        self.animate(dt)
        if self.orbital_weapon_active:
            self.update_orbital_weapon(dt)

    def draw(self):
        """Draw the player on the screen."""
        self.actor.draw()

    def handle_input(self):
        """Process keyboard inputs for movement."""
        dx, dy = 0, 0
        if keyboard.left or keyboard.a:
            dx -= 1
            self.face_right = False
        if keyboard.right or keyboard.d:
            dx += 1
            self.face_right = True
        if keyboard.up or keyboard.w:
            dy -= 1
        if keyboard.down or keyboard.s:
            dy += 1
        
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
            
        self.actor.x += dx * self.speed
        self.actor.y += dy * self.speed
        self.is_moving = dx != 0 or dy != 0

    def animate(self, dt):
        self.animation_timer += dt
        
        active_frames = self.idle_frames
        if self.is_moving:
            active_frames = self.walk_right_frames if self.face_right else self.walk_left_frames

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(active_frames)
            self.actor.image = active_frames[self.current_frame]

    def check_boundaries(self, screen_width, screen_height):
        """Prevent the player from moving off-screen."""
        self.actor.left = max(self.actor.left, 0)
        self.actor.right = min(self.actor.right, screen_width)
        self.actor.top = max(self.actor.top, 0)
        self.actor.bottom = min(self.actor.bottom, screen_height)

    def add_experience(self, amount):
        """Adds experience and checks for level up."""
        self.experience += amount
        leveled_up = False
        while self.experience >= self.xp_to_next_level:
            self.experience -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            print(f"LEVEL UP! New Level: {self.level}")
            leveled_up = True
        return leveled_up

    def process_gem_collection(self, xp_from_gem=10):
        """Processes a collected gem, adding XP and checking for healing."""
        leveled_up = self.add_experience(xp_from_gem)
        self.gems_collected_for_heal += 1
        if self.gems_collected_for_heal >= self.gems_needed_for_hp_point:
            self.heal(1)
            self.gems_collected_for_heal = 0
        return leveled_up

    def take_damage(self, amount):
        """Reduces player health."""
        if self.health > 0:
            self.health = max(0, self.health - amount)

    def heal(self, amount):
        """Increases player health."""
        self.health = min(self.max_health, self.health + amount)
        print(f"Player healed by {amount}. Current health: {self.health}")

    # --- Orbital Weapon Methods ---
    def activate_orbital_weapon(self):
        """Activates the orbital weapon if it's not already active."""
        if not self.orbital_weapon_active:
            self.orbital_weapon_active = True
            self.orbital_actor = Actor("orbital_blade.png")
            self.update_orbital_weapon(0) # Set initial position
            print("Orbital Blade Unlocked!")

    def add_orbital_weapon(self, rotation_speed_increase=0):
        """Activates the orbital weapon if it's not already active, or increases its speed."""
        if not self.orbital_weapon_active:
            self.orbital_weapon_active = True
            # Create the first orbital blade
            self.orbital_actor = Actor("orbital_blade.png")
            self.update_orbital_weapon(0) # Set initial position
            print("Orbital Blade Unlocked!")
        else:
            # If already active, just increase speed
            self.increase_orbital_rotation_speed(rotation_speed_increase)


    def update_orbital_weapon(self, dt):
        """Updates the position and angle of the orbital weapon."""
        if not self.orbital_actor: return
        self.orbital_angle = (self.orbital_angle + self.orbital_rotation_speed * dt) % (2 * math.pi)
        offset_x = math.cos(self.orbital_angle) * self.orbital_distance
        offset_y = math.sin(self.orbital_angle) * self.orbital_distance
        self.orbital_actor.pos = (self.actor.x + offset_x, self.actor.y + offset_y)
        self.orbital_actor.angle = math.degrees(-self.orbital_angle)

    def draw_orbital_weapon(self):
        """Draws the orbital weapon if active."""
        if self.orbital_actor:
            self.orbital_actor.draw()

    # --- Upgrade Methods (called by Items) ---
    def increase_projectile_damage(self, amount):
        self.projectile_base_damage += amount
        print(f"Projectile Damage increased to: {self.projectile_base_damage}")

    def increase_movement_speed(self, amount):
        self.speed += amount
        print(f"Movement Speed increased to: {self.speed}")

    def increase_max_health(self, amount):
        self.max_health += amount
        self.heal(amount) # Also heal for the increased amount
        print(f"Max Health increased to: {self.max_health}. Current Health: {self.health}")

    def increase_orbital_damage(self, amount):
        if self.orbital_weapon_active:
            self.orbital_damage += amount
            print(f"Orbital Damage increased to: {self.orbital_damage}")

    def increase_orbital_rotation_speed(self, amount):
        if self.orbital_weapon_active:
            self.orbital_rotation_speed += amount
            print(f"Orbital Rotation Speed increased to: {self.orbital_rotation_speed}")