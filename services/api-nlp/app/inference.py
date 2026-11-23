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

# DECISION:
#   Règle retenue : 1★, 2★, 3★ -> négatif / 4★ -> neutre / 5★ -> positif
#   Argument métier 1 : Écarter les cas 5 qui sont les moins pertinents pour une amélioration des services.
#   Argument métier 2 : Les cas neutres (4) sont quand même identifiables dans le cas où le propriétaire veux agir sur des avis proches de la perfection
#   Argument métier 3 : Engranger un maximum d'avis négatif (1/2/3) pour cibler les différents points d'amélioration.
#   Attention 1 : Taux de faux positif/négatif peuvent être fréquent avec les cas 3★
#       exemple : 3★ : 0.45, 4★ : 0.35, 5★ : 0.20
#                 Ce genre de cas est potentiellement une fausse alerte avec ce fonctionnement 

import time
from typing import Any

from app.schemas import Sentiment, SentimentOut


def map_stars_to_sentiment(star_label: str) -> Sentiment:
    """Mappe un label 5 étoiles ('1 star', ..., '5 stars') en 3 classes métier.

    Args:
        star_label: label produit par le modèle (ex: '4 stars').

    Returns:
        Sentiment 3 classes.

    Raises:
        ValueError: si `star_label` n'est pas dans le format attendu.
    """
    if not isinstance(star_label, str):
        raise ValueError("star_label doit être une chaîne de caractères.")
    parts = star_label.split(" ", maxsplit=1)
    if len(parts) != 2 or not parts[1]:
        raise ValueError("star_label format invalide, espace manquant.")
    
    stars = int(parts[0])
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
    start = time.perf_counter()
    raw = pipeline(text)
    duration_ms = (time.perf_counter() - start) * 1000
    
    scores_5_stars = {}
    for item in raw[0]:
        scores_5_stars[item['label']] = item['score']
        
    top_label = max(raw[0], key=lambda x: x['score'])['label']

    sentiment = map_stars_to_sentiment(top_label)

    return SentimentOut(sentiment=sentiment, scores_5_stars=scores_5_stars, model_name=model_name, latence_ms=duration_ms)