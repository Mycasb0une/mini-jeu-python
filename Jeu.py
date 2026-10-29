
def inventaire_objets(joueur):
    """Retourne une liste des objets dans l'inventaire du joueur.
    :param: joueur: Le joueur dont on veut connaître l'inventaire.
    
    :return: Une liste des objets dans l'inventaire du joueur.
    """
    return list(joueur.inventaire)


def deposer_objet(joueur, objet):
    """Essaie de déposer un objet de l'inventaire du joueur dans la pièce.
     et l'ajoute à la salle.
    :param: joueur: Le joueur qui tente de déposer l'objet
            objet: L'objet que le joueur tente de déposer
    
    :precondition: L'objet doit être dans l'inventaire du joueur.
    
    :return: Un message indiquant le résultat de l'action.

    :effet de bord: Oui
    """
    poids_actuel = sum(objet.poids for objet in joueur.inventaire)

    if objet not in joueur.inventaire:
        return "Vous n'avez pas cet objet dans votre inventaire."

    joueur.inventaire.remove(objet)
    joueur.piece.objets.append(objet)
    poids_actuel = sum(objet.poids for objet in joueur.inventaire)
    return f"Vous avez déposé {objet.nom}."


def ramasser_objet(joueur, objet):
    """Essaie de ramasser un objet dans la pièce et l'ajoute à l'inventaire du joueur.
    :param: joueur: Le joueur qui tente de ramasser l'objet
            objet: L'objet que le joueur tente de ramasser
    
    :precondition: L'objet doit être dans la pièce où se trouve le joueur.
    
    :return: Un message indiquant le résultat de l'action.

    :effet de bord: Oui
    """

    if objet.particularite == "fixe":
            return "Vous ne pouvez pas ramasser cet objet, il est fixé."
        
    poids_actuel = sum(objet.poids for objet in joueur.inventaire)

    if objet not in joueur.piece.objets:
        return "Cet objet n'est pas dans cette pièce."
    
    if poids_actuel + objet.poids > joueur.capacite:
        return "Vous ne pouvez pas ramasser cet objet, il est trop lourd."

    joueur.inventaire.add(objet)
    joueur.piece.objets.remove(objet)
    poids_actuel += objet.poids
    return f"Vous avez ramassé {objet.nom}."