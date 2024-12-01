import pygame
import random
import json

from unit import *
from tile import *
from display import *

class Game:
    """
    Classe pour représenter le jeu.
    """

    def __init__(self, screen):
        self.screen = screen
        self.current_message = ""
        self.message_timer = 0
        self.action_messages = []

        # Charger les propriétés de la carte à partir du fichier JSON
        self.load_map_from_json("map_config.json")

        # Initialisation des unités
        BASE_PATH_CARACTERS = 'assets/persos/'

        player_units = [
            HamsterGangster(0,2),
            JusOrange(0,3),
            BananePlanteur(1,2)
        ]
        player_units[0].sp = 6;
        player_units[1].sp = 6;
        player_units[2].sp = 6;

        enemy_units = [
            BonbonContaminé(19,19),
            MeringuichToxique(19,18),
            SucetteVolante(18,19)
        ]

        self.player_team = Team('Player', player_units)
        self.enemy_team = Team('Enemy', enemy_units)

        # Génération de la carte interactive
        self.generate_map()

    def is_position_occupied(self, x, y):
        """
        Vérifie si une position (x, y) est déjà occupée par une unité.
        
        x : int
            Position x de la case cible.
        y : int
            Position y de la case cible.
        """
         # Vérifie si (x, y) est dans les limites de la carte
        if not (0 <= x < len(self.map[0]) and 0 <= y < len(self.map)):
            return True  # Considère les positions hors limites comme non accessibles
    
        for unit in self.player_team.units + self.enemy_team.units:
            if unit.x == x and unit.y == y:
                return True
            # Vérifie si la case est franchissable
            actual_tile=self.map[y][x]
            if not actual_tile.walkable:  # Accès à la matrice de la carte
                return True
        return False
    
    def load_map_from_json(self, file_path):
        """
        Charge la matrice de la carte à partir d'un fichier JSON.
        """
        with open(file_path, "r") as file:
            self.map_matrix = json.load(file)["map"]

    def generate_map(self):
        self.map = []

        # mise en place de la map en arrière plan
        self.background_image = pygame.image.load('assets/game_map.png')
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH-LOG_WIDTH, HEIGHT))

        #Construit les objets `Tile` en fonction de la matrice chargée.

        for y, row in enumerate(self.map_matrix):
            tile_row = []
            for x, tile_type in enumerate(row):
                # Définir les propriétés de la case
                if tile_type == "mur":
                    is_walkable = False
                elif tile_type == "normal":  # Case normale
                    is_walkable = True

                # Créer l'objet `Tile`
                tile_row.append(Tile(x, y, tile_type, is_walkable))
            self.map.append(tile_row)
        print(self.map)

        # # Définir les proportions pour les cases spéciales
        # special_tile_types = {
        #     "infranchissable": 0.05,  # 5% de cases infranchissables
        #     "vitaminé": 0.10,           # 10% de cases régénératrices
        #     "huileuse": 0.07,        # 7% de cases glissantes
        #     "mielleuse": 0.08        # 8% de cases collantes
        # }

        # # Parcourir chaque case de la grille
        # for y in range(GRID_SIZE):
        #     row = []
        #     for x in range(GRID_SIZE):
        #         # Tirage aléatoire pour déterminer le type de la case
        #         random_value = random.random()
        #         tile_type = "normal"
        #         image_path = "assets/cases/normal.png"      #case normale par défaut 

        #         if random_value < special_tile_types["infranchissable"]:
        #             tile_type = "infranchissable"
        #             image_path = "assets/cases/spatule.png"
        #         elif random_value < special_tile_types["infranchissable"] + special_tile_types["vitaminé"]:
        #             tile_type = "vitaminé"
        #             image_path = "assets/cases/orange.png"
        #         elif random_value < (special_tile_types["infranchissable"] +
        #                             special_tile_types["vitaminé"] +
        #                             special_tile_types["huileuse"]):
        #             tile_type = "huileuse"
        #             image_path = "assets/cases/huile.png"
        #         elif random_value < (special_tile_types["infranchissable"] +
        #                             special_tile_types["vitaminé"] +
        #                             special_tile_types["huileuse"] +
        #                             special_tile_types["mielleuse"]):
        #             tile_type = "mielleuse"
        #             image_path = "assets/cases/miel.png"

        #         # Ajouter la case à la ligne
        #         row.append(Tile(x, y, tile_type, '0',image_path))

    
    
    # def apply_tile_effect(self, unit):
    #     current_tile = self.map[unit.y][unit.x]
    #     if current_tile.tile_type == "infranchissable":
    #         print(f"{unit.unit_type} ne peut pas passer ici !")
    #         return False
    #     elif current_tile.tile_type == "sucré":
    #         unit.health = min(unit.max_health, unit.health + 5)
    #         print(f"{unit.unit_type} régénère de la santé !")
    #     elif current_tile.tile_type == "huileuse":
    #         print(f"{unit.unit_type} glisse sur la case !")
    #         unit.move(random.choice([-1, 1]), random.choice([-1, 1]))
    #     elif current_tile.tile_type == "mielleuse":
    #         print(f"{unit.unit_type} est collé !")
    #         unit.speed = 0
    #     return True

    

    def handle_player_turn(self):
        for selected_unit in self.player_team.units:
            has_acted = False
            selected_unit.moves = selected_unit.speed
            selected_unit.is_selected = True
            self.flip_display()
            if (selected_unit.sp < 6):
                selected_unit.sp += 1
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_q:
                            pygame.quit()
                            exit()
                        elif event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        # Vérifier si le mouvement est valide
                        new_x, new_y = selected_unit.x + dx, selected_unit.y + dy
                        if (new_x, new_y) in self.get_reachable_tiles(selected_unit):
                            selected_unit.move(dx, dy)
                            selected_unit.moves -= 1
                            self.flip_display()

                        # Effectuer une attaque
                        if event.key == pygame.K_SPACE:  #ceci fait la fin du deplacement
                            selected_unit.moves = 0
                            self.flip_display()
                            choice = -1
                            font = pygame.font.Font(None, 26)
                            text_surface = font.render("A:passer son tour", True, WHITE)
                            text_surface2 = font.render("Z:Attaque", True, WHITE)
                            text_surface3 = font.render("E:Attaque Spéciale", True, WHITE)
                            text_surface4 = font.render("R:Attaque Spéciale2", True, WHITE)
                            self.screen.blit(text_surface, (820, 10))
                            self.screen.blit(text_surface2, (820, 30))
                            self.screen.blit(text_surface3, (820, 50))
                            self.screen.blit(text_surface4, (820, 70))
                            pygame.display.flip()                           

                            while (choice == -1):
                                for ch in pygame.event.get():
                                    if ch.type == pygame.KEYDOWN:                                        
                                        if (ch.key == pygame.K_a):
                                            choice = 0
                                        if ch.key == pygame.K_z :
                                            choice = 1
                                        if ch.key == pygame.K_e and selected_unit.sp >= 4:
                                            choice = 2
                                        if ch.key == pygame.K_r and selected_unit.sp >= 6:
                                            choice = 3
                                    elif event.type == pygame.QUIT:
                                        pygame.quit()   # pour pouvoir quitter meme pendant un tour
                                        exit()
                            tile_rect = pygame.Rect(820, 10, CELL_SIZE * 10, CELL_SIZE * 5)
                            pygame.draw.rect(self.screen, BLACK, tile_rect)
                            pygame.display.flip()
                            if (choice == 0):
                                if selected_unit.sp < 6:
                                    selected_unit.sp += 1
                            elif (choice == 1): #attaque de base
                                for enemy in self.enemy_team.units:
                                    if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                        damage = max(0, selected_unit.attack_power - enemy.defense)
                                        selected_unit.attack(enemy, False, 1)
                                        self.action_messages.append(f"{selected_unit.unit_type} attaque {enemy.unit_type} pour {damage} dégâts !")
                                        self.message_timer = pygame.time.get_ticks() + 3000
                                        if enemy.health <= 0:
                                            self.enemy_team.remove_dead_units()
                                            self.action_messages.append(f"{enemy.unit_type} est vaincu !")
                            elif (choice == 2):#attaque speciale 1
                                selected_unit.sp -= 4
                                if selected_unit.unit_type == "Jus orange":
                                    selected_unit.use_special(self.player_team.units)
                                else :
                                    for enemy in self.enemy_team.units:
                                        if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                            damage = max(0, selected_unit.attack_power - enemy.defense)
                                            #selected_unit.use_special(enemy, False, 1)
                                            selected_unit.use_special(enemy)
                                            self.action_messages.append(f"{selected_unit.unit_type} attaque {enemy.unit_type} pour {damage} dégâts !")
                                            self.message_timer = pygame.time.get_ticks() + 3000
                                            if enemy.health <= 0:
                                                self.enemy_team.remove_dead_units()
                                                self.action_messages.append(f"{enemy.unit_type} est vaincu !")
                            elif (choice == 3): #attaque speciale 2
                                selected_unit.sp -= 6
                                selected_unit.use_special2(self);
                            has_acted = True
                            selected_unit.is_selected = False  

    def handle_enemy_turn(self):
        for enemy in self.enemy_team.units:
            target = random.choice(self.player_team.units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                damage = max(0, enemy.attack_power - target.defense)
                enemy.attack(target,False,1)
                self.action_messages.append(f"{enemy.unit_type} attaque {target.unit_type} pour {damage} dégâts !")
                if target.health <= 0:
                    self.player_team.remove_dead_units()
                    self.action_messages.append(f"{target.unit_type} est vaincu !")


    def get_reachable_tiles(self, unit):
        """
        Retourne toutes les cases accessibles par une unité en fonction de sa vitesse.
        """
        reachable_tiles = []
        for dx in range(-unit.moves, unit.moves + 1):
            for dy in range(-unit.moves, unit.moves + 1):
                if abs(dx) + abs(dy) <= unit.moves:  # Distance Manhattan
                    new_x = unit.x + dx
                    new_y = unit.y + dy
                    if (0 <= new_x < GRID_SIZE and 
                        0 <= new_y < GRID_SIZE and 
                        not self.is_position_occupied(new_x, new_y) and 
                        self.map[new_y][new_x].walkable):
                        reachable_tiles.append((new_x, new_y))
        return reachable_tiles

    def flip_display(self):
        # Dessiner l'image de fond
        self.screen.blit(self.background_image, (0, 0))

        # Dessiner les tuiles accessibles pour l'unité sélectionnée
        for unit in self.player_team.units:
            if unit.is_selected:
                reachable_tiles = self.get_reachable_tiles(unit)
                for x, y in reachable_tiles:
                    tile_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, RIVER_BLUE, tile_rect)  # Remplissage bleu clair

        # Dessiner les unités
        self.player_team.draw(self.screen)
        self.enemy_team.draw(self.screen)

        # Mettre à jour l'affichage
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Le Monde Incroyable de Pierrot : l'Apocalypse")
    game = Game(screen)

    while True:
        game.handle_player_turn()
        if not game.enemy_team.is_defeated():
            game.handle_enemy_turn()
        if game.player_team.is_defeated() or game.enemy_team.is_defeated():
            # Gagnant
            if game.player_team.is_defeated():
                message = "Les zombibonbons dominent !"
            else:
                message = "Bravo ! Vous avez rétabli la paix !"
            print(message)
            pygame.time.wait(3000)
            pygame.quit()
            exit()

if __name__ == "__main__":
    main()
