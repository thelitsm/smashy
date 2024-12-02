import pygame
import random
import json

from tile import *

# Constantes
GRID_SIZE = 20
CELL_SIZE = 40
LOG_WIDTH = 500
WIDTH = GRID_SIZE * CELL_SIZE + LOG_WIDTH  # Ajoute la taille pour la console
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

class HamsterGangster(Unit):
    def __init__(self, x, y):
        """
        Initialisation spécifique au Hamster Gangster.
        """
        super().__init__(
            image_path="assets/persos/hamster_gangster.png",
            x=x,
            y=y,
            team="player",
            health=15,
            walk_on_wall=False,
            walk_on_water=False,
            unit_type="Hamster Gangster",
            speed=1, 
            attack_power=3,
            defense=0
        )

    def use_special(self, target):
        """
        Utilise la compétence spéciale du Hamster Gangster : "ak-noisettes".
        """
        print(f"{self.unit_type} utilise son ak-noisettes sur {target.unit_type} !")
        self.attack(target, is_special=True, coeff_attaque=1.5)

    def draw(self, screen):
        """
        Dessine le Hamster Gangster avec ses spécificités.
        """
        super().draw(screen)

    def attaque_ak_noisette(self, enemy_team):
        """
        Attaque à longue portée, tire sur un ennemi à une portée de 6 cases.
        """
        print(f"{self.unit_type} utilise l'attaque AK-Noisette !")
        for enemy in enemy_team.units:
            if abs(self.x - enemy.x) <= 6 and abs(self.y - enemy.y) <= 6:
                damage = max(0, self.attack_power - enemy.defense)
                enemy.health -= damage
                print(f"{enemy.unit_type} a subi {damage} dégâts !")
                if enemy.health <= 0:
                    print(f"{enemy.unit_type} est éliminé !")
                break  # Une fois l'ennemi touché, l'attaque se termine
    
    def attaque_morsure_double_dents(self, enemy_team):
        """
        Attaque à courte portée, rayon d'une case, double les dégâts.
        """
        print(f"{self.unit_type} utilise l'attaque Morsure Double-Dents !")
        for enemy in enemy_team.units:
            if abs(self.x - enemy.x) <= 1 and abs(self.y - enemy.y) <= 1:
                damage = 2 * (max(0, self.attack_power - enemy.defense))  # Double les dégâts
                enemy.health -= damage
                print(f"{enemy.unit_type} a subi {damage} dégâts !")
                if enemy.health <= 0:
                    print(f"{enemy.unit_type} est éliminé !")
                break  # Une fois l'ennemi touché, l'attaque se termine
    
    def hibernation(self):
        """
        Restaure des points de vie à Hamster Gangster.
        """
        heal_amount = 10  # Guérison de 10 points de vie
        self.health += heal_amount
        print(f"{self.unit_type} utilise Hibernation et récupère {heal_amount} points de vie !")

class JusOrange(Unit):
    def __init__(self, x, y):
        """
        Initialisation spécifique au Hamster Gangster.
        """
        super().__init__(
            image_path="assets/persos/jus_orange.png",
            x=x,
            y=y,
            team="player",
            health=15,
            walk_on_wall=False,
            walk_on_water=True,
            unit_type="Jus orange",
            speed=1, 
            attack_power=2,
            defense= 4
        )

    def use_special(self, target):
        print(f"{self.unit_type} soigne son co-equipier {target.unit_type} !")
        self.attack(target, is_special=False, coeff_attaque=1)

    def attaque_squeeze(self, enemy_team):
        print(f"{self.unit_type} utilise l'attaque Squeeze !")
        for enemy in enemy_team.units:
            if abs(self.x - enemy.x) <= 1 and abs(self.y - enemy.y) <= 1:
                damage = 1.5 * (max(0, self.attack_power - enemy.defense))  # Augmente légèrement les dégâts
                enemy.health -= damage
                print(f"{enemy.unit_type} a subi {damage} dégâts !")
                if enemy.health <= 0:
                    print(f"{enemy.unit_type} est éliminé !")
                break

    def attaque_vitamine_c(self, enemy_team):
        print(f"{self.unit_type} utilise l'attaque Vitamine C !")
        for enemy in enemy_team.units:
            if abs(self.x - enemy.x) <= 2 and abs(self.y - enemy.y) <= 2:
                damage = max(0, self.attack_power - enemy.defense)
                enemy.health -= damage
                print(f"{enemy.unit_type} a subi {damage} dégâts !")
                if enemy.health <= 0:
                    print(f"{enemy.unit_type} est éliminé !")
                break

    def draw(self, screen):

        super().draw(screen)

class BananePlanteur(Unit):
    def __init__(self, x, y):
        super().__init__(
            image_path="assets/persos/banane_pirate.png",
            x=x,
            y=y,
            team="player",
            health=15,
            walk_on_wall=False,
            walk_on_water=True,
            unit_type="Banane Planteur",
            speed=2, 
            attack_power=3,
            defense=1
        )

    def use_special(self, target):
        print(f"{self.unit_type} utilise son sabre tropical sur {target.unit_type} !")
        self.attack(target, is_special=True, coeff_attaque=1.5)

    def draw(self, screen):
        super().draw(screen)

class BonbonContaminé(Unit):
    def __init__(self, x, y):
        super().__init__(
            image_path="assets/persos/bonbon_contamine.png",
            x=x,
            y=y,
            team="enemy",
            health=15,
            walk_on_wall=False,
            walk_on_water=True,
            unit_type="Banane Planteur",
            speed=1, 
            attack_power=8,
            defense=2
        )

    def use_special(self, target):
        print(f"{self.unit_type} explose {target.unit_type} !")
        self.attack(target, is_special=True, coeff_attaque=2)

    def draw(self, screen):
        super().draw(screen)

class MeringuichToxique(Unit):
    def __init__(self, x, y):
        super().__init__(
            image_path="assets/persos/meringuich_toxique.png",
            x=x,
            y=y,
            team="enemy",
            health=15,
            walk_on_wall=False,
            walk_on_water=True,
            unit_type="Meringuich Toxique",
            speed=1, 
            attack_power=3,
            defense=1
        )

    def use_special(self, target):
        print(f"{self.unit_type} crache des meringues toxiques sur {target.unit_type} !")
        self.attack(target, is_special=True, coeff_attaque=1.5)

    def draw(self, screen):
        super().draw(screen)

class SucetteVolante(Unit):
    def __init__(self, x, y):
        super().__init__(
            image_path="assets/persos/sucette_volante.png",
            x=x,
            y=y,
            team="enemy",
            health=15,
            walk_on_wall=True,
            walk_on_water=True,
            unit_type="Sucette Volante",
            speed=2, 
            attack_power=3,
            defense=1
        )

    def use_special(self, target):
        print(f"{self.unit_type} inflige un coup d'aile sur {target.unit_type} !")
        self.attack(target, is_special=False, coeff_attaque=1)

    def draw(self, screen):
        super().draw(screen)
        

        
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
