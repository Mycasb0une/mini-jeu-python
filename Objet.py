class objet:

    def __init__(
        self, nom, description, poids, particularite=None, identifiant=None
    ):
        self.nom = nom
        self.description = description
        self.poids = poids
        self.particularite = particularite
        self.identifiant = identifiant

    def placement_dans_piece(self, piece):
        """Place l'objet dans une pièce donnée."""
        if not hasattr(piece, "objets"): #hasattr vérifie si l'objet a un attribut spécifique
            piece.objets = []
        piece.objets.append(self)
