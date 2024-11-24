import pygame
import random

# voici un commentaire pour tester le push

# Constantes
GRID_SIZE = 12
CELL_SIZE = 60
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
VALLEY_GREEN =(144,238,144) #ajout de la couleur de l'herbe(le sol) pour la carte du jeu


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
    walk_on_water : bool
        unité peut elle marcher sur l'eau (tile==2)
    walk_on_wall : bool
        unité peut elle marcher sur les murs (tile==1)

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, team,walk_on_wall,walk_on_water):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
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
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.walk_on_water = walk_on_wall
        self.walk_on_wall = walk_on_wall


    """def move(self, dx, dy):
        
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
    """
    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    #ajout de la fonction can_move:
    def can_move_to(self, x, y, game_map):
        """
        Vérifie si l'unité peut se déplacer à la case spécifiée.

        Paramètres
        ----------
        x : int
            La position x cible.
        y : int
            La position y cible.
        game_map : list[list[int]]
            La carte du jeu, où chaque case est une valeur (0, 1, ou 2).

        Retourne
        --------
        bool : True si l'unité peut se déplacer à la case, False sinon.
        """
        if not (0 <= x < len(game_map) and 0 <= y < len(game_map[0])):
            return False  # En dehors de la carte
        tile = game_map[x][y]
        if tile == 2 and not self.walk_on_water:
            return False  # Ne peut pas marcher sur l'eau
        if tile == 1 and not self.walk_on_wall:
            return False  # Ne peut pas marcher sur les murs
        return True
    def move(self, dx, dy, game_map):
        """
        Déplace l'unité de dx, dy si la case est valide.

        Paramètres
        ----------
        dx : int
            Déplacement en x.
        dy : int
            Déplacement en y.
        game_map : list[list[int]]
            La carte du jeu.
        """
        new_x, new_y = self.x + dx, self.y + dy
        print(self.x)
        print(self.y)
        
        print(new_x)
        print(new_y)
        if self.can_move_to(new_x, new_y, game_map):
            self.x = new_x
            self.y = new_y
    
    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


class RangedUnit(Unit):
    def __init__ (self, x, y, health, attack_power, team, range,walk_on_wall,walk_on_water):
        super().__init__(x, y,health,attack_power,team,walk_on_wall,walk_on_water)
        self.range = range

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= range or abs(self.y - target.y) <= range:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
