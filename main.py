import json
from pathlib import Path

import Joueur
import Carte


def afficher_sorties(joueur, sorties_verrouillees):
    """Affiche les sorties et signale celles déjà testées sans la bonne clé."""
    print("Les sorties sont :")
    for direction, sortie in joueur.piece.sorties.items():
        destination = sortie["piece"]
        verrouillee = (
            (joueur.piece.identifiant, direction) in sorties_verrouillees
            and not Carte.possede_objet(
                joueur.inventaire, sortie["requiert"]
            )
        )
        indication = " (verrouillée)" if verrouillee else ""
        print(f"  {direction} : {destination}{indication}")


def choisir_scenario(dossier_scenarios):
    """Affiche les scénarios JSON disponibles et renvoie celui sélectionné."""
    scenarios = sorted(dossier_scenarios.glob("*.json"))
    if not scenarios:
        raise SystemExit(
            f"Aucun scénario JSON trouvé dans {dossier_scenarios}."
        )

    print("Scénarios disponibles :")
    for numero, chemin in enumerate(scenarios, start=1):
        print(f"  {numero}. {chemin.stem}")

    while True:
        choix = input("Quel scénario voulez-vous jouer ? : ").strip()
        try:
            index = int(choix) - 1
        except ValueError:
            print("Entrez le numéro d'un scénario.")
            continue

        if 0 <= index < len(scenarios):
            return scenarios[index]
        print(f"Choisissez un numéro entre 1 et {len(scenarios)}.")


DOSSIER_PROJET = Path(__file__).resolve().parent
DOSSIER_SCENARIOS = DOSSIER_PROJET / "scenarios"
FICHIER_JSON = choisir_scenario(DOSSIER_SCENARIOS)
nom = input("Entrez le nom du joueur : ")
with open(FICHIER_JSON, "r", encoding="utf-8") as fichier:
    scenario = json.load(fichier)

print(scenario["titre"])
print(scenario["intro"])
carte = Carte.carte(scenario)
if scenario["depart"] not in carte.pieces:
    raise ValueError(
        f"La pièce de départ {scenario['depart']!r} n'existe pas."
    )

joueur1 = Joueur.joueur(
    nom,
    carte.pieces[scenario["depart"]],
    scenario["capacite"],
)
sorties_verrouillees = set()
print(f"Vous êtes dans la pièce : {joueur1.piece}")
print(joueur1.piece.description)
afficher_sorties(joueur1, sorties_verrouillees)

while True:
    commande = input(
        "Où voulez-vous aller ? : "
    ).strip().lower()

    if commande == "quitter" or commande == "quittez":
        break

    if commande.startswith("aller "):
        commande = commande[len("aller "):].strip()
        if commande.startswith("au "):
            commande = commande[len("au "):].strip()

    if not commande:
        print("Indiquez une direction.")
        continue

    piece_depart = joueur1.piece
    sortie_tentee = piece_depart.sorties.get(commande)
    deplacement_reussi, message = joueur1.aller(commande)
    if message:
        print(message)

    if not deplacement_reussi:
        if (
            sortie_tentee is not None
            and sortie_tentee["requiert"] is not None
            and not Carte.possede_objet(
                joueur1.inventaire, sortie_tentee["requiert"]
            )
        ):
            sorties_verrouillees.add((piece_depart.identifiant, commande))
            afficher_sorties(joueur1, sorties_verrouillees)
        continue

    sorties_verrouillees.discard((piece_depart.identifiant, commande))
    print(f"Vous êtes maintenant dans : {joueur1.piece}")
    print(joueur1.piece.description)
    afficher_sorties(joueur1, sorties_verrouillees)

    if joueur1.piece.identifiant == scenario["arrivee"]:
        print(scenario["victoire"])
        break
