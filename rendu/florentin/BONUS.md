# BONUS

## H — Mesurer l'effet d'un autre découpage 5★ → 3 classes

### Sortie du script `comparer_mappings.py`

```
Nombre d'avis correct pour 30 avis ==> {'A': 24, 'B': 21, 'C': 21, 'perso': 17, 'S': 25}

Méthode A : 24/30
négatif ==> {'négatif': 8, 'neutre': 2, 'positif': 1}
neutre ==> {'négatif': 1, 'neutre': 6, 'positif': 1}
positif ==> {'négatif': 0, 'neutre': 1, 'positif': 10}

Méthode B : 21/30
négatif ==> {'négatif': 4, 'neutre': 6, 'positif': 1}
neutre ==> {'négatif': 0, 'neutre': 7, 'positif': 1}
positif ==> {'négatif': 0, 'neutre': 1, 'positif': 10}

Méthode C : 21/30
négatif ==> {'négatif': 8, 'neutre': 3, 'positif': 0}
neutre ==> {'négatif': 1, 'neutre': 7, 'positif': 0}
positif ==> {'négatif': 0, 'neutre': 5, 'positif': 6}

Méthode perso : 17/30
négatif ==> {'négatif': 10, 'neutre': 1, 'positif': 0}
neutre ==> {'négatif': 7, 'neutre': 1, 'positif': 0}
positif ==> {'négatif': 1, 'neutre': 4, 'positif': 6}

Méthode S : 25/30
négatif ==> {'négatif': 10, 'neutre': 0, 'positif': 1}
neutre ==> {'négatif': 2, 'neutre': 5, 'positif': 1}
positif ==> {'négatif': 0, 'neutre': 1, 'positif': 10}
```

### Analyse

#### 1. Quelle règle classe le plus d'avis correctement ? Quelle règle manque le moins de négatifs ? Est-ce la même ?

La règle des sommes est celle qui ressort le plus de résultats positifs. La méthode S et ma méthode sont celles qui ressortent le moins de cas négatifs incorrects, ma méthode a tendance à favoriser le classement en négatif et la méthode S malgrès son taux de reussite correct a placer sa seul erreur "négatif" en "positif". La règle des sommes se retrouvent dans les deux catégories ce qui peux transformer notre décision finale

#### 2. Combien d'avis séparent la meilleure règle de la tienne ? Sur 30 avis, un avis = 3,3 points. Un écart de 1 ou 2 avis te paraît-il suffisant pour changer de règle ? Pourquoi ?

Un écart de 8 est visible entre ma méthode et celle des sommes. L'écart est très important et redéfinit totalement ma vision des choses. Avec ce jeu de données, je ne peux que recommander au propriétaire d'adopter la règle des sommes. Dans le cas contraire, il pourrait être submergé d'avis négatifs et/ou neutres. Un deuxième tri serait même nécessaire après ce premier filtre.

#### 3. Ouvre `data/sample_reviews.csv` et compare les colonnes `note_client` et `sentiment_attendu`. Comment le sentiment attendu semble-t-il avoir été fabriqué ? Qu'est-ce que ça implique pour la comparaison que tu viens de faire ?

Le jeu de données est construit pour mettre en évidence les dérives des différents choix qui sont présents. C'est pour cela que précédemment, j'ai indiqué que le changement de règle est justifié seulement par le jeu de données fourni.

#### 4. Si tu choisis la règle qui gagne sur ces 30 avis, puis que tu annonces son score au client, ce score est-il fiable ? Que te faudrait-il pour l'affirmer ?

Ce score n'est pas fiable pour la suite et l'utilisation réelle qu'en fera le client. Ce jeu de données est orienté pour montrer les dérives possibles. Il faudrait utiliser une base de données plus fournie et non biaisée. Mais en l'état, avec ce jeu de données nous devons changer de règle pour celle des sommes. 
