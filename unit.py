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
        self.moves = 0 # reste de mouvements possibles
        self.attack_power = attack_power # statistique d'attaque
        self.defense = defense  # Réduction des dégâts
        self.is_selected = False # est selectionné ?
        self.max_health = health # Vie maximale pour dessiner une barre de vie
        self.max_speed = 10 # Vitesse maximale pour limiter les déplacements
        self.min_speed = 1 # Vitesse minimal pour pouvoir se deplacer dans tout les cas
        self.sp = 0 # Points sur la barre spéciale
        self.is_active = False  # Ajout de cet attribut

    def move(self, dx, dy, game):
        """
        Déplace l'unité de dx, dy en fonction de sa vitesse et applique les effets des cases spéciales.
        """
        if abs(dx) + abs(dy) <= self.speed:  # Limite par la vitesse
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:  # Vérifie les limites de la grille
                target_tile = game.map[new_y][new_x]

                # Applique l'effet de la case miel
                if isinstance(target_tile, Miel):
                    target_tile.apply_effect(self)
                    game.action_messages.append(f"{self.unit_type} est immobilisé par le miel, et subit 2 degats !")
                
                # Applique l'effet de la case Orange
                if isinstance(target_tile, Orange):
                    target_tile.apply_effect(self)
                    game.action_messages.append(f"{self.unit_type} bénéficie de points de vie !")

                # Applique l'effet de la case éclair
                if isinstance(target_tile, Vitesse):
                    target_tile.apply_effect(self)
                    game.action_messages.append(f"{self.unit_type} bénéficie de points de vitesse !")

                self.x = new_x
                self.y = new_y

    def attack(self, target, is_special, coeff_attaque):
        """
        Attaque une unité cible avec/sans coefficient.
        """
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            damage = self.attack_power
            if is_special:
                damage *= coeff_attaque  # multiplie les dégâts en mode spécial
            target.health -= max(0, damage - target.defense)  # Réduction par la défense

    def get_details(self):
        '''
        Récupère les statistiques d'une unité et les détails de ses attaques pour avoir un affichage complet
        '''
        details = f" - Caractéristiques du personnage: \n"
        details += f"Vitesse: {self.speed}\n"
        details += f"Defense: {self.defense}\n"
        details += f"Attaques et degats: \n"
        details += f" - Attaque Basique: {self.attack_power}\n"
        details += f" - Special 1: {getattr(self, 'special1_description', {self.special1_description})}\n"
        details += f" - Special 2: {getattr(self, 'special2_description', {self.special2_description})}\n"
        return details          

    def draw(self, screen):
        '''
        dessine l'unité
        '''
        # dessine l'unité
        screen.blit(self.image, (self.x * (CELL_SIZE), self.y * (CELL_SIZE)))  

        # si l'unité est active, dessine un rectangle
        if self.is_active:
            c = (255, 0, 0)
            if self.team == 'player':
                c = (0, 0, 255)
            rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, c, rect, 3) 

        # Dessine la barre de vie
        max_bar_width = int(CELL_SIZE * (self.max_health / 20))
        current_bar_width = int(max_bar_width * (self.health / self.max_health))
        bar_height = 5
        bar_x = self.x * CELL_SIZE + (CELL_SIZE - max_bar_width) // 2
        bar_y = self.y * CELL_SIZE - 10

        # Dessine la barre des point spéciaux
        sp_bar_width = int(CELL_SIZE * (self.max_health / 20))
        spc_bar_width = int(sp_bar_width * (self.sp / 6))
        sp_x = self.x * CELL_SIZE + (CELL_SIZE - sp_bar_width) // 2
        sp_y = self.y * CELL_SIZE - 5

        # Barre de vie (rouge en fond et vert en premier plan
        pygame.draw.rect(screen, RED, (bar_x, bar_y, max_bar_width, bar_height))  # fond rouge
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_bar_width, bar_height))  # premier plan vert

        # Barre spéciale
        pygame.draw.rect(screen, BLACK, (sp_x, sp_y, sp_bar_width, bar_height))  # fond noir
        pygame.draw.rect(screen, BLUE, (sp_x, sp_y, spc_bar_width, bar_height))  # premier plan bleu


# on crée des sous classes héritées de unit pour chacun des 6 personnages du jeu (relation d'heritage)

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
            health=10,
            walk_on_wall=False,
            walk_on_water=False,
            unit_type="Hamster Gangster",
            speed=5, 
            attack_power=3,
            defense=1
        )
        self.attaque_description = "Morsure"
        self.special1_description = "Tire avec son Ak-noisettes"
        self.special2_description = "Nut Barrage : multiplie les dégats \n et réduit de 1 la défense des ennemis"

    def use_special(self, targets, game):
        """
        Utilise la compétence spéciale du Hamster Gangster : "ak-noisettes".
        """
        if not isinstance(targets, list):
            targets = [targets]  # Encapsule la cible unique dans une liste.
        for target in targets:
            self.attack(target, is_special=True, coeff_attaque=1.5)

    def use_special2(self,game):
        """
        Utilise la compétence légendaire du Hamster Gangster : "nut-barrage".
        """
        game.action_messages.append(f"{self.unit_type} utilise Nut Barrage !")
        for enemy in game.enemy_team.units:
            if abs(self.x - enemy.x) <= 2 and abs(self.y - enemy.y) <= 2:  # Vérifie si l'ennemi est dans le rayon
                damage = max(0, random.randint(3,10) - enemy.defense)  # dégats démultipliés
                enemy.health -= damage
                enemy.defense = max(0, enemy.defense - 1)  # Réduit la défense de 1
                game.action_messages.append(f"{enemy.unit_type} subit {damage} dégâts de Nut Barrage et sa défense est réduite à {enemy.defense} !")
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
            health=10,
            walk_on_wall=False,
            walk_on_water=False,
            unit_type="Jus orange",
            speed=4, 
            attack_power=2,
            defense= 2
        )
        self.attaque_description = "Coup de paille"
        self.special1_description = "Soigne ses alliés aléatoirement de 2 à 5 HP !"
        self.special2_description = "Soigne/pulvérise de 1 à 3 aléatoirement !"

    def use_special(self, targets, game):
        """
        Utilise la compétence spéciale du Jus d'Orange: "soigne les alliés entre 2 et 5 HP".
        """
        if not isinstance(targets, list):
            targets = [targets]  # Encapsule la cible unique dans une liste.
        for ally in targets:
            if abs(self.x - ally.x) <= 1 and abs(self.y - ally.y) <= 1:
                r = random.randint(2, 5)
                ally.health += r
                game.action_messages.append(f"{self.unit_type} soigne {ally.unit_type} de {r} pv !")
                
    def use_special2(self, game):
        """
        Utilise la compétence légendaire du Jus d'Orange: "Soigne/pulvérise de 1 à 3 aléatoirement".
        """
        for ally in game.player_team.units:
           
           if ally == 'Jus orange':
               pass
           
           elif abs(self.x - ally.x) <= 1 and abs(self.y - ally.y) <= 1:
                r = random.randint(1, 3)
                ally.health += r 
                game.action_messages.append(f"{self.unit_type} soigne {ally.unit_type} de {r} pv !")
        for enemy in game.enemy_team.units:
           if abs(self.x - enemy.x) <= 1 and abs(self.y - enemy.y) <= 1:
                r = random.randint(1, 3)
                ally.health -= r 
                game.action_messages.append(f"{self.unit_type} pulvérise {enemy.unit_type} de {r} pv !")

    def draw(self, screen):
        """
        Dessine le Jus d'Orange avec ses spécificités.
        """
        super().draw(screen)

class BananePlanteur(Unit):
    def __init__(self, x, y):
        super().__init__(
            image_path="assets/persos/banane_pirate.png",
            x=x,
            y=y,
            team="player",
            health=10,
            walk_on_wall=False,
            walk_on_water=True,
            unit_type="Banane Planteur",
            speed=5, 
            attack_power=3,
            defense=1
        )
        self.attaque_description = "Coup de banane"
        self.special1_description = "Utilise son sabre tropical x1.5"
        self.special2_description = "Bomba : parachute une bombe à distance ! "

    def use_special(self, targets,game):
        """
        Utilise la compétence spéciale de la Banane Planteur: "Utilise son sabre tropical x1.5".
        """
        if not isinstance(targets, list):
            targets = [targets]  # Encapsule la cible unique dans une liste.
        for target in targets:
            self.attack(target, is_special=True, coeff_attaque=1.5)
            game.action_messages.append(f"{self.unit_type} utilise son sabre tropical sur {target.unit_type} !")

    def use_special2(self,game):
        """
        Utilise la compétence légendaire de la Banane Planteur: "Bomba : parachute une bombe à distance !".
        """
        #bomba
        x,y = 9,9        
        c = False
        while (not c):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and x > 0:
                        x -= 1
                    elif event.key == pygame.K_d and x < GRID_SIZE - 1:
                        x += 1
                    elif event.key == pygame.K_z and y > 0:
                        y -= 1
                    elif event.key == pygame.K_s and y < GRID_SIZE - 1:
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
            health=10,
            walk_on_wall=False,
            walk_on_water=True,
            unit_type="Bonbon Contaminé",
            speed=4, 
            attack_power=4,
            defense=0
        )
        self.attaque_description = "Coup de poing"
        self.special1_description = "Coup carambarisé x2"
        self.special2_description = "Explosion sucrée: soigne ses alliés \n et contamine ses enemis"

    def use_special(self, targets, game):
        """
        Utilise la compétence spéciale du Bonbon Contaminé: "Coup carambarisé x2".
        """
        if not isinstance(targets, list):
            targets = [targets]  # Encapsule la cible unique dans une liste.

        for target in targets:
            self.attack(target, is_special=True, coeff_attaque=1.5)
            game.action_messages.append(f"{self.unit_type} explose {target.unit_type} !")

    def use_special2(self, game):
        """
        Utilise la compétence légendaire du Bonbon Contaminé: "Explosion sucrée: soigne ses alliés \n et contamine ses enemis".
        """  
        for ally in game.enemy_team.units:
           if ally == "Bonbon Contaminé":
               pass
           elif abs(self.x - ally.x) <= 1 and abs(self.y - ally.y) <= 1:
                r = random.randint(1, 3)
                ally.health += r 
                game.action_messages.append(f"{self.unit_type} soigne {ally.unit_type} de {r} pv !")
        for enemy in game.player_team.units:
           if abs(self.x - enemy.x) <= 1 and abs(self.y - enemy.y) <= 1:
                r = random.randint(3, 6)
                enemy.health -= r 
                game.action_messages.append(f"{self.unit_type} pulvérive {enemy.unit_type} de {r} pv !")

    def draw(self, screen):
        """
        Dessine le BonbonContaminé avec ses spécificités.
        """
        super().draw(screen)

class MeringuichToxique(Unit):
    def __init__(self, x, y):
        super().__init__(
            image_path="assets/persos/meringuich_toxique.png",
            x=x,
            y=y,
            team="enemy",
            health=10,
            walk_on_wall=False,
            walk_on_water=True,
            unit_type="Meringuich Toxique",
            speed=5, 
            attack_power=2,
            defense=2
        )
        self.attaque_description = "Coup de chantilly"
        self.special1_description = "Craache des meringues toxiques"
        self.special2_description = "Coup de pied de Jean Claude VD"

    def use_special(self, targets, game):
        """
        Utilise la compétence spéciale de Meringuich Toxique: "Crache des meringues toxiques".
        """
        if not isinstance(targets, list):
            targets = [targets]  # Encapsule la cible unique dans une liste.

        for target in targets:
            self.attack(target, is_special=True, coeff_attaque=1.5)
            game.action_messages.append(f"{self.unit_type} crache des meringues toxiques surn{target.unit_type} !")


    def use_special2(self, game):
        """
        Utilise la compétence légendaire de Meringuich Toxique: "Coup de pied de Jean Claude VD".
        """
        for enemy in game.player_team.units:
            #LE COUP DE PIED DE JEAN CLAUDE VAN DAMME
            if abs(self.x - enemy.x) <= 1 or abs(self.y - enemy.y) <= 1:
                n=3
                enemy.health -= (self.attack_power+1)
                dx,dy = (enemy.x-self.x,enemy.y-self.y)
                if dx != 0 and dy != 0:
                    n-=1 # si un perso est en diagonale la distance parcourue par le kick est diminuée
                while not game.is_position_occupied((enemy.x + dx), enemy.y + dy, self) and n > 0:
                    enemy.x += dx
                    enemy.y += dy
                    n-=1
                if n!=3:
                    enemy.health -= (self.attack_power+1)
        if enemy.health <= 0:
            game.player_team.remove_dead_units()
            game.action_messages.append(f"{enemy.unit_type} est vaincu !")
                    

    def draw(self, screen):
        """
        Dessine le Meringuich Toxique avec ses spécificités.
        """
        super().draw(screen)

class SucetteVolante(Unit):
    def __init__(self, x, y):
        super().__init__(
            image_path="assets/persos/sucette_volante.png",
            x=x,
            y=y,
            team="enemy",
            health=10,
            walk_on_wall=True,  # Peut traverser les murs
            walk_on_water=True,
            unit_type="Sucette Volante",
            speed=5, 
            attack_power=3,
            defense=1
        )
        self.attaque_description = "Coup simple"
        self.special1_description = "Coup d'aile"
        self.special2_description = "Paquet de sucettes explosives volantes"

    def use_special(self, targets,game):
        """
        Utilise la compétence spéciale de la Sucette Volante: "Coup d'aile".
        """
        if not isinstance(targets, list):
            targets = [targets]  # Encapsule la cible unique dans une liste.
        for target in targets:
            self.attack(target, is_special=True, coeff_attaque=2)
            game.action_messages.append(f"{self.unit_type} inflige un coup d'aile sur {target.unit_type} !")

    def use_special2(self,game):
        """
        Utilise la compétence spéciale de la Sucette Volante: "Paquet de sucettes explosives volantes".
        """
        #avion bombardier
        x,y = 9,9        
        c = False
        while (not c):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()   
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x > 0:
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
                            a,b = i - x, j - y
                            if (abs(a) == abs(b)) and (abs(a) + abs(b)) < 4:
                                tile_rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                                pygame.draw.rect(game.screen, RED, tile_rect)
                    pygame.display.flip()
                    if event.key == pygame.K_RETURN:
                        c = True

        # a revoir !
        for enemy in game.player_team.units:
            if (x == enemy.x and abs(y - enemy.y) < 6) or (enemy.y == y and abs(enemy.x - x) < 6):
                enemy.health -= 3
                if enemy.health <= 0:
                    game.player_team.remove_dead_units()
                    game.action_messages.append(f"{enemy.unit_type} est vaincu !")
    def draw(self, screen):
        """
        Dessine la Sucette Volante avec ses spécificités.
        """
        super().draw(screen)
        
# Agrégation entre Unit et Team :
# Les unités sont regroupées au sein d'une équipe, mais elles conservent leur autonomie.
# Cela permet une gestion claire des interactions et des états des équipes dans le jeu
        
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
