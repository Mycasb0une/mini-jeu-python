import Objet


def possede_objet(inventaire, identifiant):
    """Vérifie si l'inventaire contient un objet identifié par son identifiant."""
    return any(
        getattr(objet, "identifiant", objet) == identifiant
        for objet in inventaire
    )


class piece:
    
    def __init__(self, identifiant, donnees):
        self.identifiant = identifiant
        self.name = donnees["nom"]
        self.description = donnees.get("description", "")
        self.sorties = {}
        self.objets = []

    def aller(self, direction, inventaire):
        sortie = self.sorties.get(direction)
        if sortie is None:
            return None, f"Il n'y a pas de sortie vers le {direction}."

        objet_requis = sortie.get("requiert")
        if objet_requis is not None and not possede_objet(
            inventaire, objet_requis
        ):
            return None, sortie.get(
                "bloquee", "Le passage est bloqué."
            )

        return sortie["piece"], sortie.get("ouverture", "")

    def sorties_accessibles(self, inventaire):
        return {
            direction: sortie["piece"]
            for direction, sortie in self.sorties.items()
            if sortie["requiert"] is None
            or possede_objet(inventaire, sortie["requiert"])
        }

    def sorties_inaccessibles(self, inventaire):
        return {
            direction: sortie["piece"]
            for direction, sortie in self.sorties.items()
            if sortie["requiert"] is not None
            and not possede_objet(inventaire, sortie["requiert"])
        }

    
    def __str__(self):
        return self.name


class carte:
    def __init__(self, scenario):
        salles = scenario["salles"]
        self.pieces = {
            identifiant: piece(identifiant, donnees)
            for identifiant, donnees in salles.items()
        }
        self.objets = {
            identifiant: Objet.objet(
                donnees["nom"],
                donnees.get("description", ""),
                donnees.get("poids", 0),
                "fixe" if donnees.get("fixe", False) else None,
                identifiant,
            )
            for identifiant, donnees in scenario["objets"].items()
        }

        for identifiant_piece, donnees_piece in salles.items():
            for identifiant_objet in donnees_piece.get("objets", []):
                if identifiant_objet not in self.objets:
                    raise ValueError(
                        f"L'objet {identifiant_objet!r} de la pièce "
                        f"{identifiant_piece!r} n'existe pas."
                    )
                self.objets[identifiant_objet].placement_dans_piece(
                    self.pieces[identifiant_piece]
                )

        for identifiant, donnees in salles.items():
            for direction, sortie in donnees.get("sorties", {}).items():
                if isinstance(sortie, str):
                    destination = sortie
                    details = {}
                else:
                    destination = sortie["vers"]
                    details = sortie

                if destination not in self.pieces:
                    raise ValueError(
                        f"La sortie {direction!r} de {identifiant!r} "
                        f"mène à une salle inconnue : {destination!r}."
                    )

                self.pieces[identifiant].sorties[direction] = {
                    "piece": self.pieces[destination],
                    "requiert": details.get("requiert"),
                    "bloquee": details.get("bloquee"),
                    "ouverture": details.get("ouverture", ""),
                }