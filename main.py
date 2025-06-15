# main.py

import pgzrun
import math
import random
from Player import Player
from Enemy import Enemy
# --- CONFIGURAÇÕES DA JANELA ---
WIDTH = 800
HEIGHT = 600
TITLE = "Cyber-Pato: Sobrevivência de Dados"

# --- ESTADO DO JOGO ---
# Esta variável controlará se estamos jogando, no menu, ou em level up.
class GameState:
    MENU = 0
    PLAYING = 1
    LEVEL_UP = 2


game_state = GameState.MENU
sound_enabled = True
music_enabled = True

# --- LISTAS DE OBJETOS ---
enemies = []
projectiles = []
experience_gems = []


def draw_menu():
    screen.clear()
    screen.draw.text(
        "Cyber-Pato: Sobrevivência de Dados",
        center=(WIDTH / 2, HEIGHT / 2 - 50),
        fontsize=60,
        color="white",
    )

    botoes = [
        ("Jogar", (WIDTH / 2, HEIGHT / 2 + 100)),
        ("Configurações", (WIDTH / 2, HEIGHT / 2 + 150)),
        ("Sair", (WIDTH / 2, HEIGHT / 2 + 200)),
    ]

    for i, (texto, pos) in enumerate(botoes):
        box = Rect(pos, (WIDTH / 2, 50))
        color = (20, 20, 40) if i != 0 else (20, 20, 40, 150)
        screen.draw.filled_rect(box, color)
        screen.draw.text(texto, center=box.center, color="white", fontsize=40)


def draw_settings():
    screen.clear()
    screen.draw.text(
        "Configurações", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=60, color="white"
    )

    botoes = [
        ("Voltar", (WIDTH / 2, HEIGHT / 2 + 100)),
        ("Música", (WIDTH / 2, HEIGHT / 2 + 150)),
        ("Efeitos Sonoros", (WIDTH / 2, HEIGHT / 2 + 200)),
    ]

    for i, (texto, pos) in enumerate(botoes):
        box = Rect(pos, (WIDTH / 2, 50))
        color = (20, 20, 40) if i != 0 else (20, 20, 40, 150)
        screen.draw.filled_rect(box, color)
        screen.draw.text(texto, center=box.center, color="white", fontsize=40)


def draw_game_over():
    screen.fill((20, 20, 40))
    min = int(elapsed_time // 60)
    sec = int(elapsed_time % 60)
    sco
    screen.draw.text(
        "Game Over", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=60, color="red"
    )

    stats = [
        ("Inimigos derrotados", {player.enemies_killed}),
        ("Tempo de jogo", f"{min:02}:{sec:02}"),
        ("Experiência coletada", player.experience),
        ("Nível alcançado", player.level),
    ]


# --- CLASSE DO PROJÉTIL ---
class Projectile:
    def __init__(self, imagem, pos, target_pos):
        self.actor = Actor(imagem, pos=pos)
        dx = target_pos[0] - pos[0]
        dy = target_pos[1] - pos[1]
        self.angle_rad = math.atan2(dy, dx)
        self.speed = 8

    def update(self):
        self.actor.x += math.cos(self.angle_rad) * self.speed
        self.actor.y += math.sin(self.angle_rad) * self.speed

    def draw(self):
        self.actor.draw()


# --- NOVA CLASSE DO GEM DE EXPERIÊNCIA ---
class ExperienceGem:
    def __init__(self, pos):
        self.actor = Actor("gem.png", pos=pos)

    def draw(self):
        self.actor.draw()


# --- FUNÇÕES AUXILIARES ---
def spawn_enemy():
    new_enemy = Enemy(pos=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    enemies.append(new_enemy)


def shoot_projectile(mouse_pos):
    new_projectile = Projectile("bullet.png", player.actor.pos, mouse_pos)
    projectiles.append(new_projectile)


# --- INICIALIZAÇÃO DO JOGO ---
player = Player(pos=(WIDTH / 2, HEIGHT / 2))
clock.schedule_interval(spawn_enemy, 2.0)


def on_mouse_down(pos, button):
    # A declaração 'global' agora está no início da função
    global game_state

    if game_state == "playing" and button == mouse.LEFT:
        shoot_projectile(pos)
    # Se estamos na tela de level up, qualquer clique nos retorna ao jogo
    elif game_state == "level_up":
        game_state = "playing"


def draw():
    screen.clear()

    if game_state == GameState.MENU:
        draw_menu()
    elif game_state == GameState.PLAYING:
        draw_playing()
    elif game_state == GameState.LEVEL_UP:
        draw_level_up_screen()

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

    screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (20, 20, 40, 150))
    # Mostra a mensagem de Level Up
    screen.draw.text(
        "LEVEL UP!", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=60, color="yellow"
    )
    screen.draw.text(
        "Clique para continuar",
        center=(WIDTH / 2, HEIGHT / 2 + 50),
        fontsize=40,
        color="white",
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
            player.add_experience(1)  # Cada gem vale 1 de XP
        else:
            surviving_gems.append(gem)
    experience_gems[:] = surviving_gems

    # Atualização de Projéteis
    surviving_projectiles = []
    for p in projectiles:
        p.update()
        if (
            p.actor.right > 0
            and p.actor.left < WIDTH
            and p.actor.top < HEIGHT
            and p.actor.bottom > 0
        ):
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
