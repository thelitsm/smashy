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
            HamsterGangster(3,2),
            JusOrange(0,3),
            BananePlanteur(1,2)
        ]

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
            moves_left = 7 * selected_unit.speed  # Compteur de mouvement (7 déplacements max)
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

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
                        elif event.key == pygame.K_LEFT and not self.is_position_occupied(selected_unit.x - 1, selected_unit.y) and moves_left > 0:
                            dx = -1 * selected_unit.speed
                            moves_left -= selected_unit.speed
                        elif event.key == pygame.K_RIGHT and not self.is_position_occupied(selected_unit.x + 1, selected_unit.y) and moves_left > 0:
                            dx = 1 * selected_unit.speed
                            moves_left -= selected_unit.speed
                        elif event.key == pygame.K_UP and not self.is_position_occupied(selected_unit.x, selected_unit.y - 1) and moves_left > 0:
                            dy = -1 * selected_unit.speed
                            moves_left -= selected_unit.speed
                        elif event.key == pygame.K_DOWN and not self.is_position_occupied(selected_unit.x, selected_unit.y + 1) and moves_left > 0:
                            dy = 1 * selected_unit.speed
                            moves_left -= selected_unit.speed

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        if moves_left == 0 or event.key == pygame.K_SPACE:
                            self.action_messages.append(f"{selected_unit.unit_type} a terminé son déplacement.")
                            
                            # Menu de sélection de l'attaque à afficher dans la console du jeu
                            self.action_messages.append("Choisissez une attaque :")
                            self.action_messages.append("1: AK-Noisette")
                            self.action_messages.append("2: Morsure Double-Dents")
                            self.action_messages.append("3: Hibernation")
                            self.action_messages.append("4: Ne rien faire")
                            self.flip_display()


                            # Attente d'une touche pour l'attaque
                            attack_selected = False  # Flag pour vérifier si l'attaque a été choisie
                            while not attack_selected:
                                for event2 in pygame.event.get():
                                    if event2.type == pygame.KEYDOWN:
                                        if event2.key == pygame.K_1:
                                            selected_unit.attaque_ak_noisette(self.enemy_team)
                                            self.action_messages.append(f"{selected_unit.unit_type} utilise l'attaque AK-Noisette !")
                                            self.message_timer = pygame.time.get_ticks() + 3000
                                            attack_selected = True
                                        elif event2.key == pygame.K_2:
                                            selected_unit.attaque_morsure_double_dents(self.enemy_team)
                                            self.action_messages.append(f"{selected_unit.unit_type} utilise Morsure Double-Dents !")
                                            self.message_timer = pygame.time.get_ticks() + 3000
                                            attack_selected = True
                                        elif event2.key == pygame.K_3:
                                            selected_unit.hibernation()
                                            self.action_messages.append(f"{selected_unit.unit_type} utilise Hibernation pour se soigner !")
                                            self.message_timer = pygame.time.get_ticks() + 3000
                                            attack_selected = True
                                        elif event2.key == pygame.K_4:
                                            self.action_messages.append(f"{selected_unit.unit_type} ne fait rien.")
                                            self.message_timer = pygame.time.get_ticks() + 3000
                                            attack_selected = True

                                        has_acted = True
                                        selected_unit.is_selected = False
                                        break
                            
                            # Après avoir effectué l'attaque, afficher les messages d'action
                            for enemy in self.enemy_team.units:
                                if enemy.health <= 0:
                                    self.enemy_team.remove_dead_units()
                                    self.action_messages.append(f"{enemy.unit_type} est vaincu !")
                            has_acted = True
                            selected_unit.is_selected = False


    def handle_enemy_turn(self):
        for enemy in self.enemy_team.units[:]:
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

    def flip_display(self):
        # Dessiner l'image de fond limitée à la carte
        self.screen.blit(self.background_image, (0, 0), (0, 0, GRID_SIZE * CELL_SIZE, HEIGHT))

        # Dessiner la grille blanche
        for x in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, HEIGHT))  # Lignes verticales
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (GRID_SIZE * CELL_SIZE, y))  # Lignes horizontales

        # Dessiner les unités
        self.player_team.draw(self.screen)
        self.enemy_team.draw(self.screen)

        # Dessiner la console à droite (fond noir)
        pygame.draw.rect(self.screen, (0, 0, 0), (GRID_SIZE * CELL_SIZE, 0, 300, HEIGHT))  # Rectangle noir

        # Afficher les messages d'action dans la console
        font = pygame.font.SysFont(None, 24)
        y_offset = 10
        for message in self.action_messages[-20:]:  # Affiche les 20 derniers messages
            text_surface = font.render(message, True, (255, 255, 255))
            self.screen.blit(text_surface, (GRID_SIZE * CELL_SIZE + 10, y_offset))
            y_offset += 20

        # Mettre à jour l'écran
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
