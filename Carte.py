class piece:
    
    def __init__(self, identifiant, donnees):
        self.identifiant = identifiant
        self.name = donnees["nom"]
        self.description = donnees.get("description", "")
        self.sorties = {}

    def aller(self, direction, inventaire):
        sortie = self.sorties.get(direction)
        if sortie is None:
            return None, f"Il n'y a pas de sortie vers le {direction}."

        objet_requis = sortie.get("requiert")
        if objet_requis is not None and objet_requis not in inventaire:
            return None, sortie.get(
                "bloquee", "Le passage est bloqué."
            )

        return sortie["piece"], sortie.get("ouverture", "")

    def sorties_accessibles(self, inventaire):
        return {
            direction: sortie["piece"]
            for direction, sortie in self.sorties.items()
            if sortie["requiert"] is None
            or sortie["requiert"] in inventaire
        }

    def sorties_inaccessibles(self, inventaire):
        return {
            direction: sortie["piece"]
            for direction, sortie in self.sorties.items()
            if sortie["requiert"] is not None
            and sortie["requiert"] not in inventaire
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