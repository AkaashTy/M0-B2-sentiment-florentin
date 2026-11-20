"""Logique d'inférence pour la classification de sentiment.

Le modèle CamemBERT chargé sort des labels 5 étoiles
(`'1 star'`, `'2 stars'`, ..., `'5 stars'`). Le métier (Aubergine Hôtels)
veut 3 classes (`négatif`, `neutre`, `positif`).

→ Ton travail dans ce fichier :
   1. Implémenter `predict_sentiment()` (récupère les scores 5★ + applique ta règle).
   2. Implémenter `map_stars_to_sentiment()` (mapping 5★ → 3 classes).
   3. Écrire ta règle dans le commentaire `# DECISION:` ci-dessous AVANT de coder.

Le pipeline transformers est chargé une seule fois au démarrage, dans
`main.py` (lifespan), et stocké dans `state["pipeline"]`. Tu le récupères
en argument.
"""
from __future__ import annotations

# DECISION: (à écrire avant de coder, en français)
#   Règle retenue : ... étoiles -> négatif / ... -> neutre / ... -> positif
#   Argument métier 1 : ...
#   Argument métier 2 : ...
# 
# DECISION FFO
# 
# Situation : Hotel, propriétaire veut utiliser les avis client pour améliorer ses services
# 
# Comment les utilisateurs choisissent leur logement pour un séjour 
# > Consultation des autres utilisateurs afin de déterminer si le lieu leur correspond
# > Dans notre cas c'est le propriétaire qui consulte ses résultats pour ensuite les classer
# > Les classer dans le but de régler les problèmes soulevés par les clients
# > En partant de ce postulat, un avis 5★ peut être considéré comme 'parfait' car il y a la note maximale. et donc normalement pas de défauts à corriger
# > Par contre un avis 4★ est certes bon mais peut permettre de soulever des petits problèmes qui persistent dans l'établissement. Des efforts minimes seront à surveiller afin de transformer ces 4★ en 5★
# > Ensuite nous pouvons considérer que les autres avis 1★, 2★, 3★ sont eux les plus éloignés de la note parfaite et donc il y a plus d'effort a fournir de la part du propriétaire pour augmenter l'expérience client
# > Ces trois premiers niveaux peuvent donc être considérés comme négatif par le propriétaire
# 
# Avec ce raisonnement on peut prévoir un très grand nombre de résultats négatifs.
# Mais tous les avis classés comme tel auront un axe d'amélioration possible. 
# 
#   Règle retenue : 1★, 2★, 3★ étoiles -> négatif / 4★ -> neutre / 5★ -> positif


import time
from typing import Any

from app.schemas import Sentiment, SentimentOut


def map_stars_to_sentiment(star_label: str) -> Sentiment:
    """Mappe un label 5 étoiles ('1 star', ..., '5 stars') en 3 classes métier.

    À compléter par l'apprenant. **Le choix du mapping est un arbitrage
    métier**, pas une recette imposée : plusieurs découpages sont valides
    (cf. mini-cours `02_HuggingFace_Transformers_essentiel.md`, section
    "Justification du seuil de mapping").

    Ton travail : proposer **ton** mapping et **le justifier** dans le
    commentaire `# DECISION:` en haut de ce fichier, puis dans
    `rendu/<prenom>/ANALYSE.md` (coût d'un faux positif / faux négatif
    côté métier Aubergine Hôtels).

    Args:
        star_label: label produit par le modèle (ex: '4 stars').

    Returns:
        Sentiment 3 classes.

    Raises:
        ValueError: si `star_label` n'est pas dans le format attendu.
    """
    # TODO Tâche 3 — implémenter le mapping décrit dans `# DECISION:`.
    # raise NotImplementedError("Compléter `map_stars_to_sentiment` (Tâche 3).")
    stars = int(star_label.split()[0])
    if stars <= 3:
        return "négatif"
    if stars == 4:
        return "neutre"
    return "positif"


def predict_sentiment(pipeline: Any, text: str, model_name: str) -> SentimentOut:
    """Inférence de sentiment sur un texte FR.

    Args:
        pipeline: pipeline `transformers.pipeline("text-classification", ...)`
            chargé au démarrage de l'API.
        text: texte FR de la review.
        model_name: identifiant HF du modèle (passé pour traçabilité).

    Returns:
        SentimentOut avec sentiment 3 classes, scores 5★ bruts, et latence ms.
    """
    # TODO Tâche 3 — compléter :
    #
    # 1. Mesurer le temps d'inférence (time.perf_counter() avant/après).
    # 2. Appeler `raw = pipeline(text)` (sans argument en plus : le pipeline
    #    est déjà construit avec `top_k=None` dans `main.py`). `raw` est une
    #    liste contenant une liste de 5 dicts {'label', 'score'} : les
    #    probabilités sont dans `raw[0]`.
    # 3. Construire `scores_5_stars: dict[str, float]` à partir de `raw[0]`.
    # 4. Appliquer la règle écrite dans `# DECISION:` pour obtenir la classe
    #    métier : étoile la plus probable (puis `map_stars_to_sentiment`),
    #    ou somme des probabilités par groupe d'étoiles.
    # 5. Renvoyer un `SentimentOut(...)`.
    # raise NotImplementedError("Compléter `predict_sentiment` (Tâche 3).")


    start = time.perf_counter()
    
    raw = pipeline(text)
    scores_5_stars = {}
    for item in raw[0]:
        scores_5_stars[item['label']] = item['score']
        
    top_label = max(raw[0], key=lambda x: x['score'])['label']

    sentiment = map_stars_to_sentiment(top_label)

    duration_ms = (time.perf_counter() - start) * 1000
    return SentimentOut(sentiment=sentiment, scores_5_stars=scores_5_stars, model_name=model_name, latence_ms=duration_ms)