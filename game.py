import pygame
import random
import os

from unit import *
from display import *
from tile import *


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
        """
        self.current_message = ""  # Message actuel à afficher
        self.message_timer = 0  # Timer pour effacer le message
        self.screen = screen
        self.action_messages = []  # Liste pour stocker les messages d'action


        # Initialisation des unités des joueurs
        BASE_PATH_CARACTERS = 'assets/persos/'

        player_units = [
            Unit(BASE_PATH_CARACTERS + 'banane_pirate.png', 0, 0, 20, 5, 'player', 'Banane Pirate', speed=2, defense=3),
            Unit(BASE_PATH_CARACTERS + 'hamster_gangster.png', 1, 0, 15, 3, 'player', 'Tasse de Café', speed=2, defense=2),
            Unit(BASE_PATH_CARACTERS + 'jus_orange.png', 2, 0, 10, 4, 'player', 'Hamster Gangster', speed=3, defense=1)
        ]

        # Initialisation des unités ennemies
        enemy_units = [
            Enemy(BASE_PATH_CARACTERS + 'bonbon_contamine.png', 6, 6, 10, 3, 'Bonbon Contaminé', speed=1, defense=0),
            Enemy(BASE_PATH_CARACTERS + 'meringuich_toxique.png', 7, 6, 15, 2, 'Gâteau Zombie', speed=1, defense=2),
            Enemy(BASE_PATH_CARACTERS + 'sucette_volante.png', 5, 5, 8, 5, 'Sucette Volante', speed=2, defense=1)
        ]

        # Création des équipes
        self.player_team = Team('Player', player_units)
        self.enemy_team = Team('Enemy', enemy_units)

        # Génération de la carte
        self.generate_map()

    def generate_map(self):
        """
        Génère la carte du jeu avec des types de cases variées.
        """
        self.map = []
        for y in range(GRID_SIZE):
            row = []
            for x in range(GRID_SIZE):
                try:
                    # Définir le chemin de l'image en fonction du type de case
                    if (x + y) % 5 == 0:  # Zone infranchissable
                        image_path = "assets/cases/spatule.png"
                        tile_type = "infranchissable"
                    elif (x + y) % 4 == 0:  # Zone sucrée
                        image_path = "assets/cases/orange.png"
                        tile_type = "sucré"
                    elif (x + y) % 3 == 0:  # Zone huileuse
                        image_path = "assets/cases/huile.png"
                        tile_type = "huileuse"
                    elif (x + y) % 2 == 0:  # Zone mielleuse
                        image_path = "assets/cases/miel.png"
                        tile_type = "mielleuse"
                    else:  # Case normale
                        image_path = "assets/cases/normal.png"
                        tile_type = "normal"

                    # Vérifie si le fichier existe avant de l'utiliser
                    if not os.path.exists(image_path):
                        raise FileNotFoundError(f"Fichier manquant : {image_path}")

                    # Ajouter la case à la ligne
                    row.append(Tile(x, y, tile_type, image_path))

                except FileNotFoundError as e:
                    print(e)
                    pygame.quit()
                    exit()

            # Ajouter la ligne à la carte
            self.map.append(row)

    def apply_tile_effect(self, unit):
        current_tile = self.map[unit.y][unit.x]
        if current_tile.tile_type == "infranchissable":
            print(f"{unit.unit_type} ne peut pas passer ici !")
            return False
        elif current_tile.tile_type == "sucré":
            unit.health = min(unit.max_health, unit.health + 5)  # Régénération
            print(f"{unit.unit_type} régénère de la santé !")
        elif current_tile.tile_type == "huileuse":
            print(f"{unit.unit_type} glisse sur la case !")
            unit.move(random.choice([-1, 1]), random.choice([-1, 1]))  # Mouvement aléatoire
        elif current_tile.tile_type == "mielleuse":
            print(f"{unit.unit_type} est collé !")
            unit.speed = 0  # Immobilisé pour un tour
        return True


    def handle_player_turn(self):
        """
        Gère le tour du joueur.
        """
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
                                    self.message_timer = pygame.time.get_ticks() + 1500  # Afficher pendant 2 secondes

                                    if enemy.health <= 0:
                                        self.enemy_team.remove_dead_units()
                                        self.action_messages.append(f"{enemy.unit_type} est vaincu !")

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """
        Gère le tour des ennemis.
        """
        for enemy in self.enemy_team.units[:]:
            target = random.choice(self.player_team.units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                damage = max(0, enemy.attack_power - target.defense)
                enemy.attack(target)
                self.action_messages.append(
                    f"{enemy.unit_type} attaque {target.unit_type} pour {damage} dégâts !"
                )
                if target.health <= 0:
                    self.player_team.remove_dead_units()
                    self.action_messages.append(f"{target.unit_type} est vaincu !")

    def flip_display(self):
        self.screen.fill(BLACK)

        # Dessiner la carte
        for row in self.map:
            for tile in row:
                tile.draw(self.screen)

        # Dessiner les unités
        self.player_team.draw(self.screen)
        self.enemy_team.draw(self.screen)

        pygame.display.flip()

def main():
    """
    Fonction principale pour démarrer le jeu.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Le Monde Incroyable de l'Apocalypse")
    game = Game(screen)

    while True:
        game.handle_player_turn()
        if not game.enemy_team.is_defeated():
            game.handle_enemy_turn()
    
        if game.player_team.is_defeated() or game.enemy_team.is_defeated():
            # Déterminer le gagnant
            if game.player_team.is_defeated():
                winning_message = "Les zombibonbons ont pris le pouvoir sur le monde, c'est l'apocalypse !"
            else:
                winning_message = "Bravo ! Vous avez réussi à battre les zombibonbons, vous avez rétabli la paix dans le monde"

            # Ajuster la taille du texte avec la fonction
            font, text_surface = render_text_fit_to_screen(
                winning_message,
                None,  # Police par défaut
                WHITE,
                WIDTH - 20,  # Largeur maximale avec marges
                game.screen
            )

            # Centrer et afficher le texte
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            game.screen.fill(BLACK)  # Effacer l'écran
            game.screen.blit(text_surface, text_rect)  # Dessiner le texte
            pygame.display.flip()  # Mettre à jour l'écran

            # Attendre avant de quitter
            pygame.time.wait(3000)
            pygame.quit()
            exit()

if __name__ == "__main__":
    main()
