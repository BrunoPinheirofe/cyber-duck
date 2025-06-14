# main.py

import pgzrun
import math
import random

# --- CONFIGURAÇÕES DA JANELA ---
WIDTH = 800
HEIGHT = 600
TITLE = "Cyber-Pato: Sobrevivência de Dados"

# --- ESTADO DO JOGO ---
# Esta variável controlará se estamos jogando, no menu, ou em level up.
game_state = "playing"

# --- LISTAS DE OBJETOS ---
enemies = []
projectiles = []
experience_gems = [] # Nova lista para os gems de XP

# --- CLASSE DO JOGADOR (Player) ---
class Player:
    def __init__(self, image_file, pos):
        self.actor = Actor(image_file, pos=pos)
        self.speed = 3
        # Novos atributos para o sistema de XP e Nível
        self.level = 1
        self.experience = 0
        self.xp_to_next_level = 5 # Começa precisando de 5 XP para o primeiro nível

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
            dx *= 0.707
            dy *= 0.707
        self.actor.x += dx * self.speed
        self.actor.y += dy * self.speed
    
    def check_boundaries(self):
        if self.actor.left < 0: self.actor.left = 0
        if self.actor.right > WIDTH: self.actor.right = WIDTH
        if self.actor.top < 0: self.actor.top = 0
        if self.actor.bottom > HEIGHT: self.actor.bottom = HEIGHT
        
    def add_experience(self, amount):
        self.experience += amount
        print(f"XP: {self.experience} / {self.xp_to_next_level}") # Mostra o progresso no console

    def check_level_up(self):
        global game_state
        if self.experience >= self.xp_to_next_level:
            self.level += 1
            self.experience -= self.xp_to_next_level
            # Aumenta a dificuldade para o próximo nível
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            print(f"LEVEL UP! Novo Nível: {self.level}")
            game_state = "level_up" # Pausa o jogo e entra no estado de level up

# --- CLASSE DO PROJÉTIL ---
class Projectile:
    def __init__(self, image_file, pos, target_pos):
        self.actor = Actor(image_file, pos=pos)
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        self.angle_rad = math.atan2(dy, dx)
        self.speed = 8

    def update(self):
        self.actor.x += math.cos(self.angle_rad) * self.speed
        self.actor.y += math.sin(self.angle_rad) * self.speed

    def draw(self):
        self.actor.draw()

# --- CLASSE DO INIMIGO (Enemy) ---
class Enemy:
    def __init__(self, image_file, speed):
        start_pos = self.get_random_spawn_pos()
        self.actor = Actor(image_file, pos=start_pos)
        self.speed = speed

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
        if side == 'top': return (random.randint(0, WIDTH), -30)
        if side == 'bottom': return (random.randint(0, WIDTH), HEIGHT + 30)
        if side == 'left': return (-30, random.randint(0, HEIGHT))
        if side == 'right': return (WIDTH + 30, random.randint(0, HEIGHT))

# --- NOVA CLASSE DO GEM DE EXPERIÊNCIA ---
class ExperienceGem:
    def __init__(self, pos):
        self.actor = Actor('gem.png', pos=pos)

    def draw(self):
        self.actor.draw()

# --- FUNÇÕES AUXILIARES ---
def spawn_enemy():
    new_enemy = Enemy('wolf.png', speed=random.uniform(1.0, 2.0))
    enemies.append(new_enemy)

def shoot_projectile(mouse_pos):
    new_projectile = Projectile('bullet.png', player.actor.pos, mouse_pos)
    projectiles.append(new_projectile)

# --- INICIALIZAÇÃO DO JOGO ---
player = Player('pato_placeholder.png', pos=(WIDTH / 2, HEIGHT / 2))
clock.schedule_interval(spawn_enemy, 2.0)

# --- FUNÇÕES PRINCIPAIS DO PGZERO ---
# Bloco de código corrigido para a função on_mouse_down

def on_mouse_down(pos, button):
    # A declaração 'global' agora está no início da função
    global game_state

    if game_state == "playing" and button == mouse.LEFT:
        shoot_projectile(pos)
    # Se estamos na tela de level up, qualquer clique nos retorna ao jogo
    elif game_state == "level_up":
        game_state = "playing"

def draw():
    screen.fill((20, 20, 40))
    player.draw()
    for gem in experience_gems:
        gem.draw()
    for enemy in enemies:
        enemy.draw()
    for projectile in projectiles:
        projectile.draw()
        
    # Desenha a barra de XP na parte inferior da tela
    xp_bar_width = (player.experience / player.xp_to_next_level) * WIDTH
    screen.draw.filled_rect(Rect((0, HEIGHT - 10), (xp_bar_width, 10)), (100, 200, 255))
    
    # Se o jogo está em modo "level up", desenha a tela de pausa
    if game_state == "level_up":
        draw_level_up_screen()

def draw_level_up_screen():
    # Desenha um retângulo semi-transparente sobre o jogo
    # (Exceção: pgzero não suporta transparência fácil, então usamos um retângulo sólido)
    screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (20, 20, 40, 150))
    # Mostra a mensagem de Level Up
    screen.draw.text(
        "LEVEL UP!",
        center=(WIDTH / 2, HEIGHT / 2 - 50),
        fontsize=60,
        color="yellow"
    )
    screen.draw.text(
        "Clique para continuar",
        center=(WIDTH / 2, HEIGHT / 2 + 50),
        fontsize=40,
        color="white"
    )

def update(dt):
    # Se o jogo não estiver no estado "playing", pulamos toda a lógica de atualização
    if game_state != "playing":
        return

    player.update()
    
    # --- Lógica de Colisão e Atualizações ---
    # Coleta de XP
    surviving_gems = []
    for gem in experience_gems:
        if player.actor.colliderect(gem.actor):
            player.add_experience(1) # Cada gem vale 1 de XP
        else:
            surviving_gems.append(gem)
    experience_gems[:] = surviving_gems
    
    # Atualização de Projéteis
    surviving_projectiles = []
    for p in projectiles:
        p.update()
        if p.actor.right > 0 and p.actor.left < WIDTH and p.actor.top < HEIGHT and p.actor.bottom > 0:
            surviving_projectiles.append(p)
    projectiles[:] = surviving_projectiles
    
    # Atualização de Inimigos e Colisão
    surviving_enemies = []
    for e in enemies:
        e.update(player.actor.pos)
        
        hit_by_projectile = False
        for p in projectiles:
            if e.actor.colliderect(p.actor):
                hit_by_projectile = True
                if p in projectiles:
                    projectiles.remove(p)
                # NOVO: Dropar um gem de XP na posição do inimigo
                experience_gems.append(ExperienceGem(e.actor.pos))
                break
        
        if not hit_by_projectile:
            surviving_enemies.append(e)
            
    enemies[:] = surviving_enemies

# Inicia o jogo
pgzrun.go()