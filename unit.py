import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, image_path, x, y, health, attack_power, team, unit_type, speed, defense):
        """
        Construit une unité avec des attributs spécifiques.
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.unit_type = unit_type  # Type de l'unité
        self.speed = speed  # Vitesse de déplacement
        self.defense = defense  # Réduction des dégâts
        self.is_selected = False
        self.max_health = health
        # Charger l'image avec gestion des erreurs
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image : {image_path}")
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.image.fill((255, 0, 0))  # Remplacer par une couleur rouge par défaut

    def move(self, dx, dy):
        """
        Déplace l'unité de dx, dy en fonction de sa vitesse.
        """
        if abs(dx) + abs(dy) <= self.speed:  # Limite par la vitesse
            if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
                self.x += dx
                self.y += dy

    def attack(self, target, is_special=False):
        """
        Attaque une unité cible.
        """
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            damage = self.attack_power
            if is_special:
                damage *= 1.5  # multiplie les dégâts en mode spécial
            target.health -= max(0, damage - target.defense)  # Réduction par la défense

    def use_special(self, target):
        """
        Utilise une compétence spéciale.
        """
        if self.unit_type == 'Banane Pirate':
            print("Banane Pirate utilise son Coup de Sabre Tropical !")
            self.attack(target, is_special=True)
        elif self.unit_type == 'Tasse de Café':
            print("Tasse de Café lance du Café Revitalisant !")
            target.health += 5  # Soigne un allié
        elif self.unit_type == 'Hamster Gangster':
            print("Hamster Gangster utilise son ak-noisettes !")
            self.attack(target, is_special=True)

    def draw(self, screen):
        """
        Affiche l'unité sur l'écran avec une couleur spécifique et sa barre de vie.
        """

        # Couleur spécifique pour chaque type d'unité
        if self.unit_type == 'Banane Pirate':
            color = (255, 255, 0)  # Jaune
        elif self.unit_type == 'Tasse de Café':
            color = (165, 42, 42)  # Marron
        elif self.unit_type == 'Hamster Gangster':
            color = (128, 128, 128)  # Gris
        else:
            color = RED if self.team == 'enemy' else BLUE

        # Dessiner le personnage avec son image
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        # Dessiner la barre de vie
        max_bar_width = int(CELL_SIZE * (self.max_health / 20))  # Ajuster la longueur max
        current_bar_width = int(max_bar_width * (self.health / self.max_health))
        bar_height = 5
        bar_x = self.x * CELL_SIZE + (CELL_SIZE - max_bar_width) // 2  # Centrer la barre
        bar_y = self.y * CELL_SIZE - 10  # Position au-dessus de l'unité

        # Fond rouge (barre vide)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, max_bar_width, bar_height))

        # Barre verte (barre de vie actuelle)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_bar_width, bar_height))

        
class Team:
    """
    Classe pour représenter une équipe.
    """
    def __init__(self, name, units):
        """
        Initialise une équipe avec un nom et une liste d'unités.
        """
        self.name = name  # Nom de l'équipe (ex. 'Player', 'Enemy')
        self.units = units  # Liste d'instances de Unit

    def is_defeated(self):
        """
        Vérifie si l'équipe est éliminée.
        """
        return all(unit.health <= 0 for unit in self.units)

    def remove_dead_units(self):
        """
        Supprime les unités mortes de l'équipe.
        """
        self.units = [unit for unit in self.units if unit.health > 0]

    def draw(self, screen):
        """
        Dessine toutes les unités de l'équipe.
        """
        for unit in self.units:
            unit.draw(screen)

class Enemy(Unit):
    """
    Classe pour représenter un ennemi.
    Hérite de la classe Unit.
    """
    def __init__(self, image_path, x, y, health, attack_power, unit_type, speed, defense):
        super().__init__(image_path, x, y, health, attack_power, 'enemy', unit_type, speed, defense)

    def use_special(self, target):
        """
        Compétence spéciale des ennemis.
        """
        if self.unit_type == 'Bonbon Contaminé':
            print("Bonbon Contaminé explose dans un nuage de sucre !")
            target.health -= 5  # Inflige des dégâts à la zone
            self.health = 0  # Se détruit après l'explosion
        elif self.unit_type == 'Gâteau Zombie':
            print("Gâteau Zombie crache des miettes toxiques !")
            target.health -= 3  # Inflige des dégâts à un seul ennemi
        elif self.unit_type == 'Sucette Volante':
            print("Sucette Volante fonce sur sa cible !")
            target.health -= 7  # Dégâts puissants
            self.health -= 2  # Subit un contrecoup

