import pygame
import random

# Fonction utilitaire pour ajuster le texte
def render_text_fit_to_screen(text, font_name, color, max_width, screen):
    """
    Rend le texte ajusté à la largeur maximale de l'écran.
    """
    font_size = 48  # Taille initiale de la police
    while font_size > 10:  # Minimum de 10 pour la lisibilité
        font = pygame.font.SysFont(font_name, font_size)
        text_surface = font.render(text, True, color)
        if text_surface.get_width() <= max_width:
            return font, text_surface
        font_size -= 2  # Réduire progressivement la taille de la police
    return font, text_surface
