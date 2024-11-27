import pygame
import random

# Constantes
GRID_SIZE = 20
CELL_SIZE = 40
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RIVER_BLUE = (173,216,230)   #ajout de la couleur de l'eau pour la carte du jeu
GROUND_BROWN = (165,42,42)   #ajout de la couleur des obstacles montagneux) pour la carte du jeu
VALLEY_GREEN =(144,238,144)  #ajout de la couleur de l'herbe(le sol) pour la carte 


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

    def __init__(self, image_path, x, y, team, health, walk_on_wall, walk_on_water, unit_type, speed, attack_power, defense):

        self.image = pygame.transform.scale(pygame.image.load(image_path), (CELL_SIZE, CELL_SIZE))       # ajustement de la taille de l'image
        self.x = x
        self.y = y
        self.team = team  # 'player' ou 'enemy'
        self.health = health
        self.walk_on_wall = walk_on_wall
        self.walk_on_water = walk_on_water
        self.unit_type = unit_type  # Type de l'unité
        self.speed = speed  # Vitesse de déplacement
        self.attack_power = attack_power
        self.defense = defense  # Réduction des dégâts
        self.is_selected = False
        self.max_health = health # Vie maximale pour dessiner une barre de vie

    def move(self, dx, dy):
        """
        Déplace l'unité de dx, dy en fonction de sa vitesse.
        """

        if abs(dx) + abs(dy) <= self.speed:  # Limite par la vitesse
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:  # Vérifie les limites de la grille
                self.x = new_x
                self.y = new_y

    def attack(self, target, is_special, coeff_attaque):
        """
        Attaque une unité cible.
        """
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            damage = self.attack_power
            if is_special:
                damage *= coeff_attaque  # multiplie les dégâts en mode spécial
            target.health -= max(0, damage - target.defense)  # Réduction par la défense

    def use_special(self, target):
        """
        Utilise une compétence spéciale.
        """
        if self.unit_type == 'Banane Planteur':
            print("Banane Planteur utilise son Coup de Sabre Tropical !")
            self.attack(target, is_special=True, coeff_attaque=1.2)
        elif self.unit_type == 'Jus orange':
            print("le jus d'orange lance des mini vitamines revitalisants !")
            target.health += 5  # Soigne un allié et lui ajoute 5 hp
        elif self.unit_type == 'Hamster Gangster':
            print("Hamster Gangster utilise son ak-noisettes !")
            self.attack(target, is_special=True, coeff_attaque=1.5)
        # elif self.unit_type == 'Bonbon Contaminé':
        #     print("Bonbon Contaminé explose dans un nuage de sucre !")
        #     target.health -= 5  # Inflige des dégâts à la zone
        #     self.health = 0  # Se détruit après l'explosion
        elif self.unit_type == 'Meringuich Zombie':
            print("Meringuich Zombie crache des meringues toxiques !")
            target.health -= 3  # Inflige des dégâts à un seul ennemi
        elif self.unit_type == 'Sucette Volante':
            print("Sucette Volante fonce sur sa cible !")
            target.health -= 7  # Dégâts puissants

    def degat_zone(self, team, position_x, position_y, damage):
        print(f"{self.unit_type} utilise une attaque de zone !")
        for unit in team.units:
            # Vérifie si l'unité est dans la zone de ±2 cases
            if abs(unit.x - position_x) <= 2 and abs(unit.y - position_y) <= 2:
                # Inflige les dégâts à l'unité
                unit.health -= max(0, damage - unit.defense)
                print(f"{unit.unit_type} a subi {max(0, damage - unit.defense)} dégâts !")
                if unit.health <= 0:
                    print(f"{unit.unit_type} est éliminé !")
                    

    def draw(self, screen):
        """
        Affiche l'unité sur l'écran avec une couleur spécifique et sa barre de vie.
        """

        # Couleur spécifique pour chaque type d'unité
        if (self.team == 'player'):
            color = BLUE  # bleu si ton équipe
        elif self.team == 'enemy':
            color = RED # rouge si adversaire

        # Dessiner le personnage avec son image
        screen.blit(self.image, (self.x * (CELL_SIZE), self.y * (CELL_SIZE)))  

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
        self.units = units  # Liste d'instances des personnage

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
