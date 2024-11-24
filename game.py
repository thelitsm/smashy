import pygame
import random
from unit import *

class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [
            Unit(0, 0, 10, 2, 'player',False,False),
            Unit(1, 0, 10, 2, 'player',False,False),
            RangedUnit(2, 0, 10, 2, 'player', 4,False,False)
        ]
        self.enemy_units = [
            Unit(6, 6, 1, 1, 'enemy',False,False),
            Unit(7, 6, 1, 1, 'enemy',False,False)
        ]

        self.MAP = [
            [0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 2, 2, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 1, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 1, 1, 0, 0, 0, 2, 0],
            [0, 0, 2, 2, 0, 0, 1, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:
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
                        selected_unit.move(dx, dy, self.MAP)
                        self.flip_display()
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy, self.MAP)
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Affiche le jeu."""
        
        MAP = self.MAP
        self.screen.fill(VALLEY_GREEN)
        for x in range(len(MAP)):
            for y in range(len(MAP[0])):
                tile = MAP[x][y]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if tile == 1:
                    pygame.draw.rect(self.screen, GROUND_BROWN, rect)
                elif tile == 2:
                    pygame.draw.rect(self.screen, RIVER_BLUE, rect)
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smashy")
    game = Game(screen)
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()
