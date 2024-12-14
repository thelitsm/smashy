import pygame
import json

from tile import *



class Map:
    def __init__(self, file_path):
        self.tiles = []
        self.load_map_from_json(file_path)

    def load_map_from_json(self, file_path):
        with open(file_path, "r") as file:
            map_matrix = json.load(file)["map"]
        for y, row in enumerate(map_matrix):
            tile_row = []
            for x, tile_type in enumerate(row):
                if tile_type == "mur":
                    tile_row.append(GenericTile(x, y, "mur", False))  # Pas d'image pour les murs
                elif tile_type == "miel":
                    tile_row.append(Miel(x, y, "miel", True, "assets/cases/miel.png"))
                elif tile_type == "eau":
                    tile_row.append(Eau(x, y, "eau", True, "assets/cases/eau.png"))
                elif tile_type == "vitesse":
                    tile_row.append(Vitesse(x, y, "vitesse", True, "assets/cases/eclair.png"))
                elif tile_type == "orange":
                    tile_row.append(Orange(x, y, "orange", True, "assets/cases/orange.png"))
                else:  # Case normale
                    tile_row.append(GenericTile(x, y, "normal", True))
            self.tiles.append(tile_row)

    def generate_map(self):
        self.map = []  # Initialiser une nouvelle carte

        # Mise en place de la carte en arrière-plan
        self.background_image = pygame.image.load('assets/game_map.png')
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH - LOG_WIDTH, HEIGHT))

        # Construit les objets Tile en fonction des données de `Map`
        for y, row in enumerate(self.map.tiles):  # Remplacez `self.map_matrix` par `self.map.tiles`
            tile_row = []
            for x, tile in enumerate(row):
                tile_row.append(tile)  # Ajoute les tuiles existantes
            self.map.append(tile_row)

        # Dessiner les différents types de tiles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = self.map[i][j]
                tile.draw(self.screen)  # Dessine la tuile sur l'écran

        pygame.display.flip()  # Mettre à jour l'affichage

    def get_tile(self, x, y):
        return self.tiles[y][x]