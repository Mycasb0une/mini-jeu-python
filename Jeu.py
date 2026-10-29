import Carte


def ramasser_objet(joueur, objet):
    """Essaie d'ajouter un objet portable à l'inventaire du joueur et
    le retire de la salle.
    :param: joueur: Le joueur qui tente de ramasser l'objet
            objet: L'objet que le joueur tente de ramasser
    
    :precondition: L'objet doit être dans la pièce du joueur 
    et ne pas dépasser la capacité de l'inventaire.
    
    :return: Un message indiquant le résultat de l'action.

    :effet de bord: Oui
    """
    if objet.particularite == "fixe":
        return "Cet objet est fixé et ne peut pas être ramassé."

    if objet not in joueur.piece.objets:
        return "Cet objet n'est pas dans cette pièce."

    poids_actuel = sum(item.poids for item in joueur.inventaire)
    if poids_actuel + objet.poids > joueur.capacite:
        return "Cet objet est trop lourd pour être ramassé."

    joueur.piece.objets.remove(objet)
    joueur.inventaire.add(objet)
    return f"Vous avez ramassé {objet.nom}."
