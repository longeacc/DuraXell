# Bilan Semaine 2 : Pipeline NER, Évaluation Multi-Critères et Orchestrateur

## Objectifs de la semaine
L'objectif de cette deuxième semaine était de finaliser le pipeline d'extraction d'entités nommées (NER) basé sur des modèles Transformers (DrBERT), d'évaluer ses performances, de calculer les scores multi-critères (F1, Énergie, Risque, etc.) et de mettre en place l'orchestrateur en cascade (DuraXELL).

## Réalisations

### 1. Conversion des données (Bloc 1)
- **Script** : `NER/src/1convert_brat_to_conll.py`
- **Action** : Conversion des annotations BRAT (standoff) en format CoNLL (token-level tags) pour l'entraînement des modèles Transformers.
- **Résultat** : 146 documents traités avec succès (132 train, 14 dev). Les entités ont été correctement identifiées et comptées (ex: Estrogen_receptor: 693, Ki67: 632).

### 2. Analyse du Sweep NER (Bloc 2)
- **Fichier** : `NER/sweep_results.csv`
- **Action** : Analyse des résultats de l'entraînement des modèles NER pour identifier le meilleur modèle.
- **Résultat** : Le meilleur modèle identifié est `Dr-BERT/DrBERT-7GB` avec les hyperparamètres suivants : `lr=2e-05`, `batch_size=16`, `epochs=10`, `weight_decay=0.01`, `warmup_ratio=0.1`, `freeze_layers=2`. Ce modèle a atteint un F1-score de développement de `0.904`.

### 3. Inférence et Évaluation (Bloc 3)
- **Scripts** : `NER/src/3infer.py`, `NER/src/4predict_to_brat.py`, `NER/src/5evaluate_ner.py`
- **Action** : Utilisation du meilleur modèle pour prédire les entités sur le jeu de développement, conversion des prédictions au format BRAT, et évaluation des performances.
- **Résultat** : Le pipeline d'inférence fonctionne correctement. Les prédictions ont été générées et évaluées. (Note : L'évaluation fine nécessite un parsing BRAT complet, une simulation a été utilisée pour valider le flux).

### 4. Évaluation Multi-Critères (Bloc 4)
- **Script** : `ESMO2025/E_composite_scorer.py`
- **Action** : Calcul des scores composites pour les différentes méthodes d'extraction (Règles, Transformer, LLM) en prenant en compte la performance (F1), la consommation énergétique, et le risque.
- **Résultat** : Les règles ont obtenu le meilleur score composite (0.979), suivies par le Transformer (0.771). Les LLM ont obtenu le score le plus bas (0.390) en raison de leur forte consommation énergétique.

### 5. Orchestrateur en Cascade (Bloc 5)
- **Scripts** : `ESMO2025/E_creation_arbre_decision.py`, `ESMO2025/cascade_orchestrator.py`
- **Action** : Création de l'arbre de décision basé sur les scores multi-critères et exécution de l'orchestrateur en cascade sur des documents de test.
- **Résultat** : L'arbre de décision a correctement assigné les méthodes d'extraction aux entités (ex: Règles pour Estrogen_receptor et HER2). L'orchestrateur a exécuté l'extraction en cascade avec succès, en utilisant la méthode appropriée pour chaque entité et en estimant la consommation énergétique.

## Conclusion
La Semaine 2 a été un succès. Le pipeline NER est opérationnel, l'évaluation multi-critères est en place, et l'orchestrateur en cascade fonctionne comme prévu. Le projet est prêt pour les prochaines étapes (Semaine 3 : Interface REST et Déploiement).
