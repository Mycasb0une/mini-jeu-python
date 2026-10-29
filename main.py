#---Point d'entrée du jeu et interface textuelle avec le joueur---

import json
from pathlib import Path

import Joueur, Carte, Jeu
import Objet

def afficher_sorties(joueur: Joueur.joueur, sorties_verrouillees: set[tuple[str, str]]) -> None:
    """Affiche les sorties de la pièce et indique celles qui restent verrouillées.

    :param: joueur: Joueur dont la pièce actuelle fournit les sorties à afficher.
            sorties_verrouillees: Couples (identifiant de pièce, direction)
        déjà tentés sans posséder l'objet requis.

    :precondition: Le joueur doit avoir une pièce actuelle.

    :return: Aucun.

    :effet de bord: Oui
    """
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


def afficher_objets(piece: Carte.piece) -> None:
    """Affiche les objets présents dans une pièce.

    :param piece: Pièce dont les objets doivent être affichés.

    :precondition: Aucune

    :return: Aucun.

    :effet de bord: Oui
    """
    if not piece.objets:
        print("Il n'y a aucun objet dans cette pièce.")
        return

    print("Les objets dans cette pièce sont :")
    for objet in piece.objets:
        print(f"  {objet.nom}")


def trouver_objet(objets: list[Objet.objet], nom: str) -> Objet.objet | None:
    """Recherche un objet à partir de son nom affiché ou de son identifiant.

    Les noms et identifiants des objets sont comparés en minuscules ;
    la valeur de ``nom`` doit donc déjà être normalisée.

    :param: objets: Objets parmi lesquels effectuer la recherche.
            nom: Nom ou identifiant recherché, en minuscules.
    
    :precondition: Aucune

    :return: Le premier objet correspondant, ou ``None`` si aucun ne
        correspond.
    
    :effet de bord: Aucun
    """
    for objet in objets:
        if objet.nom.lower() == nom or objet.identifiant.lower() == nom:
            return objet
    return None


def choisir_scenario(dossier_scenarios: Path) -> Path:
    """Propose les scénarios JSON disponibles et renvoie celui sélectionné.

    :param dossier_scenarios: Dossier où rechercher les fichiers ``.json``.
    
    :precondition: Aucune

    :return: Chemin du scénario choisi.

    :raises SystemExit: Si aucun fichier JSON n'est trouvé dans le dossier.
    
    :effet de bord: Oui
    """
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
afficher_objets(joueur1.piece)
afficher_sorties(joueur1, sorties_verrouillees)

abreviations = {"n": "nord", "s": "sud", "e": "est", "o": "ouest"}

while True:
    # Demande au joueur une direction ou une commande, puis normalise sa réponse.
    commande = input(
        "Où voulez-vous aller ? : "
    ).strip().lower()

    # Termine la partie si le joueur tape "quitter" ou "quittez".
    if commande == "quitter" or commande == "quittez":
        break

    # Affiche les objets présents dans la pièce actuelle.
    if commande == "objets":
        afficher_objets(joueur1.piece)
        continue

    # Affiche la description d'un objet dans la pièce ou dans l'inventaire.
    if commande.startswith("regarder "):
        nom_objet = commande[len("regarder "):].strip()
        objets_accessibles = (
            joueur1.piece.objets + list(joueur1.inventaire)
        )
        objet = trouver_objet(objets_accessibles, nom_objet)
        if objet is None:
            print("Vous ne voyez pas cet objet ici.")
        else:
            print(objet.description)
        continue

    # Ramasse un objet de la pièce et le place dans l'inventaire.
    if commande.startswith("ramasser "):
        nom_objet = commande[len("ramasser "):].strip()
        objet = trouver_objet(joueur1.piece.objets, nom_objet)
        if objet is None:
            print("Cet objet n'est pas dans cette pièce.")
        else:
            print(Jeu.ramasser_objet(joueur1, objet))
        continue

    # Dépose un objet de l'inventaire dans la pièce actuelle.
    if commande.startswith("deposer "):
        nom_objet = commande[len("deposer "):].strip()
        objet = trouver_objet(joueur1.inventaire, nom_objet)
        if objet is None:
            print("Vous n'avez pas cet objet dans votre inventaire.")
        else:
            print(Jeu.deposer_objet(joueur1, objet))
        continue

    # Permet d'écrire "aller nord" ou "aller au nord" avant de se déplacer.
    if commande.startswith("aller "):
        commande = commande[len("aller "):].strip()
        if commande.startswith("au "):
            commande = commande[len("au "):].strip()

    # Remplace une abréviation par la direction complète correspondante.
    commande = abreviations.get(commande, commande)

    # Indique au joueur qu'il doit saisir une direction si sa réponse est vide.
    if not commande:
        print("Indiquez une direction.")
        continue

    # Tente le déplacement et récupère la sortie pour vérifier si elle est verrouillée.
    piece_depart = joueur1.piece
    sortie_tentee = piece_depart.sorties.get(commande)
    deplacement_reussi, message = joueur1.aller(commande)
    if message:
        print(message)

    # Si le déplacement échoue, signale une sortie verrouillée si nécessaire.
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

    # Après un déplacement réussi, affiche les informations de la nouvelle pièce.
    sorties_verrouillees.discard((piece_depart.identifiant, commande))
    print(f"Vous êtes maintenant dans : {joueur1.piece}")
    print(joueur1.piece.description)
    afficher_objets(joueur1.piece)
    afficher_sorties(joueur1, sorties_verrouillees)

    # Termine la partie si le joueur arrive à la destination finale.
    if joueur1.piece.identifiant == scenario["arrivee"]:
        print(scenario["victoire"])
        break
