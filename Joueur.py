import pygame
class joueur:
    """Représente un joueur dans le jeu."""

    def __init__(self, nom, largeur=10, hauteur=10):
        """Initialise un joueur avec un nom."""
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur

    

    def aller_gauche(self):
        """Déplace le joueur vers la gauche."""
        

    def aller_droite(self):
        """Déplace le joueur vers la droite."""
        

    def aller_haut(self):
        """Déplace le joueur vers le haut."""
        
    def aller_bas(self):
        """Déplace le joueur vers le bas."""

        
    def __str__(self):
        return f"{self.nom} (Largeur: {self.largeur}, Hauteur: {self.hauteur})"