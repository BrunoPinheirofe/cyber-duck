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
        self.projectile_base_damage = 25 # Dano base do projétil principal
        self.enemies_killed = 0  # Contador de inimigos derrotados

        # Atributos para recuperação de vida com gemas
        self.gems_collected_for_heal = 0
        self.gems_needed_for_hp_point = 20 # Coletar 20 gemas para recuperar 1 HP

        # animations
        self.idle_frames = ["duck-idle1.png", "duck-idle2.png"]
        self.walk_left_frames = ["duck-walk-left1.png", "duck-walk-left2.png"]
        self.walk_right_frames = ["duck-walk-right1.png", "duck-walk-right2.png"]

        self.animation_timer = 0.0
        self.animation_speed = 0.2  # Tempo entre as animações
        self.current_frame = 0
        self.is_moving = False
        self.face_right = True

        # Atributos da Arma Orbital
        self.orbital_weapon_active = False # Começa desativada
        self.orbital_actor = None          # Ator da arma orbital, inicializado como None
        self.orbital_distance = 40         # Distância do jogador
        self.orbital_angle = 0             # Ângulo inicial
        self.orbital_rotation_speed = 2.5  # Radianos por segundo
        self.orbital_damage = 15           # Dano da arma orbital

    def activate_orbital_weapon(self):
        """Ativa e inicializa a arma orbital."""
        if not self.orbital_weapon_active: # Ativa somente se não estiver ativa
            self.orbital_weapon_active = True
            self.orbital_actor = Actor("orbital_blade.png") # Cria o ator da arma
            # Garante que a posição inicial da arma orbital seja definida corretamente
            self.update_orbital_weapon(0) # Chama com dt=0 para definir a posição inicial
            print("Arma Orbital Ativada!") # Feedback no console

    def update(self, dt, screen_width=800, screen_height=600):
        self.handle_input()
        self.check_boundaries(screen_width, screen_height)
        self.animate(dt)
        if self.orbital_weapon_active and self.orbital_actor:
            self.update_orbital_weapon(dt)

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
            # Corrected: Use idle_frames when player is not moving.
            active_frames = self.idle_frames

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
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            print(f"LEVEL UP! Novo Nível: {self.level}")
            leveled_up_this_call = True
        
        # Lógica de cura por gemas (cada gema coletada contribui)
        # Assumindo que 'amount' de XP vem de uma gema. Se não, ajuste.
        # Se cada gema dá 10 XP, e queremos 1 HP a cada 20 gemas, então a cada 200 XP de gemas.
        # Simplificando: vamos contar gemas diretamente.
        # Esta função é chamada com XP, não com contagem de gemas.
        # Vamos adicionar um método separado para processar gemas.
        return leveled_up_this_call

    def process_gem_collection(self, xp_from_gem=10):
        """Chamado quando uma gema é coletada."""
        leveled_up = self.add_experience(xp_from_gem)
        self.gems_collected_for_heal += 1
        if self.gems_collected_for_heal >= self.gems_needed_for_hp_point:
            self.heal(1) # Recupera 1 ponto de vida
            self.gems_collected_for_heal = 0 # Reseta o contador
        return leveled_up

    def take_damage(self, amount):
        if self.health > 0:  # Only take damage if alive
            self.health -= amount
            self.health = max(0, self.health)  # Clamp health at 0
        # Game over check will be handled in main.py based on self.health

    # def check_level_up(self): # This method is now redundant

    def heal(self, amount):
        self.health += amount
        self.health = min(self.health, self.max_health) # Não ultrapassar a vida máxima
        print(f"Player healed by {amount}. Current health: {self.health}")

    def update_orbital_weapon(self, dt):
        if not self.orbital_weapon_active or not self.orbital_actor:
            return

        self.orbital_angle += self.orbital_rotation_speed * dt
        self.orbital_angle %= (2 * math.pi)
        
        offset_x = math.cos(self.orbital_angle) * self.orbital_distance
        offset_y = math.sin(self.orbital_angle) * self.orbital_distance
        self.orbital_actor.pos = (self.actor.x + offset_x, self.actor.y + offset_y)
        self.orbital_actor.angle = math.degrees(-self.orbital_angle) # Opcional: para girar o sprite

    def draw_orbital_weapon(self):
        if self.orbital_weapon_active and self.orbital_actor:
            self.orbital_actor.draw()

    # --- MÉTODOS DE UPGRADE ---
    def increase_projectile_damage(self, amount):
        self.projectile_base_damage += amount
        print(f"Dano do Projétil aumentado para: {self.projectile_base_damage}")

    def increase_movement_speed(self, amount):
        self.speed += amount
        print(f"Velocidade do Jogador aumentada para: {self.speed}")

    def increase_max_health(self, amount):
        self.max_health += amount
        self.health += amount # Cura o jogador pela quantidade aumentada também
        self.health = min(self.health, self.max_health) # Garante que não ultrapasse o máximo
        print(f"Vida Máxima aumentada para: {self.max_health}. Vida Atual: {self.health}")

    def increase_orbital_damage(self, amount):
        if self.orbital_weapon_active:
            self.orbital_damage += amount
            print(f"Dano da Arma Orbital aumentado para: {self.orbital_damage}")

    def increase_orbital_rotation_speed(self, amount):
        if self.orbital_weapon_active:
            self.orbital_rotation_speed += amount
            print(f"Velocidade de Rotação da Arma Orbital aumentada para: {self.orbital_rotation_speed}")

    # O método activate_orbital_weapon() já existe e será usado como uma opção de upgrade.
