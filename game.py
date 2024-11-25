import pygame
import random
import os

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
            Unit(BASE_PATH_CARACTERS + 'banane_pirate.png', 0, 0, 20, 5, 'player', False, False, 'Banane Pirate', speed=2, defense=3),
            Unit(BASE_PATH_CARACTERS + 'jus_orange.png', 1, 0, 15, 3, 'player', False, False, 'Jus d\'Orange', speed=2, defense=2),
            Unit(BASE_PATH_CARACTERS + 'hamster_gangster.png', 2, 0, 10, 4, 'player', False, False, 'Hamster Gangster', speed=3, defense=1)
        ]

        enemy_units = [
            Enemy(BASE_PATH_CARACTERS + 'bonbon_contamine.png', 6, 6, 10, 3, False, False, 'Bonbon Contaminé', speed=1, defense=0),
            Enemy(BASE_PATH_CARACTERS + 'meringuich_toxique.png', 7, 6, 15, 2,False, False, 'Gâteau Zombie', speed=1, defense=2),
            Enemy(BASE_PATH_CARACTERS + 'sucette_volante.png', 5, 5, 8, 5,False, False, 'Sucette Volante', speed=2, defense=1)
        ]

        self.player_team = Team('Player', player_units)
        self.enemy_team = Team('Enemy', enemy_units)

        # Génération de la carte interactive
        self.generate_map()

    def generate_map(self):
        self.map = []
        for y in range(GRID_SIZE):
            row = []
            for x in range(GRID_SIZE):
                try:
                    if (x + y) % 5 == 0:
                        image_path = "assets/cases/spatule.png"
                        tile_type = "infranchissable"
                    elif (x + y) % 4 == 0:
                        image_path = "assets/cases/orange.png"
                        tile_type = "sucré"
                    elif (x + y) % 3 == 0:
                        image_path = "assets/cases/huile.png"
                        tile_type = "huileuse"
                    elif (x + y) % 2 == 0:
                        image_path = "assets/cases/miel.png"
                        tile_type = "mielleuse"
                    else:
                        image_path = "assets/cases/normal.png"
                        tile_type = "normal"

                    if not os.path.exists(image_path):
                        raise FileNotFoundError(f"Fichier manquant : {image_path}")

                    row.append(Tile(x, y, tile_type, image_path))

                except FileNotFoundError as e:
                    print(e)
                    pygame.quit()
                    exit()
            self.map.append(row)

    def apply_tile_effect(self, unit):
        current_tile = self.map[unit.y][unit.x]
        if current_tile.tile_type == "infranchissable":
            print(f"{unit.unit_type} ne peut pas passer ici !")
            return False
        elif current_tile.tile_type == "sucré":
            unit.health = min(unit.max_health, unit.health + 5)
            print(f"{unit.unit_type} régénère de la santé !")
        elif current_tile.tile_type == "huileuse":
            print(f"{unit.unit_type} glisse sur la case !")
            unit.move(random.choice([-1, 1]), random.choice([-1, 1]))
        elif current_tile.tile_type == "mielleuse":
            print(f"{unit.unit_type} est collé !")
            unit.speed = 0
        return True

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
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_team.units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    damage = max(0, selected_unit.attack_power - enemy.defense)
                                    selected_unit.attack(enemy)
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
                enemy.attack(target)
                self.action_messages.append(f"{enemy.unit_type} attaque {target.unit_type} pour {damage} dégâts !")
                if target.health <= 0:
                    self.player_team.remove_dead_units()
                    self.action_messages.append(f"{target.unit_type} est vaincu !")

    def flip_display(self):
        self.screen.fill(BLACK)
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
