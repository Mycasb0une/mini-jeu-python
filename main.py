import json
import Joueur
import Carte


nom = input("Entrez le nom du joueur : ")
FICHIER_JSON = "manoir.json"
with open(FICHIER_JSON, "r", encoding="utf-8") as fichier:
    scenario = json.load(fichier)

print(scenario["titre"])
print(scenario["intro"])
carte = Carte.carte(scenario)
if scenario["depart"] not in carte.pieces:
    raise ValueError(
        f"La pièce de départ {scenario['depart']!r} n'existe pas."
    )

joueur1 = Joueur.joueur(nom, carte.pieces[scenario["depart"]])
print(f"Vous êtes dans la pièce : {joueur1.piece}")
print(joueur1.piece.description)

while True:
    commande = input(
        "Où voulez-vous aller ? (ex. « aller au nord » ; "
        "« quitter » pour arrêter) : "
    ).strip().lower()

    if commande == "quitter":
        break

    if commande.startswith("aller "):
        commande = commande[len("aller "):].strip()
        if commande.startswith("au "):
            commande = commande[len("au "):].strip()

    if not commande:
        print("Indiquez une direction.")
        continue

    deplacement_reussi, message = joueur1.aller(commande)
    if message:
        print(message)

    if not deplacement_reussi:
        continue

    print(f"Vous êtes maintenant dans : {joueur1.piece}")
    print(joueur1.piece.description)

    if joueur1.piece.identifiant == scenario["arrivee"]:
        print(scenario["victoire"])
        break
