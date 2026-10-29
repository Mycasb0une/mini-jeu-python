class joueur:
    """Représente un joueur dans le jeu."""

    def __init__(self, nom, piece, capacite):
        """Initialise un joueur avec un nom et sa pièce de départ."""
        self.nom = nom
        self.piece = piece
        self.capacite = capacite
        self.inventaire = set()
        self.inventaire_capacite = capacite

    

    def aller_ouest(self):
        """Déplace le joueur vers la gauche."""
        return self.aller("ouest")

    def aller_est(self):
        """Déplace le joueur vers la droite."""
        return self.aller("est")

    def aller_nord(self):
        """Déplace le joueur vers le haut."""
        return self.aller("nord")

    def aller_sud(self):
        """Déplace le joueur vers le bas."""
        return self.aller("sud")

    def aller(self, direction):
        """Tente de déplacer le joueur dans une direction."""
        if self.piece is None:
            raise ValueError("Le joueur doit avoir une pièce de départ.")

        nouvelle_piece, message = self.piece.aller(
            direction, self.inventaire
        )
        if nouvelle_piece is not None:
            self.piece = nouvelle_piece
        return nouvelle_piece is not None, message

    def __str__(self):
        return f"{self.nom} est un joueur."