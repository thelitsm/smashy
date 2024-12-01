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
RIVER_BLUE = (173,216,230,40)   #ajout de la couleur de l'eau pour la carte du jeu
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
        self.moves = 0
        self.attack_power = attack_power
        self.defense = defense  # Réduction des dégâts
        self.is_selected = False
        self.max_health = health # Vie maximale pour dessiner une barre de vie
        self.sp = 0

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

    def use_special2(self,game):
        print(self.unit_type)                

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

        sp_bar_width = int(CELL_SIZE * (self.max_health / 20))   # Ajuster la longueur max
        spc_bar_width = int(sp_bar_width * (self.sp / 6))
        bar_height = 5
        sp_x = self.x * CELL_SIZE + (CELL_SIZE - sp_bar_width ) // 2  # Centrer la barre
        sp_y = self.y * CELL_SIZE - 5 # Position au-dessus de l'unité


        # Fond rouge (barre vide)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, max_bar_width, bar_height))
        # Barre verte (barre de vie actuelle)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_bar_width, bar_height))

        #Fond Noir
        pygame.draw.rect(screen, BLACK, (sp_x, sp_y, sp_bar_width, bar_height))
        # Barre Bleue (barre de sp actuelle)
        pygame.draw.rect(screen, BLUE, (sp_x, sp_y, spc_bar_width, bar_height))



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
            speed=3, 
            attack_power=3,
            defense=0
        )

    def use_special(self, target):
        """
        Utilise la compétence spéciale du Hamster Gangster : "ak-noisettes".
        """
        print(f"{self.unit_type} utilise son ak-noisettes sur {target.unit_type} !")
        self.attack(target, is_special=True, coeff_attaque=1.5)
    def special2(self,game):
        print(f"{self.unit_type} utilise Nut Barrage !")
        for enemy in game.enemy_team.units:
            if abs(self.x - enemy.x) <= 1 and abs(self.y - enemy.y) <= 2:  # Vérifie si l'ennemi est dans le rayon
                damage = max(0, random.randint(3,10) - enemy.defense)  # dégats démultipliés
                enemy.health -= damage
                enemy.defense = max(0, enemy.defense - 1)  # Réduit la défense de 1
                print(f"{enemy.unit_type} subit {damage} dégâts de Nut Barrage et sa défense est réduite à {enemy.defense} !")
            if enemy.health <= 0:
                game.enemy_team.remove_dead_units()
                game.action_messages.append(f"{enemy.unit_type} est vaincu !")
    def draw(self, screen):
        """
        Dessine le Hamster Gangster avec ses spécificités.
        """
        super().draw(screen)

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
            speed=3, 
            attack_power=2,
            defense= 4
        )

    def use_special(self, targets):
        for ally in targets:
            if abs(self.x - ally.x) <= 1 and abs(self.y - ally.y) <= 1:
                r = random.randint(2, 5)
                ally.health += r
                print(f"{self.unit_type} soigne {ally.unit_type} de {r} pv !")
    def use_special2(self, game):
        for ally in game.player_team.units:
           if abs(self.x - ally.x) <= 1 and abs(self.y - ally.y) <= 1:
                r = random.randint(1, 3)
                ally.health += r 
        for enemy in game.enemy_team.units:
           if abs(self.x - enemy.x) <= 1 and abs(self.y - enemy.y) <= 1:
                r = random.randint(1, 3)
                ally.health -= r 
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
            speed=4, 
            attack_power=3,
            defense=1
        )

    def use_special(self, target):
        print(f"{self.unit_type} utilise son sabre tropical sur {target.unit_type} !")
        self.attack(target, is_special=True, coeff_attaque=1.5)

    def special2(self,game):
        #bomba
        x,y = 4,4        
        c = False
        while (not c):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_LEFT and x > 0:
                        x -= 1
                    elif event.key == pygame.K_RIGHT and x < GRID_SIZE - 1:
                        x += 1
                    elif event.key == pygame.K_UP and y > 0:
                        y -= 1
                    elif event.key == pygame.K_DOWN and y < GRID_SIZE - 1:
                        y += 1
                    game.flip_display()
                    for i in range(len(game.map)):
                        for j in range(len(game.map[0])):
                            if (x == i and abs(y - j) < 4) or (y == j and abs(x - i) < 4):
                                tile_rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                                pygame.draw.rect(game.screen, RED, tile_rect)
                    pygame.display.flip()
                    if event.key == pygame.K_SPACE:
                        c = True
        for enemy in game.enemy_team.units:
            if (x == enemy.x and abs(y - enemy.y) < 4) or (enemy.y == y and abs(enemy.x - x) < 4):
                enemy.health -= 3
                if enemy.health <= 0:
                    game.enemy_team.remove_dead_units()
                    game.action_messages.append(f"{enemy.unit_type} est vaincu !")
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
            speed=4, 
            attack_power=3,
            defense=1
        )

    def use_special(self, target):
        print(f"{self.unit_type} crache des meringues toxiques surn{target.unit_type} !")
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
