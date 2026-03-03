# AUDIT DU 24 FÉVRIER 2026 - DURAXELL

## 1. État des lieux ESMO2025 (Métriques)

| Script | Rôle | État Actuel | Entrées | Sorties | Qualité / Bugs |
| [E_templeability.py](ESMO2025/E_templeability.py) | Calcule la stabilité de la forme (Te) | ✅ VALIDÉ (Tests OK) | Corpus brut | CSV, JSON | Normalisation regex robuste. |
| [E_homogeneity.py](ESMO2025/E_homogeneity.py) | Calcule la variabilité lexicale (He) | ✅ VALIDÉ (Tests OK) | CSV Te | CSV He | Retourne float correct maintenant. |
| [E_risk_context.py](ESMO2025/E_risk_context.py) | Détecte le risque (négation, ambiguïté) | ✅ VALIDÉ (Tests OK) | Corpus | JSON | Regex améliorées pour négation. |
| [E_frequency.py](ESMO2025/E_frequency.py) | Compte les occurrences (Freq) | ✅ VALIDÉ (Tests OK) | Corpus | CSV | Gestion eco2ai isolée. Logique ingestion testée. |
| [E_annotation_yield.py](ESMO2025/E_annotation_yield.py) | Calcule le rendement (F1 Règles vs GS) | ✅ VALIDÉ (Tests OK) | Dossiers GS/Pred | CSV | Import `DecisionTree` corrigé. Logique F1 stricte implémentée. |

## 2. État du Pipeline NER

- **Structure** : Dossier `NER/` présent.
- **Modèles** : Scripts 1 à 4 présents.
- **Manquant** : Le modèle entraîné réel (`best_model.pt`) n'est pas dans le dossier (logique, trop lourd pour git/workspace).
- **Format** : Utilise BRAT (.ann) en entrée/sortie. C'est standard.

## 3. Arbre de Décision

- **Script** : [E_creation_arbre_decision.py](ESMO2025/E_creation_arbre_decision.py)
- **Logique** : 
    1. Structure (Te + He) > Seuil ? -> OUI
    2. Risque < Seuil ? -> OUI -> **REGLES**
    3. Sinon -> **ML**
- **Yield** : Intégré récemment.
- **Sortie** : `decision_config.json` généré correctement.

## 4. Module REST-interface

- **Status** : Squelette créé (Mardi/Mercredi).
- **Architecture** :
    - `rest_annotator.py` : Saisie (Highlighting).
    - `rest_evaluator.py` : Analyse (Empirisme).
    - `rest_decision_bridge.py` : Comparaison (Top-down vs Bottom-up).
- **Intégration** : Prêt pour la phase de test.

## 5. Environnement

- **Dépendances** : `requirements.txt` à mettre à jour avec `eco2ai`, `transformers`, `torch`.
- **Reproductibilité** : Les scripts s'exécutent via `run_full_pipeline_report.py`.
