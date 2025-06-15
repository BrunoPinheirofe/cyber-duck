# 🦆 Cyber-Pato: Sobrevivência de Dados 🎮

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Pygame Zero](https://img.shields.io/badge/Pygame%20Zero-1.2+-green.svg?style=for-the-badge)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-red.svg?style=for-the-badge&logo=pygame&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

</div>

## 📖 Descrição

**Cyber-Pato: Sobrevivência de Dados** é um jogo de ação 2D desenvolvido em Python usando Pygame Zero. Controle um pato cibernético que deve sobreviver a ondas de inimigos enquanto coleta gemas de experiência para evoluir e se tornar mais poderoso!

### 🎯 Características Principais

- 🎮 **Gameplay dinâmico**: Sistema de combate com projéteis e inimigos
- 📈 **Sistema de progressão**: Coleta XP e evolua de nível com barra de progresso visual
- 🐺 **Inimigos inteligentes**: Lobos que perseguem o jogador de forma inteligente
- 💎 **Sistema de recompensas**: Gemas de experiência que dropam dos inimigos eliminados
- 🎨 **Interface intuitiva**: Barra de XP na parte inferior da tela
- ⏸️ **Sistema de pausa**: Tela de level up que pausa o jogo automaticamente
- 🎯 **Controles responsivos**: Movimento suave com WASD ou setas

## 🚀 Como Executar

### 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 🔧 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/teste_game.git
cd teste_game
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual:**

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

4. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

### 🎮 Executando o Jogo

```bash
pgzrun main.py
```

## 🎮 Controles

| Ação | Tecla/Mouse |
|------|-------------|
| **Mover** | `WASD` ou `Setas` |
| **Atirar** | `Clique Esquerdo` |
| **Continuar** | `Clique` (durante level up) |

## 🎯 Objetivo do Jogo

- **Sobreviva** às ondas de inimigos que aparecem a cada 2 segundos
- **Elimine inimigos** com seus projéteis para fazer drop de gemas de XP
- **Colete gemas** de experiência para ganhar XP
- **Suba de nível** para se tornar mais poderoso (cada nível requer 50% mais XP)
- **Mantenha-se vivo** enquanto enfrenta ondas cada vez mais desafiadoras

## 🎮 Mecânicas do Jogo

### 🦆 Jogador (Cyber-Pato)
- **Movimento**: Controle suave com velocidade de 3 unidades
- **Tiro**: Projéteis que seguem a direção do mouse
- **Progressão**: Sistema de níveis com XP crescente
- **Limites**: Não pode sair da tela

### 🐺 Inimigos (Lobos)
- **IA**: Perseguem o jogador de forma inteligente
- **Spawn**: Aparecem nas bordas da tela a cada 2 segundos
- **Velocidade**: Variável entre 1.0 e 2.0 unidades
- **Recompensa**: Dropam gemas de XP quando eliminados

### 💎 Sistema de XP
- **Coleta**: Cada gema vale 1 ponto de experiência
- **Progressão**: XP necessário aumenta 50% a cada nível
- **Visual**: Barra de progresso na parte inferior da tela
- **Level Up**: Tela de pausa automática ao subir de nível

## 🛠️ Tecnologias Utilizadas

- **🐍 Python 3.8+**: Linguagem principal
- **🎮 Pygame Zero 1.2+**: Framework de desenvolvimento de jogos
- **🎮 Pygame 2.6+**: Biblioteca base para gráficos e input
- **🎨 Assets Customizados**: Sprites e recursos visuais

## 📁 Estrutura do Projeto

```
teste_game/
├── main.py              # Arquivo principal do jogo (227 linhas)
├── requirements.txt     # Dependências do projeto
├── images/              # Pasta com sprites e assets
│   ├── pato_placeholder.png  # Sprite do jogador
│   ├── wolf.png              # Sprite dos inimigos
│   ├── bullet.png            # Sprite dos projéteis
│   └── gem.png               # Sprite das gemas de XP
├── duck-idle2.png       # Asset adicional do pato
├── bomb.png             # Asset de bomba
├── tile_0105.png        # Asset de tile
├── tile_0129.png        # Asset de tile
├── README.md            # Este arquivo
└── .gitignore          # Arquivos ignorados pelo Git
```

## 🎮 Estados do Jogo

### 🎯 Playing
- Jogador pode se mover e atirar
- Inimigos perseguem o jogador
- Sistema de colisão ativo
- Barra de XP visível

### ⏸️ Level Up
- Jogo pausado automaticamente
- Tela de "LEVEL UP!" exibida
- Clique para retornar ao jogo
- Progresso salvo

## 🔧 Configurações do Jogo

```python
# Configurações da janela
WIDTH = 800
HEIGHT = 600
TITLE = "Cyber-Pato: Sobrevivência de Dados"

# Configurações do jogador
PLAYER_SPEED = 3
PROJECTILE_SPEED = 8
ENEMY_SPAWN_RATE = 2.0  # segundos
```

## 🐛 Solução de Problemas

### Erro: "pgzrun: command not found"
```bash
pip install pgzero
```

### Erro: "No module named 'pygame'"
```bash
pip install pygame
```

### Performance lenta
- Certifique-se de que o ambiente virtual está ativo
- Verifique se todas as dependências estão instaladas corretamente

## 📚 Documentação e Recursos

### 📖 Pygame Zero
- [📚 Documentação Oficial](https://pygame-zero.readthedocs.io/)
- [🎮 Guia de Início Rápido](https://pygame-zero.readthedocs.io/en/stable/introduction.html)
- [🔧 Referência da API](https://pygame-zero.readthedocs.io/en/stable/handbook/index.html)

### 🐍 Python
- [📚 Documentação Python](https://docs.python.org/)
- [🎮 Pygame Documentation](https://www.pygame.org/docs/)

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Desenvolvedor

Desenvolvido com ❤️ usando Python e Pygame Zero.

---

**Divirta-se jogando Cyber-Pato: Sobrevivência de Dados!** 🦆🎮
