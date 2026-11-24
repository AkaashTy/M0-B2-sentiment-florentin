from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
import pytest

@pytest.fixture(scope="module")
def client():
    # Le bloc "with" déclenche le lifespan (startup/shutdown) de l'app
    with TestClient(app) as test_client:
        yield test_client
        
def test_predict_texte_positif_valid_200(client) -> None:
    payload = {
        "texte": "Personnel charmant, chambre impeccable, on reviendra !",
        }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["sentiment"] in {"positif","neutre","négatif"}
    assert len(body["scores_5_stars"]) == 5
        
        
def test_predict_texte_vide_invalid_422(client) -> None:
    payload = {
        "texte": "",
        }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

@pytest.mark.parametrize("avis, attente", [
    ("Excellente nuit, accueil au top, vue sur le bassin imprenable. Coup de cœur de l'année !", "positif"),
    ("Hôtel d'une médiocrité rare. Bruit de plomberie toute la nuit, et personne pour s'en occuper.", "négatif"),
    ("Que dire à part que c'était parfait. Personnel, propreté, confort, calme. Tout y était. Bravo.", "positif"),
])
def test_predict_avis_attente_200(client, avis: str, attente: str) -> None:
    payload = {
        "texte": avis,
        }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["sentiment"] == attente