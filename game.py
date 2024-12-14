import pygame
import random
import json

from unit import *
from tile import *
from map import *

class Game:
    """
    Classe pour représenter le jeu.
    """

    def __init__(self, screen):
        self.screen = screen
        self.current_message = ""
        self.message_timer = 0
        self.action_messages = []
        self.load_map_from_json("map_config.json")  # Charge la carte
        self.generate_map()  # Génère la carte

        # Charger les propriétés de la carte à partir du fichier JSON
        self.map = Map("map_config.json")  # Chargement via la classe Map

        # Initialisation des unités
        BASE_PATH_CARACTERS = 'assets/persos/'

        player_units = [
            HamsterGangster(1,2),
            JusOrange(0,3),
            BananePlanteur(0,2)
        ]
        player_units[0].sp = 6
        player_units[1].sp = 6
        player_units[2].sp = 6

        enemy_units = [
            BonbonContaminé(19,18),
            MeringuichToxique(19,19),
            SucetteVolante(18,19)
        ]

        enemy_units[0].sp = 6
        enemy_units[1].sp = 6
        enemy_units[2].sp = 6

        self.player_team = Team('Player', player_units)
        self.enemy_team = Team('Enemy', enemy_units)

        # Génération de la carte interactive
        self.generate_map()

    def show_start_screen(self):
        # Charger une image de fond
        start_image = pygame.image.load("assets/start_screen.png")
        start_image = pygame.transform.scale(start_image, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(start_image, (0, 0))

        # Définir les polices
        font_title_large = pygame.font.Font(None, 72)
        font_title_small = pygame.font.Font(None, 72)
        font_text = pygame.font.Font(None, 48)

        # Texte et couleurs
        title_text_top = font_title_large.render(" Le Monde Incroyable de Pierrot:", True, WHITE)
        title_text_bottom = font_title_small.render("L'Apocalypse", True, WHITE)
        play_text = font_text.render("Press ENTER to Play", True, WHITE)
        quit_text = font_text.render("Press Q to Quit", True, WHITE)
        instructions_text = font_text.render("Press I for Instructions", True, WHITE)

        # Rectangle du titre
        total_width = max(title_text_top.get_width(), title_text_bottom.get_width())
        total_height = title_text_top.get_height() + title_text_bottom.get_height() + 10
        title_rect = pygame.Rect(
            (self.screen.get_width() // 2 - total_width // 2),
            100,
            total_width + 20,
            total_height + 20
        )

        # Rectangles pour les autres textes
        play_rect = play_text.get_rect(center=(self.screen.get_width() // 2, 300)).inflate(20, 10)
        quit_rect = quit_text.get_rect(center=(self.screen.get_width() // 2, 400)).inflate(20, 10)
        instructions_rect = instructions_text.get_rect(center=(self.screen.get_width() // 2, 500)).inflate(20, 10)

        rect_color = (100, 100, 200)
        animation_offset_title = 0
        animation_offset_play = 0
        animation_offset_quit = 0
        animation_offset_instructions = 0

        animation_direction_title = 1
        animation_direction_play = 1
        animation_direction_quit = 1
        animation_direction_instructions = 1

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_i:
                        self.show_instructions()

            # Animation
            animation_offset_title += animation_direction_title
            animation_offset_play += animation_direction_play
            animation_offset_quit += animation_direction_quit
            animation_offset_instructions += animation_direction_instructions

            if abs(animation_offset_title) > 5:
                animation_direction_title *= -1
            if abs(animation_offset_play) > 3:
                animation_direction_play *= -1
            if abs(animation_offset_quit) > 3:
                animation_direction_quit *= -1
            if abs(animation_offset_instructions) > 3:
                animation_direction_instructions *= -1

            # Affichage de l'écran de garde
            self.screen.blit(start_image, (0, 0))

            # Dessiner le rectangle du titre
            title_rect_animated = title_rect.copy()
            title_rect_animated.y += animation_offset_title
            pygame.draw.rect(self.screen, rect_color, title_rect_animated)
            pygame.draw.rect(self.screen, (255, 255, 255), title_rect_animated, 3)
            self.screen.blit(title_text_top, (self.screen.get_width() // 2 - title_text_top.get_width() // 2, title_rect_animated.y + 10))
            self.screen.blit(title_text_bottom, (self.screen.get_width() // 2 - title_text_bottom.get_width() // 2, title_rect_animated.y + title_text_top.get_height() + 15))

            # Dessiner les rectangles des autres textes
            play_rect_animated = play_rect.copy()
            play_rect_animated.y += animation_offset_play
            pygame.draw.rect(self.screen, rect_color, play_rect_animated)
            pygame.draw.rect(self.screen, (255, 255, 255), play_rect_animated, 2)
            self.screen.blit(play_text, (play_rect_animated.x + 10, play_rect_animated.y + 5))

            quit_rect_animated = quit_rect.copy()
            quit_rect_animated.y += animation_offset_quit
            pygame.draw.rect(self.screen, rect_color, quit_rect_animated)
            pygame.draw.rect(self.screen, (255, 255, 255), quit_rect_animated, 2)
            self.screen.blit(quit_text, (quit_rect_animated.x + 10, quit_rect_animated.y + 5))

            instructions_rect_animated = instructions_rect.copy()
            instructions_rect_animated.y += animation_offset_instructions
            pygame.draw.rect(self.screen, rect_color, instructions_rect_animated)
            pygame.draw.rect(self.screen, (255, 255, 255), instructions_rect_animated, 2)
            self.screen.blit(instructions_text, (instructions_rect_animated.x + 10, instructions_rect_animated.y + 5))

            # Mettre à jour l'écran
            pygame.display.flip()
            pygame.time.delay(30)

    def show_end_screen(self, winner):
        """
        Affiche la page de fin avec le vainqueur.
        """
        self.screen.fill((0, 0, 0))  # Fond noir

        # Définir les polices
        font_title = pygame.font.Font(None, 72)
        font_text = pygame.font.Font(None, 48)

        # Texte du vainqueur
        title_text = f"Félicitations à l'équipe {winner} !" if winner != "Draw" else "C'est un match nul !"
        title_surface = font_title.render(title_text, True, (255, 255, 255))

        # Texte d'options
        replay_text = font_text.render("Appuyez sur R pour rejouer", True, (255, 255, 255))
        quit_text = font_text.render("Appuyez sur Q pour quitter", True, (255, 255, 255))

        # Positionner les textes au centre de l'écran
        title_x = self.screen.get_width() // 2 - title_surface.get_width() // 2
        title_y = self.screen.get_height() // 3

        replay_x = self.screen.get_width() // 2 - replay_text.get_width() // 2
        replay_y = title_y + 100

        quit_x = self.screen.get_width() // 2 - quit_text.get_width() // 2
        quit_y = replay_y + 50

        # Afficher les textes
        self.screen.blit(title_surface, (title_x, title_y))
        self.screen.blit(replay_text, (replay_x, replay_y))
        self.screen.blit(quit_text, (quit_x, quit_y))

        pygame.display.flip()

        # Attente pour rejouer ou quitter
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Rejouer
                        self.reset_game()  # Réinitialiser le jeu
                        waiting = False
                    elif event.key == pygame.K_q:  # Quitter
                        pygame.quit()
                        exit()

    def show_instructions(self):
        self.screen.fill((0, 0, 0))  # Fond noir
        font = pygame.font.SysFont(None, 36)

        instructions = [
            "Comment jouer :",
            "- Joueur 1 : Déplacez votre personnage avec les Z, Q, S, D.",
            "- Appuyez sur ESPACE pour valider votre déplacement.",
            "- Joueur 2 : Déplacez votre personnage avec les flèches directionnelles.",
            "- Appuyez sur ENTRER pour valider votre déplacement.",
            "- Choisissez une attaque ou une action spéciale en suivant les touches indiquées.",
            "- Battez les zombibonbons pour gagner !",
            "",
            "Press M to return to the main menu.",
            "Press ESCAPE to return to the main anytime during the game."
        ]

        y_offset = 100
        for line in instructions:
            text_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.screen.get_width() // 2 - text_surface.get_width() // 2, y_offset))
            y_offset += 50

        pygame.display.flip()

        # Attente pour retourner au menu principal
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: 
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_m:  # Retour au menu
                        waiting = False
        self.show_start_screen()

    def is_position_occupied(self, x, y, actual_unit):
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
            if actual_tile.tile_type == 'eau' and actual_unit.unit_type not in actual_tile.allowed_characters :
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
                    image_path=None
                    tile_row.append(GenericTile(x, y, tile_type, is_walkable,image_path))
                if tile_type == 'miel':
                    image_path='assets/cases/miel.png'
                    is_walkable = True
                    tile_row.append(Miel(x, y, tile_type, is_walkable, image_path))
                if tile_type == 'eau':
                    image_path='assets/cases/eau.png'
                    is_walkable = True
                    tile_row.append(Eau(x, y, tile_type, is_walkable,image_path))
                if tile_type == 'vitesse':
                    image_path='assets/cases/eclair.png'
                    is_walkable = True
                    tile_row.append(Vitesse(x, y, tile_type, is_walkable,image_path))
                if tile_type == 'orange':
                    image_path='assets/cases/orange.png'
                    is_walkable = True
                    tile_row.append(Orange(x, y, tile_type, is_walkable,image_path))
                elif tile_type == "normal":  # Case normale
                    image_path=None
                    is_walkable = True
                    tile_row.append(GenericTile(x, y, tile_type, is_walkable,image_path))

            self.map.append(tile_row)

        # Dessiner les différents types de tiles 
        for i in range(GRID_SIZE):  
            for j in range(GRID_SIZE):  # Remplace GRID_SIZE par self.height
                tile = self.map[i][j]
                tile.draw(self.screen)  # Dessiner la tile seulement si elle existe
        # Mettre à jour l'affichage
        pygame.display.flip()

    def reset_game(self):
        """
        Réinitialise le jeu et affiche l'écran de démarrage.
        """
        print("Réinitialisation du jeu...")
        self.load_map_from_json("map_config.json")  # Recharge la carte
        self.generate_map()  # Régénère les objets Tile

        # Réinitialise les équipes et unités
        player_units = [
            HamsterGangster(1, 2),
            JusOrange(0, 3),
            BananePlanteur(0, 2)
        ]
        player_units[0].sp = 6
        player_units[1].sp = 6
        player_units[2].sp = 6

        enemy_units = [
            BonbonContaminé(19, 18),
            MeringuichToxique(19, 19),
            SucetteVolante(18, 19)
        ]
        enemy_units[0].sp = 6
        enemy_units[1].sp = 6
        enemy_units[2].sp = 6

        self.player_team = Team('Player', player_units)
        self.enemy_team = Team('Enemy', enemy_units)

        self.show_start_screen()  # Revient à l'écran de démarrage
    
    def handle_player_turn(self):
        for selected_unit in self.player_team.units:
            # Définir le personnage comme actif
            selected_unit.is_active = True
            has_acted = False
            selected_unit.moves = selected_unit.speed
            selected_unit.is_selected = True
            self.action_messages.append(f" ")
            self.action_messages.append(f"C'est au tour de {selected_unit.unit_type} !")
            info_deplacement = f"{selected_unit.unit_type} a {selected_unit.moves} déplacements restants."
            self.action_messages.append(info_deplacement)
            self.action_messages.append(f"Appuyez sur ESPACE pour confirmer votre déplacement")
            index_of_move = self.action_messages.index(info_deplacement)
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
                        if event.key == pygame.K_ESCAPE:
                            self.reset_game()
                            return
                        elif event.key == pygame.K_q:
                            dx = -1
                        elif event.key == pygame.K_d:
                            dx = 1
                        elif event.key == pygame.K_z:
                            dy = -1
                        elif event.key == pygame.K_s:
                            dy = 1

                        # Vérifier si le mouvement est valide
                        new_x, new_y = selected_unit.x + dx, selected_unit.y + dy
                        if (new_x, new_y) in self.get_reachable_tiles(selected_unit):
                            selected_unit.move(dx, dy,self)
                            if selected_unit.moves > 0 : selected_unit.moves -= 1 
                            self.action_messages[index_of_move]= (f"{selected_unit.unit_type} a {selected_unit.moves} déplacements restants.")
                            self.flip_display()

                        # Effectuer une attaque
                        if event.key == pygame.K_SPACE or selected_unit.moves == 0:  #ceci marque la fin du deplacement
                            #self.action_messages = [] 
                            # tile_rect = pygame.Rect(800, 10, CELL_SIZE * 12, CELL_SIZE * 5)
                            # pygame.draw.rect(self.screen, BLACK, tile_rect)
                            # pygame.display.flip()
                            #self.flip_display()
                            selected_unit.moves = 0
                            choice = -1
                            # tile_rect = pygame.Rect(800, 10, CELL_SIZE * 10, CELL_SIZE * 5)
                            # pygame.draw.rect(self.screen, BLACK, tile_rect)
                            # pygame.display.flip()
                            self.action_messages.append(f" ")
                            self.action_messages.append("Choisissez une attaque :")
                            self.action_messages.append(f"A : ne rien faire")
                            self.action_messages.append(f"E : attaque simple")
                            self.action_messages.append(f"R : attaque spéciale")
                            self.action_messages.append(f"T : attaque légendaire")
                            self.action_messages.append(f" ")
                            self.flip_display()                          

                            while (choice == -1):
                                for ch in pygame.event.get():
                                    if ch.type == pygame.KEYDOWN:                                        
                                        if (ch.key == pygame.K_a):
                                            choice = 0
                                        if ch.key == pygame.K_e :
                                            choice = 1
                                        if ch.key == pygame.K_r:
                                            if(selected_unit.sp < 4):
                                                self.action_messages.append(f"{selected_unit.unit_type} n'a pas cumulé assez de points spéciaux !")
                                                break
                                            choice = 2
                                        if ch.key == pygame.K_t:
                                            if (selected_unit.sp < 6):
                                                self.action_messages.append(f"{selected_unit.unit_type} n'a pas cumulé assez de points spéciaux !")
                                                break
                                            choice = 3
                                        if ch.key == pygame.K_ESCAPE:
                                            self.reset_game()
                                            return
                                        self.flip_display()
                            self.action_messages = [] 
                            tile_rect = pygame.Rect(800, 10, CELL_SIZE * 12, CELL_SIZE * 5)
                            pygame.draw.rect(self.screen, BLACK, tile_rect)
                            pygame.display.flip()

                            if (choice == 0):
                                self.action_messages.append(f"{selected_unit.unit_type} a décidé de ne rien faire !")
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
                                    selected_unit.use_special(self.player_team.units,self)
                                    self.action_messages.append(f"{selected_unit.unit_type} a lancé sa bomba !")
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
                                selected_unit.use_special2(self)
                            has_acted = True
                            selected_unit.is_selected = False
                            selected_unit.is_active = False 
                            self.flip_display()  # Mise à jour l'écran

    def handle_player2_turn(self):
        for selected_unit in self.enemy_team.units:
            # Définir le personnage comme actif
            selected_unit.is_active = True
            has_acted = False
            selected_unit.moves = selected_unit.speed
            selected_unit.is_selected = True
            self.action_messages.append(f" ")
            self.action_messages.append(f"C'est au tour de {selected_unit.unit_type} !")
            info_deplacement = f"{selected_unit.unit_type} a {selected_unit.moves} déplacements restants."
            self.action_messages.append(info_deplacement)
            self.action_messages.append(f"Appuyez sur ENTRER pour confirmer votre déplacement")
            index_of_move = self.action_messages.index(info_deplacement)
            self.flip_display2()
            if (selected_unit.sp < 6):
                selected_unit.sp += 1
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_ESCAPE:
                            self.reset_game()
                            return
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
                            selected_unit.move(dx, dy,self)
                            if selected_unit.moves > 0 : selected_unit.moves -= 1 
                            self.action_messages[index_of_move]= (f"{selected_unit.unit_type} a {selected_unit.moves} déplacements restants.")
                            self.flip_display2()

                        # Effectuer une attaque
                        if event.key == pygame.K_RETURN or selected_unit.moves == 0:  #ceci marque la fin du deplacement
                            self.action_messages = [] 
                            tile_rect = pygame.Rect(800, 10, CELL_SIZE * 12, CELL_SIZE * 5)
                            pygame.draw.rect(self.screen, BLACK, tile_rect)
                            pygame.display.flip()
                            self.flip_display2()
                            selected_unit.moves = 0
                            choice = -1
                            tile_rect = pygame.Rect(800, 10, CELL_SIZE * 10, CELL_SIZE * 5)
                            pygame.draw.rect(self.screen, BLACK, tile_rect)
                            pygame.display.flip()
                            self.action_messages.append(f" ")
                            self.action_messages.append("Choisissez une attaque :")
                            self.action_messages.append(f"U : ne rien faire")
                            self.action_messages.append(f"I : attaque simple")
                            self.action_messages.append(f"O : attaque spéciale")
                            self.action_messages.append(f"P : attaque légendaire")
                            self.action_messages.append(f" ")
                            self.flip_display2()                          

                            while (choice == -1):
                                for ch in pygame.event.get():
                                    if ch.type == pygame.KEYDOWN:                                        
                                        if (ch.key == pygame.K_u):
                                            choice = 0
                                        if ch.key == pygame.K_i :
                                            choice = 1
                                        if ch.key == pygame.K_o:
                                            if(selected_unit.sp < 4):
                                                self.action_messages.append(f"{selected_unit.unit_type} n'a pas cumulé assez de points spéciaux !")
                                                break
                                            choice = 2
                                        if ch.key == pygame.K_p:
                                            if (selected_unit.sp < 6):
                                                self.action_messages.append(f"{selected_unit.unit_type} n'a pas cumulé assez de points spéciaux !")
                                                break
                                            choice = 3
                                        if ch.key == pygame.K_ESCAPE:
                                            self.reset_game()
                                            return
                                        self.flip_display2()
                            self.action_messages = [] 
                            tile_rect = pygame.Rect(800, 10, CELL_SIZE * 12, CELL_SIZE * 5)
                            pygame.draw.rect(self.screen, BLACK, tile_rect)
                            pygame.display.flip()

                            if (choice == 0):
                                self.action_messages.append(f"{selected_unit.unit_type} a décidé de ne rien faire !")
                                if selected_unit.sp < 6:
                                    selected_unit.sp += 1
                            elif (choice == 1): #attaque de base
                                for enemy in self.player_team.units:
                                    if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                        damage = max(0, selected_unit.attack_power - enemy.defense)
                                        selected_unit.attack(enemy, False, 1)
                                        self.action_messages.append(f"{selected_unit.unit_type} attaque {enemy.unit_type} pour {damage} dégâts !")
                                        self.message_timer = pygame.time.get_ticks() + 3000
                                        if enemy.health <= 0:
                                            self.player_team.remove_dead_units()
                                            self.action_messages.append(f"{enemy.unit_type} est vaincu !")
                            elif (choice == 2):#attaque speciale 1
                                selected_unit.sp -= 4
                                if selected_unit.unit_type == "Jus orange":
                                    selected_unit.use_special(self.enemy_team.units,self)
                                    self.action_messages.append(f"{enemy.unit_type} a lancé sa bomba !")
                                else :
                                    for enemy in self.player_team.units:
                                        if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                            damage = max(0, selected_unit.attack_power - enemy.defense)
                                            #selected_unit.use_special(enemy, False, 1)
                                            selected_unit.use_special(enemy)
                                            self.action_messages.append(f"{selected_unit.unit_type} attaque {enemy.unit_type} pour {damage} dégâts !")
                                            self.message_timer = pygame.time.get_ticks() + 3000
                                            if enemy.health <= 0:
                                                self.player_team.remove_dead_units()
                                                self.action_messages.append(f"{enemy.unit_type} est vaincu !")
                            elif (choice == 3): #attaque speciale 2
                                selected_unit.sp -= 6
                                selected_unit.use_special2(self)
                            has_acted = True
                            selected_unit.is_selected = False
                            selected_unit.is_active = False 
                            self.flip_display2()  # Mise à jour l'écran
              
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
                        not self.is_position_occupied(new_x, new_y, unit) and 
                        self.map[new_y][new_x].walkable):
                        reachable_tiles.append((new_x, new_y))
        return reachable_tiles
    
    def draw_game_console(self):
        """
        Affiche les messages d'action et les informations de l'unité sélectionnée dans le game log.
        """
        # Zone noire pour le log
        pygame.draw.rect(self.screen, (0, 0, 0), (GRID_SIZE * CELL_SIZE, 0, LOG_WIDTH, HEIGHT))

        font = pygame.font.SysFont(None, 24)
        line_spacing = 24
        y_offset = 20  # Décalage initial (descend tout le contenu du log)

        # Afficher les messages d'action
        for message in self.action_messages[-6:]:  # Limiter à 6 messages pour laisser de la place
            text_surface = font.render(message, True, (255, 255, 255))
            self.screen.blit(text_surface, (GRID_SIZE * CELL_SIZE + 10, y_offset))
            y_offset += line_spacing

        # Ajouter un espace avant la section info
        y_offset = 250

        # Dessiner une bordure orange autour de la section info
        pygame.draw.rect(self.screen, (255, 165, 0), (GRID_SIZE * CELL_SIZE + 5, y_offset - 10, LOG_WIDTH - 10, y_offset + 70), 3)

        # Afficher les informations de l'unité sélectionnée
        for unit in self.player_team.units + self.enemy_team.units:
            if unit.is_selected:
                # Dessiner une image agrandie pour l'unité
                log_image_size = (80, 80)  # Taille agrandie de l'image
                enlarged_image = pygame.transform.scale(unit.image, log_image_size)
                image_x = GRID_SIZE * CELL_SIZE + 10
                self.screen.blit(enlarged_image, (image_x, y_offset))

                # Afficher le nom aligné à droite de l'image
                name_surface = font.render(f"{unit.unit_type}", True, (255, 153, 153))
                name_x = image_x + log_image_size[0] + 10
                self.screen.blit(name_surface, (name_x, y_offset))

                # Dessiner les barres de vie et SP alignées verticalement
                bar_x = name_x  # Position des barres alignées avec le nom
                bar_y = y_offset + name_surface.get_height() + 10  # Sous le nom

                # Barre de vie
                max_bar_width = 100
                health_bar_width = int(max_bar_width * (unit.health / unit.max_health))
                pygame.draw.rect(self.screen, RED, (bar_x, bar_y, max_bar_width, 10))  # Barre rouge (fond)
                pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, health_bar_width, 10))  # Barre verte (actuelle)

                # Barre SP (sous la barre de vie)
                sp_bar_width = int(max_bar_width * (unit.sp / 6))  # 6 est le max de SP
                sp_bar_y = bar_y + 15  # Décalage vertical sous la barre de vie
                pygame.draw.rect(self.screen, (211,211,211), (bar_x, sp_bar_y, max_bar_width, 10))  # Barre noire (fond)
                pygame.draw.rect(self.screen, BLUE, (bar_x, sp_bar_y, sp_bar_width, 10))  # Barre bleue (actuelle)

                # Passer à la ligne suivante après l'image et les barres
                y_offset += log_image_size[1] + 20

                # Afficher les statistiques restantes sous l'image
                details = unit.get_details().split("\n")
                for line in details:
                    if "Vitesse:" in line or "Defense:" in line:
                        text_surface = font.render(line, True, BLUE)  # Texte bleu pour vitesse et défense
                    elif "Attaques et degats:" in line:
                        text_surface = font.render(line, True, RED)  # Texte bleu pour vitesse et défense
                    else:
                        text_surface = font.render(line, True, (211, 211, 211))  # Texte gris clair pour le reste
                    self.screen.blit(text_surface, (GRID_SIZE * CELL_SIZE + 10, y_offset))
                    y_offset += line_spacing


                break  # Une seule unité sélectionnée à la fois

        pygame.display.flip()

    def draw_tile_descriptions(self):
        """
        Affiche les descriptions des cases spéciales en bas de l'écran avec leurs images.
        """
        font = pygame.font.SysFont(None, 24)
        descriptions = [
            {
                "name": "Miel",
                "effect": "Bloque les unités et inflige 2 dégâts.",
                "image": "assets/cases/miel.png"
            },
            {
                "name": "Orange",
                "effect": "Restaure aléatoirement entre 1 et 4 HP.",
                "image": "assets/cases/orange.png"
            },
            {
                "name": "Eau",
                "effect": "Traversable par jus d\'orange et sucette volante.",
                "image": "assets/cases/eau.png"
            },
            {
                "name": "Vitesse",
                "effect": "Modifie la vitesse entre -1 et +2.",
                "image": "assets/cases/eclair.png"
            }
        ]

        # Zone noire pour le fond
        pygame.draw.rect(self.screen, (0, 0, 0), (800, HEIGHT - 150, WIDTH, 150))

        x_offset = 810
        y_offset = HEIGHT - 200  # Position initiale verticale
        image_size = (40, 40)  # Taille des images des cases

        for desc in descriptions:
            # Charger et afficher l'image
            image = pygame.image.load(desc["image"])
            image = pygame.transform.scale(image, image_size)
            self.screen.blit(image, (x_offset, y_offset))

            # Afficher le texte de description
            text_surface = font.render(f"{desc['name']}: {desc['effect']}", True, (255, 255, 255))
            self.screen.blit(text_surface, (x_offset + image_size[0] + 10, y_offset + 10))

            # Passer à la ligne suivante
            y_offset += 50

        pygame.display.flip()

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

        # Dessiner les différents types de tiles 
        for i in range(GRID_SIZE):  
            for j in range(GRID_SIZE):  # Remplace GRID_SIZE par self.height
                tile = self.map[i][j]
                tile.draw(self.screen)  # Dessiner la tile seulement si elle existe

        # Dessiner les unités
        self.player_team.draw(self.screen)
        self.enemy_team.draw(self.screen)

        # Dessiner la console à droite (fond noir)
        self.draw_game_console()

        # Afficher les descriptions des cases spéciales avec images
        self.draw_tile_descriptions()

        # Mettre à jour l'affichage
        pygame.display.flip()
 
    def flip_display2(self):   #pour tour j2
        # Dessiner l'image de fond
        self.screen.blit(self.background_image, (0, 0))

        # Dessiner les différents types de tiles 
        for i in range(GRID_SIZE):  
            for j in range(GRID_SIZE):  
                tile = self.map[i][j]
                tile.draw(self.screen)  # Dessiner la tile seulement si elle existe

        # Dessiner les tuiles accessibles pour l'unité sélectionnée
        for unit in self.enemy_team.units:
            if unit.is_selected:
                reachable_tiles = self.get_reachable_tiles(unit)
                for x, y in reachable_tiles:
                    tile_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (200,10,0), tile_rect)  # Remplissage rouge 
                    
        # Dessiner les unités
        self.player_team.draw(self.screen)
        self.enemy_team.draw(self.screen)

        # Dessiner la console à droite (fond noir)
        self.draw_game_console()

        # Afficher les descriptions des cases spéciales avec images
        self.draw_tile_descriptions()

        # Mettre à jour l'affichage
        pygame.display.flip()



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Le Monde Incroyable de Pierrot : l'Apocalypse")

    # Charger et jouer la musique
    pygame.mixer.init()
    pygame.mixer.music.load("assets/game_music.mp3")  # Remplacez par le chemin de votre fichier audio
    pygame.mixer.music.set_volume(0.5)  # Ajustez le volume (0.0 à 1.0)
    pygame.mixer.music.play(-1)  # Lecture en boucle infinie

    # Afficher la page de garde
    game = Game(screen)
    game.show_start_screen()

    while True:
        game.handle_player_turn()
        if not game.enemy_team.is_defeated():
            game.handle_player2_turn()
        if game.player_team.is_defeated() or game.enemy_team.is_defeated():
            # Gagnant
            if game.player_team.is_defeated():
                winner = "Player2"
q
            else:
                winner = "Player1"

            # Afficher l'écran de fin
            game.show_end_screen(winner)

if __name__ == "__main__":
    main()
