import pgzrun
import math
import random
from pygame.rect import Rect
from Player import Player # Nome importado, mantido
from Enemy import Wolf, Bat # Nomes importados, mantidos
from Itens import get_upgrade_options # Nome importado, mantido

# --- CONFIGURAÇÃO DA JANELA DO JOGO ---
WIDTH = 1200
HEIGHT =  800
TITLE = "Cyber-Duck" # Título do jogo, mantido


class EstadoJogo:
    MENU = 0
    JOGANDO = 1
    FIM_DE_JOGO = 2
    ESCOLHA_MELHORIA = 3


# --- CONFIGURAÇÃO INICIAL ---
estado_jogo = EstadoJogo.MENU
som_ligado = True
tempo_decorrido = 0

# --- CONFIGURAÇÃO DA INTERFACE DO USUÁRIO (UI) ---
NUM_CORACOES_VIDA = 5
WIDTH_IMAGEM_CORACAO = 16 # Largura da imagem do coração
ESPACAMENTO_CORACAO = 4

COR_BOTAO_PADRAO = (0, 70, 130)
COR_BOTAO_CURSOR = (0, 100, 180) # Cor quando o cursor está sobre (ou para botões de escolha)
COR_TEXTO_BOTAO = (255, 255, 255)

# --- BOTÕES DO MENU ---
botao_jogar = Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50)
botao_som = Rect(WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50)
botao_sair = Rect(WIDTH / 2 - 100, HEIGHT / 2 + 140, 200, 50)

# --- OBJETOS DO JOGO ---
inimigos = []
projeteis = []
gemas_experiencia = []
opcoes_melhoria = [] # Anteriormente level_up_options
botoes_opcao = []


# --- CONFIGURAÇÃO DO JOGADOR ---
jogador = Player((WIDTH / 2, HEIGHT / 2)) # 'Player' é o nome da classe importada


# --- FUNÇÃO PARA REINICIAR O JOGO ---
def reiniciar_jogo():
    """Reinicia todas as variáveis do jogo para o estado inicial."""
    global jogador, inimigos, projeteis, gemas_experiencia, tempo_decorrido, estado_jogo

    jogador = Player((WIDTH / 2, HEIGHT / 2))

    # Limpa todas as listas de objetos do jogo
    inimigos.clear()
    projeteis.clear()
    gemas_experiencia.clear()
    opcoes_melhoria.clear()
    botoes_opcao.clear()

    tempo_decorrido = 0

    clock.schedule_unique(gerar_inimigo, 2.0) # 'gerar_inimigo' é a função traduzida

    if som_ligado:
        try:
            music.play("background_music") 
            music.set_volume(0.5)  # Ajusta o volume da música de fundo
        except Exception as e:
            print(f"Erro ao tocar música de fundo: {e}")
    else:
        music.set_volume(0)
        
        
def desenhar_menu():
    """Desenha a tela do menu principal."""
    screen.fill((10, 10, 30)) # 'screen' é um objeto global do Pygame Zero
    screen.draw.text("Cyber-Duck", center=(WIDTH / 2, HEIGHT / 2 - 150), fontsize=80, color="cyan")
    screen.draw.text("Data Survival", center=(WIDTH / 2, HEIGHT / 2 - 90), fontsize=50, color="yellow")

    screen.draw.filled_rect(botao_jogar, (0, 100, 150))
    screen.draw.text("Jogar", center=botao_jogar.center, fontsize=40, color="white")

    texto_som = "Sons: LIGADO" if som_ligado else "Sons: DESLIGADO"
    screen.draw.filled_rect(botao_som, (0, 100, 150))
    screen.draw.text(texto_som, center=botao_som.center, fontsize=40, color="white")

    screen.draw.filled_rect(botao_sair, (150, 0, 0))
    screen.draw.text("Sair", center=botao_sair.center, fontsize=40, color="white")

def desenhar_jogando():
    """Desenha todos os elementos para o estado principal de jogo."""
    screen.fill((20, 20, 40))

    jogador.draw()
    if jogador.orbital_weapon_active: # Assumindo que 'orbital_weapon_active' é um atributo da classe Player
        jogador.draw_orbital_weapon() # Assumindo que 'draw_orbital_weapon' é um método da classe Player
        
    for gema in gemas_experiencia: gema.draw()
    for inimigo_obj in inimigos: inimigo_obj.draw() # Renomeado 'enemy' para 'inimigo_obj' para evitar conflito com módulo Enemy
    for projetil_obj in projeteis: projetil_obj.draw() # Renomeado 'projectile' para 'projetil_obj'

    # --- ELEMENTOS DA UI ---
    # Barra de Experiência
    largura_barra_xp = (jogador.experience / jogador.xp_to_next_level) * WIDTH if jogador.xp_to_next_level > 0 else 0
    screen.draw.filled_rect(Rect((0, HEIGHT - 20), (WIDTH, 20)), (10, 10, 30))
    screen.draw.filled_rect(Rect((0, HEIGHT - 20), (largura_barra_xp, 20)), (100, 200, 255))
    screen.draw.text(f"Nível: {jogador.level}", (10, HEIGHT - 22), fontsize=20, color="white")

    # Tempo Decorrido
    minutos, segundos = divmod(int(tempo_decorrido), 60)
    screen.draw.text(f"Tempo: {minutos:02d}:{segundos:02d}", topright=(WIDTH - 10, 10), fontsize=30, color="white")

    # Vida do Jogador
    vida_por_coracao = jogador.max_health / NUM_CORACOES_VIDA
    for i in range(NUM_CORACOES_VIDA):
        pos_x_coracao = 10 + i * (WIDTH_IMAGEM_CORACAO + ESPACAMENTO_CORACAO)
        nome_imagem = "heart_full.png" if jogador.health > i * vida_por_coracao else "heart_empty.png" # Nomes dos arquivos de imagem mantidos
        screen.blit(nome_imagem, (pos_x_coracao, 10))

def desenhar_fim_de_jogo():
    """Desenha a tela de fim de jogo."""
    screen.fill((30, 10, 10))
    screen.draw.text("FIM DE JOGO", center=(WIDTH / 2, HEIGHT / 2 - 100), fontsize=90, color="red")
    
    minutos, segundos = divmod(int(tempo_decorrido), 60)
    screen.draw.text(f"Tempo Sobrevivido: {minutos:02d}:{segundos:02d}", center=(WIDTH / 2, HEIGHT / 2), fontsize=40, color="white")
    screen.draw.text(f"Inimigos Derrotados: {jogador.enemies_killed}", center=(WIDTH / 2, HEIGHT / 2 + 50), fontsize=40, color="white")
    screen.draw.text(f"Nível Final: {jogador.level}", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=40, color="white")
    screen.draw.text("Clique para voltar ao menu", center=(WIDTH / 2, HEIGHT - 50), fontsize=30, color="yellow")

def desenhar_escolha_melhoria():
    """Desenha a tela de escolha de melhoria ao subir de nível."""
    desenhar_jogando() # Desenha o estado de jogo pausado ao fundo
    # Sobreposição escura
    sobreposicao_escura = Rect(0, 0, WIDTH, HEIGHT)
    screen.draw.filled_rect(sobreposicao_escura, (0, 0, 0, 150))
    
    screen.draw.text(f"SUBIU DE NÍVEL! (Nível {jogador.level})", center=(WIDTH / 2, HEIGHT / 4 - 30), fontsize=60, color="yellow", ocolor="black", owidth=1.5)
    screen.draw.text("Escolha uma Melhoria:", center=(WIDTH / 2, HEIGHT / 4 + 30), fontsize=40, color="white")

    
    for i, opcao in enumerate(opcoes_melhoria):
        rect_botao = botoes_opcao[i]
        cor_botao_atual = COR_BOTAO_CURSOR # Usa a cor de cursor/hover para os botões de escolha
        screen.draw.filled_rect(rect_botao, cor_botao_atual)
        screen.draw.text(opcao.description, center=rect_botao.center, fontsize=30, color=COR_TEXTO_BOTAO) # 'opcao.description' vem do módulo Itens

def draw(): # Hook do Pygame Zero, nome mantido
    """Hook principal de desenho do PgZero."""
    screen.clear()
    if estado_jogo == EstadoJogo.MENU:
        desenhar_menu()
    elif estado_jogo == EstadoJogo.JOGANDO:
        desenhar_jogando()
    elif estado_jogo == EstadoJogo.FIM_DE_JOGO:
        # O som de fim de jogo é tocado apenas uma vez na transição de estado
        desenhar_fim_de_jogo()
    elif estado_jogo == EstadoJogo.ESCOLHA_MELHORIA:
        # Desenha o jogo pausado ao fundo, depois a UI de escolha por cima
        desenhar_jogando() 
        desenhar_escolha_melhoria()

# --- FUNÇÕES DE ATUALIZAÇÃO ---

def atualizar_jogando(dt):
    """Loop principal de atualização lógica para o estado 'JOGANDO'."""
    global tempo_decorrido, estado_jogo

    tempo_decorrido += dt
    jogador.update(dt, WIDTH, HEIGHT)

    # --- Lidar com Inimigos ---
    for inimigo_atual in inimigos[:]: # 'inimigo_atual' é uma instância de Enemy.Wolf ou Enemy.Bat
        inimigo_atual.update(dt, jogador.actor.pos)
        
        # Colisão com jogador
        if inimigo_atual.actor.colliderect(jogador.actor):
            jogador.take_damage(inimigo_atual.damage_output)
            if som_ligado: sounds.hit.play() 
            inimigos.remove(inimigo_atual)
            if jogador.health <= 0:
                estado_jogo = EstadoJogo.FIM_DE_JOGO
                if som_ligado: sounds.game_over.play()
                music.stop()
                return
            continue

        # Colisão com arma orbital
        if jogador.orbital_weapon_active and jogador.orbital_actor.colliderect(inimigo_atual.actor):
            if inimigo_atual.take_damage(jogador.orbital_damage): # True se o inimigo morreu
                if inimigo_atual in inimigos: inimigos.remove(inimigo_atual)
                gemas_experiencia.append(GemaExperiencia(inimigo_atual.actor.pos))
                jogador.enemies_killed += 1
            if som_ligado: sounds.hit.play()

    # --- Lidar com Projéteis ---
    for projetil_atual in projeteis[:]: # 'projetil_atual' é uma instância de Projetil
        projetil_atual.update()
        if not projetil_atual.actor.colliderect(Rect(0, 0, WIDTH, HEIGHT)):
            projeteis.remove(projetil_atual)
            continue
        
        for inimigo_atual in inimigos[:]:
            if inimigo_atual.actor.colliderect(projetil_atual.actor):
                if projetil_atual in projeteis: projeteis.remove(projetil_atual)
                if inimigo_atual.take_damage(projetil_atual.dano): # True se o inimigo morreu
                    if inimigo_atual in inimigos: inimigos.remove(inimigo_atual)
                    gemas_experiencia.append(GemaExperiencia(inimigo_atual.actor.pos))
                    jogador.enemies_killed += 1
                if som_ligado: sounds.hit.play()
                break

    # --- Lidar com Gemas de Experiência ---
    for gema_atual in gemas_experiencia[:]: # 'gema_atual' é uma instância de GemaExperiencia
        if jogador.actor.colliderect(gema_atual.actor):
            gemas_experiencia.remove(gema_atual)
            if som_ligado: sounds.collect.play() # 'collect' é nome do arquivo de som
            if jogador.process_gem_collection(): # True se subiu de nível
                if som_ligado: sounds.level_up.play() # 'level_up' é nome do arquivo de som
                preparar_escolhas_melhoria()
                estado_jogo = EstadoJogo.ESCOLHA_MELHORIA

def update(dt): # Hook do Pygame Zero, nome mantido
    """Hook principal de atualização do PgZero, chamado a cada frame."""
    if estado_jogo == EstadoJogo.JOGANDO:
        atualizar_jogando(dt)

# --- SUBIR DE NÍVEL & MECÂNICAS DO JOGO ---

def preparar_escolhas_melhoria():
    """Prepara uma lista de opções de melhoria para o jogador."""
    global opcoes_melhoria, botoes_opcao
    opcoes_melhoria.clear()
    botoes_opcao.clear()
    
    # Obtém 2 opções de melhoria aleatórias do sistema de itens
    opcoes_melhoria = get_upgrade_options(jogador, num_options=2) # 'get_upgrade_options' é importado

    largura_botao, altura_botao, espacamento_botoes = 450, 90, 30
    num_opcoes = len(opcoes_melhoria)
    pos_y_inicial_botoes = HEIGHT / 2 - ((altura_botao * num_opcoes + espacamento_botoes * (num_opcoes - 1)) / 2) + 50

    for i in range(num_opcoes):
        pos_y_botao = pos_y_inicial_botoes + i * (altura_botao + espacamento_botoes)
        botoes_opcao.append(Rect(WIDTH / 2 - largura_botao / 2, pos_y_botao, largura_botao, altura_botao))

def gerar_inimigo():
    """Gera um novo inimigo em uma posição aleatória fora da tela."""
    lado_tela = random.choice(['top', 'bottom', 'left', 'right']) # Mantido em inglês para lógica simples, poderia ser traduzido
    if lado_tela == 'top': posicao_spawn = (random.randint(0, WIDTH), -30)
    elif lado_tela == 'bottom': posicao_spawn = (random.randint(0, WIDTH), HEIGHT + 30)
    elif lado_tela == 'left': posicao_spawn = (-30, random.randint(0, HEIGHT))
    else: posicao_spawn = (WIDTH + 30, random.randint(0, HEIGHT)) # right
    
    # Adiciona variedade na geração de inimigos
    if random.random() < 0.7: # 70% de chance para um Lobo
        inimigos.append(Wolf(posicao_spawn)) # 'Wolf' é classe importada
    else: # 30% de chance para um Morcego
        inimigos.append(Bat(posicao_spawn)) # 'Bat' é classe importada

    # Aumenta a taxa de geração ao longo do tempo
    atraso_spawn = max(0.5, 2.5 - tempo_decorrido * 0.04)
    clock.schedule_unique(gerar_inimigo, atraso_spawn) # 'clock' é objeto global do Pygame Zero

# --- HOOKS DE EVENTO ---

def on_mouse_down(pos, button): # Hook do Pygame Zero, nome e parâmetros mantidos (pos, button)
    """Hook de evento de clique do mouse do PgZero."""
    global estado_jogo, som_ligado
    
    if estado_jogo == EstadoJogo.MENU:
        if botao_jogar.collidepoint(pos):
            estado_jogo = EstadoJogo.JOGANDO
            reiniciar_jogo()
        elif botao_som.collidepoint(pos):
            som_ligado = not som_ligado
            if not som_ligado: music.stop()
        elif botao_sair.collidepoint(pos):
            exit()

    elif estado_jogo == EstadoJogo.JOGANDO:
        if button == mouse.LEFT: # 'mouse.LEFT' é constante do Pygame Zero
            projeteis.append(Projetil(jogador.actor.pos, pos, jogador.projectile_base_damage))
            if som_ligado: sounds.shoot.play() # 'shoot' é nome do arquivo de som
            
    elif estado_jogo == EstadoJogo.FIM_DE_JOGO:
        estado_jogo = EstadoJogo.MENU

    elif estado_jogo == EstadoJogo.ESCOLHA_MELHORIA:
        for i, rect_botao_atual in enumerate(botoes_opcao):
            if rect_botao_atual.collidepoint(pos) and button == mouse.LEFT:
                item_escolhido = opcoes_melhoria[i]
                item_escolhido.apply(jogador) # Aplica o efeito do item
                print(f"Jogador escolheu: {item_escolhido.description}") # 'item_escolhido.description' vem do módulo Itens
                
                estado_jogo = EstadoJogo.JOGANDO
                opcoes_melhoria.clear()
                botoes_opcao.clear()
                break

# --- CLASSES AUXILIARES ---

class Projetil:
    """Representa um projétil disparado pelo jogador."""
    def __init__(self, pos_inicial, pos_alvo, valor_dano):
        self.actor = Actor("projectile.png", pos=pos_inicial) # "projectile.png" é nome do arquivo de imagem
        self.dano = valor_dano
        self.velocidade = 8
        
        # Calcula o ângulo e componentes de velocidade
        angulo_radianos = math.atan2(pos_alvo[1] - pos_inicial[1], pos_alvo[0] - pos_inicial[0])
        self.vx = math.cos(angulo_radianos) * self.velocidade
        self.vy = math.sin(angulo_radianos) * self.velocidade
        self.actor.angle = math.degrees(-angulo_radianos) + 90 # Ajusta o ângulo do ator

    def update(self):
        self.actor.x += self.vx
        self.actor.y += self.vy

    def draw(self):
        self.actor.draw()

class GemaExperiencia:
    """Representa uma gema de experiência deixada por um inimigo."""
    def __init__(self, pos): # 'pos' é a posição
        self.actor = Actor("gem.png", pos=pos) # "gem.png" é nome do arquivo de imagem
        self.valor_xp = 10

    def draw(self):
        self.actor.draw()

# --- INICIA O JOGO ---
pgzrun.go() # Função do Pygame Zero para iniciar o jogo