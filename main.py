import pygame
import Joueur

keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        Joueur.aller_gauche()
    if keys[pygame.K_d]:
        Joueur.aller_droite()
    if keys[pygame.K_z]:
        Joueur.aller_haut()
    if keys[pygame.K_s]:
        Joueur.aller_bas()