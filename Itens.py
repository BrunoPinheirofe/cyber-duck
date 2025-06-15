import random

class Item:
    """Classe base para um item ou melhoria que pode ser escolhida ao subir de nível."""
    def __init__(self, description):
        self.description = description

    def apply(self, player):
        """Aplica o efeito do item ao jogador. Deve ser sobrescrito."""
        raise NotImplementedError("O método 'apply' deve ser implementado por subclasses.")

# --- Melhorias de Arma e Atributos ---

class ProjectileDamageUpgrade(Item):
    def __init__(self):
        super().__init__("Aumenta o dano dos projéteis em 10.")

    def apply(self, player):
        player.increase_projectile_damage(10)

class MovementSpeedUpgrade(Item):
    def __init__(self):
        super().__init__("Aumenta a velocidade de movimento em 25%.")

    def apply(self, player):
        player.increase_movement_speed(0.25)

class MaxHealthUpgrade(Item):
    def __init__(self):
        super().__init__("Aumenta a vida máxima do jogador em 20.")

    def apply(self, player):
        player.increase_max_health(20)

# --- Melhorias Relacionadas à Arma Orbital ---

class OrbitalWeaponUnlock(Item):
    def __init__(self):
        super().__init__("Desbloqueia a arma orbital")

    def apply(self, player):
        player.activate_orbital_weapon()

class OrbitalDamageUpgrade(Item):
    def __init__(self):
        super().__init__("Aumenta o dano da arma orbital em 8")

    def apply(self, player):
        player.increase_orbital_damage(8)

class OrbitalSpeedUpgrade(Item):
    def __init__(self):
        super().__init__("Aumenta a velocidade da arma orbital em 50%")

    def apply(self, player):
        player.add_orbital_weapon(0.5)

# --- Melhorias de Utilidade ---
class HealthPotion(Item):
    def __init__(self):
        super().__init__("Restaura 50% da vida máxima do jogador.")
        
    def apply(self, player):
        heal_amount = player.max_health * 0.50
        player.heal(heal_amount)

# --- Função para obter melhorias disponíveis ---

def get_upgrade_options(player, num_options=3):
    """Retorna uma lista de `num_options` escolhas de melhoria válidas para o jogador."""
    possible_upgrades = [
        ProjectileDamageUpgrade,
        MovementSpeedUpgrade,
        MaxHealthUpgrade,
        HealthPotion,
    ]

    # Adiciona opções de arma orbital se estiver desbloqueada.
    if player.orbital_weapon_active:
        possible_upgrades.extend([
            OrbitalDamageUpgrade,
            OrbitalSpeedUpgrade,
        ])
    # Oferece o desbloqueio da arma orbital se ainda não estiver ativa.
    else:
        possible_upgrades.append(OrbitalWeaponUnlock)

    # Instancia os objetos de melhoria
    instantiated_upgrades = [cls() for cls in possible_upgrades]

    # Embaralha e seleciona o número de opções necessárias
    random.shuffle(instantiated_upgrades)
    return instantiated_upgrades[:num_options]