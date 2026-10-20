import json
from pathlib import Path

import pygame


def main():
    """Lance le jeu avec le titre défini dans manoir.json."""
    chemin_manoir = Path(__file__).with_name("manoir.json")
    with chemin_manoir.open(encoding="utf-8") as fichier:
        manoir = json.load(fichier)

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(manoir["titre"])
    joueur = pygame.Rect(385, 285, 30, 30)
    horloge = pygame.time.Clock()
    en_cours = True

    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    en_cours = False
                elif evenement.key in (pygame.K_LEFT, pygame.K_q):
                    joueur.x = max(0, joueur.x - 30)
                elif evenement.key in (pygame.K_RIGHT, pygame.K_d):
                    joueur.x = min(screen.get_width() - joueur.width, joueur.x + 30)
                elif evenement.key in (pygame.K_UP, pygame.K_z):
                    joueur.y = max(0, joueur.y - 30)
                elif evenement.key in (pygame.K_DOWN, pygame.K_s):
                    joueur.y = min(screen.get_height() - joueur.height, joueur.y + 30)

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (40, 100, 220), joueur)
        pygame.display.flip()
        horloge.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
