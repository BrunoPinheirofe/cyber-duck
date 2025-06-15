
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
    LEVEL_UP_CHOICE = 3 # Novo estado para a tela de escolha de upgrade

# --- INITIAL SETUP ---
game_state = GameState.MENU
sound_enabled = True
elapsed_time = 0
# level_up_display_timer = 0.0  # Timer para exibir a mensagem de level up (será substituído pela tela de escolha)
# A mensagem "LEVEL UP!" será parte da tela de escolha.
LEVEL_UP_MESSAGE_DURATION = 2.0 # Duração que a mensagem fica na tela (em segundos)

# --- HEALTH DISPLAY CONFIGURATION ---
NUM_HEART_CONTAINERS = 5
HEART_IMAGE_WIDTH = 16  # Assuming heart images are 16px wide. Adjust if different.
HEART_SPACING = 4       # Spacing between hearts.

# --- GAME OBJECT LISTS ---
enemies = []
projectiles = []
experience_gems = []


# --- LEVEL UP CHOICE SCREEN ---
level_up_options = [] # Lista para armazenar as descrições e funções das opções de upgrade
option_buttons = []   # Lista para armazenar os Rects dos botões de opção

# --- UI COLOR CONSTANTS ---
BUTTON_DEFAULT_COLOR = (0, 70, 130)    # Darker blue for default button state
BUTTON_HOVER_COLOR = (0, 100, 180)     # Brighter blue for button hover state
BUTTON_TEXT_COLOR = (255, 255, 255)  # White for button text

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
    player.gems_collected_for_heal = 0 # Resetar contador de gemas para cura
    # Limpar opções de level up anteriores, se houver
    level_up_options.clear()
    option_buttons.clear()
    
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
player = Player((WIDTH / 2, HEIGHT / 2)) # Corrigido para centro da tela


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
    if player.orbital_weapon_active: # Desenhar a arma orbital
        player.draw_orbital_weapon()
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

def draw_level_up_choice():
    screen.fill((25, 25, 60)) # Fundo azul escuro para a tela de escolha
    screen.draw.text(
        f"LEVEL UP! (Nível {player.level})",
        center=(WIDTH / 2, HEIGHT / 4 - 30),
        fontsize=60,
        color="yellow",
        ocolor="black",
        owidth=1.5
    )
    screen.draw.text(
        "Escolha uma Melhoria:",
        center=(WIDTH / 2, HEIGHT / 4 + 30),
        fontsize=40,
        color="white"
    )

    for i, option in enumerate(level_up_options):
        button_rect = option_buttons[i]
        color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse.get_pos()) else BUTTON_DEFAULT_COLOR
        screen.draw.filled_rect(button_rect, color)
        screen.draw.textbox( # Usar textbox para quebra de linha automática
            option["text"],
            button_rect.inflate(-20, -20), # Reduz um pouco para margem interna
            fontsize=28,
            color=BUTTON_TEXT_COLOR,
            align="center"
        )

# --- MAIN DRAW HOOK ---
def draw():
    """PgZero draw hook, called every frame."""
    screen.clear()
    if game_state == GameState.MENU:
        draw_menu()
    elif game_state == GameState.PLAYING: # Apenas desenha o jogo se estiver JOGANDO
        draw_playing()
    elif game_state == GameState.GAME_OVER:
        draw_game_over()
    elif game_state == GameState.LEVEL_UP_CHOICE:
        draw_level_up_choice()


# --- UPDATE FUNCTIONS ---
def update_playing(dt):
    """Main logic update when the game is in the 'PLAYING' state."""
    global elapsed_time, game_state # level_up_display_timer foi removido da lista global pois não é mais usado aqui

    elapsed_time += dt
    player.update(dt, WIDTH, HEIGHT)

    # Update enemies and handle collisions
    for e in enemies[:]:
        e.update(player.actor.pos)
        # Check for collision with the player
        if e.actor.colliderect(player.actor):
            player.take_damage(e.damage_output) # Player takes damage from the enemy
            if sound_enabled: sounds.hit.play() # Play hit sound
            
            # Inimigo que colidiu é removido (ou poderia recuar/ficar invulnerável por um tempo)
            enemies.remove(e) 

            if player.health <= 0:
                game_state = GameState.GAME_OVER
                music.stop()
                # Player defeated sound could be added here if different from generic hit
                return # Stop processing further logic in this frame if game is over
            continue # Pula para o próximo inimigo para evitar erros com a lista modificada

        # Check for collision with orbital weapon
        if player.orbital_weapon_active and player.orbital_actor.colliderect(e.actor):
            # Aplicar dano ao inimigo. Pode-se adicionar um cooldown aqui para evitar dano contínuo.
            # Por simplicidade, vamos aplicar dano e se o inimigo morrer, ele é removido.
            if e.take_damage(player.orbital_damage): # Se o inimigo foi derrotado
                if e in enemies: enemies.remove(e)
                experience_gems.append(ExperienceGem(e.actor.pos))
                player.enemies_killed += 1
                if sound_enabled: sounds.hit.play() # Som de acerto (pode ser diferente)
            # Para um efeito de "empurrão" ou dano por segundo, a lógica seria mais complexa.
            # Por agora, o orbital causa dano ao tocar.

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
                if p in projectiles: projectiles.remove(p)
                
                if e.take_damage(p.damage): # Se o inimigo foi derrotado pelo projétil
                    if e in enemies: enemies.remove(e)
                    experience_gems.append(ExperienceGem(e.actor.pos))
                    player.enemies_killed += 1
                if sound_enabled: sounds.hit.play() # Som de acerto
                break

    # Update experience gems and check for collection
    for gem in experience_gems[:]:
        if player.actor.colliderect(gem.actor):
            experience_gems.remove(gem)
            was_level_up = player.process_gem_collection(xp_from_gem=10) # Usa o novo método
            if sound_enabled: sounds.collect.play()
            if was_level_up:
                if sound_enabled:
                    sounds.level_up.play()
                prepare_level_up_choices()
                game_state = GameState.LEVEL_UP_CHOICE

# --- MAIN UPDATE HOOK ---
def update(dt):
    """PgZero update hook, called every frame."""
    if game_state == GameState.PLAYING:
        update_playing(dt)

# --- LEVEL UP CHOICE LOGIC ---
def prepare_level_up_choices():
    """Prepara uma lista de 2 opções de upgrade para o jogador."""
    global level_up_options, option_buttons
    level_up_options.clear()
    option_buttons.clear()

    all_possible_upgrades = [
        {"id": "proj_dmg", "text": "Aumentar Dano do Projétil (+5)", "apply": lambda p: p.increase_projectile_damage(5)},
        {"id": "player_speed", "text": "Aumentar Velocidade de Movimento (+0.3)", "apply": lambda p: p.increase_movement_speed(0.3)},
        {"id": "max_hp", "text": "Aumentar Vida Máxima (+10)", "apply": lambda p: p.increase_max_health(10)},
    ]

    if player.orbital_weapon_active:
        all_possible_upgrades.append(
            {"id": "orb_dmg", "text": "Aumentar Dano da Lâmina Orbital (+5)", "apply": lambda p: p.increase_orbital_damage(5)}
        )
        all_possible_upgrades.append(
            {"id": "orb_speed", "text": "Aumentar Velocidade da Lâmina Orbital (+0.5)", "apply": lambda p: p.increase_orbital_rotation_speed(0.5)}
        )
    elif player.level >= 2: # Oferecer ativação da arma orbital a partir do nível 2 se ainda não a tiver
        # Garante que esta opção não seja oferecida se já tiver a arma
        # (a condição `player.orbital_weapon_active` acima já cuida disso, mas é bom ser explícito)
        if not any(upg['id'] == "activate_orbital" for upg in all_possible_upgrades):
             all_possible_upgrades.append(
                {"id": "activate_orbital", "text": "Desbloquear Lâmina Orbital", "apply": lambda p: p.activate_orbital_weapon()}
            )

    # Embaralha e seleciona até 2 opções distintas
    random.shuffle(all_possible_upgrades)
    
    # Tenta pegar 2 opções, mas pega menos se não houver suficientes
    num_options_to_present = min(2, len(all_possible_upgrades))
    chosen_upgrades = all_possible_upgrades[:num_options_to_present]

    level_up_options.extend(chosen_upgrades)

    # Define os retângulos dos botões
    button_width = 400
    button_height = 80
    spacing = 30
    start_y = HEIGHT / 2 - ( (button_height * num_options_to_present + spacing * (num_options_to_present -1) ) / 2 ) + 50

    for i, option in enumerate(level_up_options):
        button_y = start_y + i * (button_height + spacing)
        option_buttons.append(Rect(WIDTH / 2 - button_width / 2, button_y, button_width, button_height))

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
            # Usar o dano base do projétil do jogador
            projectiles.append(Projectile(player.actor.pos, pos, player.projectile_base_damage))
            if sound_enabled: sounds.shoot.play()
            
    elif game_state == GameState.GAME_OVER:
        game_state = GameState.MENU

    elif game_state == GameState.LEVEL_UP_CHOICE:
        for i, btn_rect in enumerate(option_buttons):
            if btn_rect.collidepoint(pos) and button == mouse.LEFT:
                chosen_option = level_up_options[i]
                chosen_option["apply"](player) # Aplica a melhoria ao jogador
                print(f"Jogador escolheu: {chosen_option['text']}")
                
                game_state = GameState.PLAYING # Volta ao jogo
                # Limpar opções para a próxima vez
                level_up_options.clear()
                option_buttons.clear()
                break # Sai do loop após encontrar o botão clicado

# --- HELPER CLASSES AND FUNCTIONS ---
class Projectile:
    """Represents a projectile fired by the player."""
    def __init__(self, start_pos, target_pos, damage_value): # Adicionado damage_value
        self.actor = Actor("projectile.png", pos=start_pos)
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        angle_rad = math.atan2(dy, dx)
        self.speed = 8
        self.damage = damage_value # Usa o valor de dano passado
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