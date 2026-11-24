import json
from pathlib import Path

FICHIER_SCORES = Path(__file__).parent / "scores_30_avis.json"
CLASSES = ["négatif", "neutre", "positif"]


# un dict {nombre d'étoiles: classe métier}.
REGLES_ETOILE: dict[str, dict[int, str]] = {
    "A": {1: "négatif", 2: "négatif", 3: "neutre", 4: "positif", 5: "positif"},
    "B": {1: "négatif", 2: "neutre", 3: "neutre", 4: "positif", 5: "positif"},
    "C": {1: "négatif", 2: "négatif", 3: "neutre", 4: "neutre", 5: "positif"},
    "perso": {1: "négatif", 2: "négatif", 3: "négatif", 4: "neutre", 5: "positif"},
}

def etoile_max(scores: dict[str, float]) -> int:
    label = max(scores, key=scores.get)
    return int(label.split()[0])

def regle_somme(scores: dict[str, float]) -> str:
    totaux = {
        "négatif": scores["1 star"] + scores["2 stars"],
        "neutre": scores["3 stars"],
        "positif": scores["4 stars"] + scores["5 stars"],
    }
    return max(totaux, key=totaux.get)

avis = json.loads(FICHIER_SCORES.read_text(encoding="utf-8"))
total = len(avis)
count_correct = {}
matrices = {}

for methode in list(REGLES_ETOILE) + ['S']:
    count_correct[methode]=0
    matrices[methode] = {attendu: {predit: 0 for predit in CLASSES} for attendu in CLASSES}
    for a in avis:
        if methode == "S":
            predit = regle_somme(a['scores_5_stars'])
        else:
            rules = REGLES_ETOILE[methode]
            max_star = etoile_max(a['scores_5_stars'])
            predit = rules[max_star]
        if predit == a['attendu']:
            count_correct[methode]+= 1
        matrices[methode][a['attendu']][predit] += 1


print(f"Nombre d'avis correct pour {len(avis)} avis ==> {count_correct}")

for methode, matrice in matrices.items():
    print(f"\n Méthode {methode} : {count_correct[methode]}/{total} ")
    for attendu, ligne in matrice.items():
        print(attendu, "==>", ligne)