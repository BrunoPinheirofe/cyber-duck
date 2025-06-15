
import pgzrun
import math
import random
from pygame.rect import Rect
from Player import Player
from Enemy import Enemy

# --- GAME WINDOW CONFIGURATION ---
WIDTH = 800
HEIGHT = 600
TITLE = "Cyber-Duck: Data Survival"

# --- GAME STATES ---
# Controls the current state of the game (Menu, Playing, Game Over).
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

# --- INITIAL SETUP ---
game_state = GameState.MENU
sound_enabled = True
elapsed_time = 0

# --- HEALTH DISPLAY CONFIGURATION ---
NUM_HEART_CONTAINERS = 5
HEART_IMAGE_WIDTH = 16  # Assuming heart images are 16px wide. Adjust if different.
HEART_SPACING = 4       # Spacing between hearts.

# --- GAME OBJECT LISTS ---
enemies = []
projectiles = []
experience_gems = []

# --- MENU BUTTONS ---
# Define rectangles for menu buttons to detect clicks.
play_button = Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50)
sound_button = Rect(WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50)
exit_button = Rect(WIDTH / 2 - 100, HEIGHT / 2 + 140, 200, 50)


# --- RESET GAME FUNCTION ---
def reset_game():
    """Resets all game variables to their initial state."""
    global player, enemies, projectiles, experience_gems, elapsed_time
    
    # Initialize the player at the center of the screen
    player = Player((WIDTH / 2, HEIGHT / 2))
    
    # Clear all game object lists
    enemies.clear()
    projectiles.clear()
    experience_gems.clear()
    
    # Reset game statistics
    elapsed_time = 0
    
    # Schedule the first enemy spawn
    clock.schedule_unique(spawn_enemy, 2.0)
    
    # Start background music if sound is enabled
    if sound_enabled:
        print("DEBUG: Sound is enabled. Attempting to play background music.")
        try:
            music.play("background_music") # Pygame Zero will try .ogg, .wav, .mp3
            music.set_volume(0.3)
            print("DEBUG: music.play('background_music') called. Volume set to 0.3.")
            # You can add a delayed check to see if music is actually busy
            # import pygame # Add this at the top if you use the check below
            # def check_music_status():
            #    if pygame.mixer.music.get_busy():
            #        print("DEBUG: Pygame reports music is playing.")
            #    else:
            #        print("DEBUG: Pygame reports music is NOT playing. Check file, path, format, and system audio settings.")
            # clock.schedule_unique(check_music_status, 0.2) # Check after 0.2 seconds
        except Exception as e: # More specific: except pygame.error as e: (requires pygame import)
            print(f"DEBUG: An error occurred trying to play music: {e}")
            print("DEBUG: Please ensure 'background_music.ogg' (recommended), '.wav', or '.mp3' exists in a 'music' folder relative to your main.py.")
    else:
        print("DEBUG: Sound is disabled in settings. Music will not be played.")

# Initialize player for the first time
player = Player((WIDTH , HEIGHT))


# --- DRAW FUNCTIONS ---
def draw_menu():
    """Draws the main menu screen."""
    screen.fill((10, 10, 30))  # Dark blue background
    screen.draw.text(
        "Cyber-Duck", center=(WIDTH / 2, HEIGHT / 2 - 150), fontsize=80, color="cyan"
    )
    screen.draw.text(
        "Data Survival", center=(WIDTH / 2, HEIGHT / 2 - 90), fontsize=50, color="yellow"
    )

    # Draw buttons
    screen.draw.filled_rect(play_button, (0, 100, 150))
    screen.draw.text("Play", center=play_button.center, fontsize=40, color="white")

    sound_text = "Sound: ON" if sound_enabled else "Sound: OFF"
    screen.draw.filled_rect(sound_button, (0, 100, 150))
    screen.draw.text(sound_text, center=sound_button.center, fontsize=40, color="white")

    screen.draw.filled_rect(exit_button, (150, 0, 0))
    screen.draw.text("Exit", center=exit_button.center, fontsize=40, color="white")

def draw_playing():
    """Draws all elements during the gameplay state."""
    screen.fill((20, 20, 40))  # Darker blue background for gameplay

    # Draw all game objects
    player.draw()
    for gem in experience_gems:
        gem.draw()
    for enemy in enemies:
        enemy.draw()
    for projectile in projectiles:
        projectile.draw()

    # Draw the experience bar
    xp_bar_width = (player.experience / player.xp_to_next_level) * WIDTH if player.xp_to_next_level > 0 else 0
    screen.draw.filled_rect(Rect((0, HEIGHT - 20), (WIDTH, 20)), (10, 10, 30))
    screen.draw.filled_rect(Rect((0, HEIGHT - 20), (xp_bar_width, 20)), (100, 200, 255))
    screen.draw.text(f"Level: {player.level}", (10, HEIGHT - 22), fontsize=20, color="white")

    # Draw elapsed time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    screen.draw.text(f"Time: {minutes:02d}:{seconds:02d}", topright=(WIDTH - 10, 10), fontsize=30, color="white")

    # Draw player health (hearts)
    health_per_heart = player.max_health / NUM_HEART_CONTAINERS
    heart_x_start = 10
    heart_y = 10

    for i in range(NUM_HEART_CONTAINERS):
        current_heart_x = heart_x_start + i * (HEART_IMAGE_WIDTH + HEART_SPACING)
        # If player's health is greater than the health represented by previous hearts,
        # this heart is at least partially full (we draw it as full).
        if player.health > i * health_per_heart:
            screen.blit("heart_full.png", (current_heart_x, heart_y))
        else:
            screen.blit("heart_empty.png", (current_heart_x, heart_y))



def draw_game_over():
    """Draws the game over screen with final stats."""
    screen.fill((30, 10, 10))  # Dark red background
    screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2 - 100), fontsize=90, color="red")
    
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    # Display final stats
    screen.draw.text(f"Time Survived: {minutes:02d}:{seconds:02d}", center=(WIDTH / 2, HEIGHT / 2), fontsize=40, color="white")
    screen.draw.text(f"Enemies Defeated: {player.enemies_killed}", center=(WIDTH / 2, HEIGHT / 2 + 50), fontsize=40, color="white")
    screen.draw.text(f"Final Level: {player.level}", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=40, color="white")
    screen.draw.text("Click to return to menu", center=(WIDTH / 2, HEIGHT - 50), fontsize=30, color="yellow")


# --- MAIN DRAW HOOK ---
def draw():
    """PgZero draw hook, called every frame."""
    screen.clear()
    if game_state == GameState.MENU:
        draw_menu()
    elif game_state == GameState.PLAYING:
        draw_playing()
    elif game_state == GameState.GAME_OVER:
        draw_game_over()


# --- UPDATE FUNCTIONS ---
def update_playing(dt):
    """Main logic update when the game is in the 'PLAYING' state."""
    global elapsed_time, game_state
    
    elapsed_time += dt
    player.update(dt, WIDTH, HEIGHT)

    # Update enemies and handle collisions
    for e in enemies[:]:
        e.update(player.actor.pos)
        # Check for collision with the player
        if e.actor.colliderect(player.actor):
            player.take_damage(e.damage) # Player takes damage from the enemy
            if sound_enabled: sounds.hit.play() # Play hit sound
            
            # Remove the enemy that hit the player to prevent multiple hits from the same enemy instance
            enemies.remove(e) 

            if player.health <= 0:
                game_state = GameState.GAME_OVER
                music.stop()
                # Player defeated sound could be added here if different from generic hit
                return # Stop processing further logic in this frame if game is over
    # Update projectiles and check for hits
    for p in projectiles[:]:
        p.update()
        # Remove projectile if it goes off-screen
        if not p.actor.colliderect(Rect(0, 0, WIDTH, HEIGHT)):
            projectiles.remove(p)
            continue
        
        # Check for projectile hitting an enemy
        for e in enemies[:]:
            if e.actor.colliderect(p.actor):
                enemies.remove(e)
                if p in projectiles: projectiles.remove(p)
                experience_gems.append(ExperienceGem(e.actor.pos))
                player.enemies_killed += 1
                if sound_enabled: sounds.hit.play()
                break

    # Update experience gems and check for collection
    for gem in experience_gems[:]:
        if player.actor.colliderect(gem.actor):
            experience_gems.remove(gem)
            was_level_up = player.add_experience(10) # Now returns True if level up occurred
            if sound_enabled: sounds.collect.play()
            if was_level_up and sound_enabled:
                sounds.level_up.play()

# --- MAIN UPDATE HOOK ---
def update(dt):
    """PgZero update hook, called every frame."""
    if game_state == GameState.PLAYING:
        update_playing(dt)

# --- EVENT HOOKS ---
def on_mouse_down(pos, button):
    """PgZero mouse down event hook."""
    global game_state, sound_enabled
    
    if game_state == GameState.MENU:
        if play_button.collidepoint(pos):
            game_state = GameState.PLAYING
            reset_game()
        elif sound_button.collidepoint(pos):
            sound_enabled = not sound_enabled
            if not sound_enabled:
                music.stop()
        elif exit_button.collidepoint(pos):
            exit()

    elif game_state == GameState.PLAYING:
        if button == mouse.LEFT:
            projectiles.append(Projectile(player.actor.pos, pos))
            if sound_enabled: sounds.shoot.play()
            
    elif game_state == GameState.GAME_OVER:
        game_state = GameState.MENU

# --- HELPER CLASSES AND FUNCTIONS ---
class Projectile:
    """Represents a projectile fired by the player."""
    def __init__(self, start_pos, target_pos):
        self.actor = Actor("projectile.png", pos=start_pos)
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        angle_rad = math.atan2(dy, dx)
        self.speed = 8
        self.vx = math.cos(angle_rad) * self.speed
        self.vy = math.sin(angle_rad) * self.speed
        self.actor.angle = math.degrees(-angle_rad) + 90

    def update(self):
        self.actor.x += self.vx
        self.actor.y += self.vy

    def draw(self):
        self.actor.draw()

class ExperienceGem:
    """Represents an experience gem dropped by an enemy."""
    def __init__(self, pos):
        self.actor = Actor("gem.png", pos=pos)

    def draw(self): # screen parameter is unused by Actor.draw()
        self.actor.draw()

def spawn_enemy():
    """Spawns a new enemy at a random position off-screen."""
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top': pos = (random.randint(0, WIDTH), -30)
    elif side == 'bottom': pos = (random.randint(0, WIDTH), HEIGHT + 30)
    elif side == 'left': pos = (-30, random.randint(0, HEIGHT))
    else: pos = (WIDTH + 30, random.randint(0, HEIGHT))
    
    enemies.append(Enemy(pos))
    # Schedule the next enemy spawn
    clock.schedule_unique(spawn_enemy, max(0.5, 3.0 - elapsed_time * 0.05))

# --- START THE GAME ---
pgzrun.go()