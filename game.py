import pygame
import random

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

        # Initialisation des unités
        BASE_PATH_CARACTERS = 'assets/persos/'

        player_units = [
            Unit(BASE_PATH_CARACTERS + 'banane_pirate.png', 0, 2,'player', 10, False, False, 'Banane Pirate', speed=2, attack_power=2, defense=2),
            Unit(BASE_PATH_CARACTERS + 'jus_orange.png', 1, 2,'player', 10, False, False, 'Jus d\'Orange', speed=1, attack_power=1, defense=4),
            Unit(BASE_PATH_CARACTERS + 'hamster_gangster.png', 0, 3,'player', 15, False, False, 'Hamster Gangster', speed=1,attack_power=3, defense=2)
        ]

        enemy_units = [
            Unit(BASE_PATH_CARACTERS + 'bonbon_contamine.png', 16, 16,'enemy', 10, False, False, 'Bonbon Contaminé', speed=1, attack_power=2, defense=1),
            Unit(BASE_PATH_CARACTERS + 'meringuich_toxique.png', 15, 16,'enemy', 15, False, False, 'Gâteau Zombie', speed=1, attack_power=2, defense=1),
            Unit(BASE_PATH_CARACTERS + 'sucette_volante.png', 16, 15,'enemy', 10, False, False, 'Sucette Volante', speed=3, attack_power=2, defense=1)
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
        for unit in self.player_team.units + self.enemy_team.units:
            if unit.x == x and unit.y == y:
                return True
        return False

    def generate_map(self):
        self.map = []

        # mise en place de la map en arrière plan
        self.background_image = pygame.image.load('assets/game_map.png')
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        # Définir les proportions pour les cases spéciales
        special_tile_types = {
            "infranchissable": 0.05,  # 5% de cases infranchissables
            "vitaminé": 0.10,           # 10% de cases régénératrices
            "huileuse": 0.07,        # 7% de cases glissantes
            "mielleuse": 0.08        # 8% de cases collantes
        }

        # Parcourir chaque case de la grille
        for y in range(GRID_SIZE):
            row = []
            for x in range(GRID_SIZE):
                # Tirage aléatoire pour déterminer le type de la case
                random_value = random.random()
                tile_type = "normal"
                image_path = "assets/cases/normal.png"      #case normale par défaut 

                if random_value < special_tile_types["infranchissable"]:
                    tile_type = "infranchissable"
                    image_path = "assets/cases/spatule.png"
                elif random_value < special_tile_types["infranchissable"] + special_tile_types["vitaminé"]:
                    tile_type = "vitaminé"
                    image_path = "assets/cases/orange.png"
                elif random_value < (special_tile_types["infranchissable"] +
                                    special_tile_types["vitaminé"] +
                                    special_tile_types["huileuse"]):
                    tile_type = "huileuse"
                    image_path = "assets/cases/huile.png"
                elif random_value < (special_tile_types["infranchissable"] +
                                    special_tile_types["vitaminé"] +
                                    special_tile_types["huileuse"] +
                                    special_tile_types["mielleuse"]):
                    tile_type = "mielleuse"
                    image_path = "assets/cases/miel.png"

                # Ajouter la case à la ligne
                row.append(Tile(x, y, tile_type, '0',image_path))

    
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
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT and not self.is_position_occupied(selected_unit.x - 1,selected_unit.y):
                            dx = -1
                        elif event.key == pygame.K_RIGHT and not self.is_position_occupied(selected_unit.x + 1,selected_unit.y):
                            dx = 1
                        elif event.key == pygame.K_UP and not self.is_position_occupied(selected_unit.x,selected_unit.y - 1):
                            dy = -1
                        elif event.key == pygame.K_DOWN and not self.is_position_occupied(selected_unit.x,selected_unit.y +1):
                            dy = 1

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_team.units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    damage = max(0, selected_unit.attack_power - enemy.defense)
                                    selected_unit.attack(enemy,False,1)
                                    self.current_message = f"{selected_unit.unit_type} attaque {enemy.unit_type} pour {damage} dégâts !"
                                    self.message_timer = pygame.time.get_ticks() + 1500
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
        # Dessiner l'image de fond
        self.screen.blit(self.background_image, (0, 0))
        # Dessiner la grille blanche
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, HEIGHT))  # Lignes verticales
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (WIDTH, y))  # Lignes horizontales
        for row in self.map:
            for tile in row:
                tile.draw(self.screen)
        self.player_team.draw(self.screen)
        self.enemy_team.draw(self.screen)
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
