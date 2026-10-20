import json
import Joueur
nom = input("Entrez le nom du joueur : ")
joueur1 = Joueur.joueur(nom)
FICHIER_JSON = "manoir.json"
with open(FICHIER_JSON, "r", encoding="utf-8") as fichier:
    manoir = json.load(fichier)

print(manoir["titre"])
print(manoir["intro"])
print("Vous êtes dans la pièce :", manoir["départ"])




