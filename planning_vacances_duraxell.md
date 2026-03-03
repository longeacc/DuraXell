# Planning Vacances DuraXELL — 24 février → 8 mars 2026

## Cadrage stratégique (auto-évaluation HDR)

### Repositionnement critique : ESMO2025 **est** DuraXELL

Après examen du dépôt `longeacc/ESMO2025`, une observation s'impose : ce repository n'est pas un sous-projet à "inclure dans" DuraXELL — **il en constitue le cœur opérationnel**. Sa structure contient déjà les métriques fondamentales (Te, He, R, Freq), l'arbre de décision (`E_creation_arbre_decision.py`), le pipeline NER complet (BRAT → CoNLL → HuggingFace → Prédiction), et le système de règles. Traiter ESMO2025 comme un composant annexe serait une erreur architecturale.

**Décision d'initiative (HDR)** : le planning est construit autour de ESMO2025 comme colonne vertébrale, dans laquelle le projet REST-interface de Guillaume Bazin est intégré comme module de validation empirique. L'arbre de décision existant dans `E_creation_arbre_decision.py` est déjà fonctionnel mais nécessite des raffinements sur les seuils, l'ajout de la métrique d'annotation yield, et la connexion avec la méthodologie REST.

### Architecture cible à l'issue des 10 jours de travail

```
ESMO2025/                                ← RACINE DuraXELL
├── ESMO2025/
│   ├── E_templeability.py               ← EXISTANT (à auditer/affiner)
│   ├── E_homogeneity.py                 ← EXISTANT (à auditer/affiner)
│   ├── E_risk_context.py                ← EXISTANT (à auditer/affiner)
│   ├── E_frequency.py                   ← EXISTANT (à auditer/affiner)
│   ├── E_fesability_NER.py              ← EXISTANT (à compléter)
│   ├── E_creation_arbre_decision.py     ← EXISTANT (à raffiner seuils + yield)
│   ├── cascade_orchestrator.py          ← À CRÉER — orchestre Rules→ML→LLM
│   ├── energy_tracker.py                ← À CRÉER — mesure unifiée kWh/CO2
│   ├── REST_interface/                  ← INTÉGRATION Bazin
│   │   ├── rest_annotator.py            ← Outil d'annotation pilote ~40 dossiers
│   │   ├── rest_evaluator.py            ← Boucle itérative évaluation par entité
│   │   ├── rest_decision_bridge.py      ← Pont REST ↔ arbre de décision
│   │   └── templates/                   ← Templates web pour annotation
│   ├── NER/                             ← EXISTANT
│   │   ├── data/                        ← Données BRAT
│   │   ├── models/                      ← Modèles entraînés
│   │   └── src/                         ← Pipeline NER complet
│   ├── Rules/                           ← EXISTANT
│   │   └── src/                         ← Regex + évaluation
│   ├── Results/                         ← EXISTANT (à enrichir)
│   └── reports/                         ← À CRÉER — rapports consolidés
├── Consumtion_of_Duraxell.csv           ← Tracking énergie eco2ai
├── breast_cancer_biomarker_eval_summary.csv
├── commandes.ipynb                      ← À ENRICHIR — notebook maître
└── README.md                            ← À CRÉER — documentation projet
```

---

## Règles d'hygiène de vie appliquées quotidiennement

- **Lever** : 7h00 (rythme constant, y compris jours de pause)
- **Marche matinale** : 30 min minimum, à jeun ou après petit-déjeuner léger
- **Blocs de travail profond** : 90 min max, suivis de 15 min de pause
- **Marche/sport en milieu de journée** : 45-60 min (déjeuner inclus)
- **Marche vespérale** : 30-45 min
- **Écrans coupés** : 21h30
- **Coucher** : 22h00-22h30
- **Hydratation** : 2L/jour minimum
- **Pas de caféine après 14h**

---

## SEMAINE 1 : FONDATIONS ET MÉTRIQUES (24–28 février)

---

### Mardi 24 février — AUDIT COMPLET ET SETUP

**Objectif du jour** : comprendre l'état exact du code ESMO2025, cloner REST-interface, établir l'environnement de travail reproductible.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–7:30 | Réveil + routine | Hydratation, étirements légers |
| 7:30–8:00 | **Marche matinale** | 30 min, rythme soutenu, sans téléphone. Objectif : 3000 pas |
| 8:00–8:15 | Petit-déjeuner | Protéines + glucides complexes |
| **8:15–9:45** | **Bloc 1 : Audit ESMO2025** | |
| | | • Lire intégralement `ARCHITECTURE_RECAP.md` |
| | | • Exécuter chaque script `E_*.py` séparément pour comprendre les entrées/sorties |
| | | • Documenter dans un carnet : quels fichiers JSON/CSV chaque script produit |
| | | • Identifier les dépendances manquantes (`requirements.txt` → vérifier eco2ai, pandas, numpy) |
| | | • Lister les données présentes dans `Rules/src/Breast/` (combien de fichiers .ann, .txt) |
| 9:45–10:00 | Pause | Debout, étirements, eau |
| **10:00–11:30** | **Bloc 2 : Audit NER Pipeline** | |
| | | • Parcourir `NER/src/` dans l'ordre : `1convert_brat_to_conll.py` → `2sweep_ner.py` → `3infer.py` → `4predict_to_brat.py` |
| | | • Vérifier les données dans `NER/data/` : format, nombre d'exemples, split train/val |
| | | • Vérifier `NER/models/` : quels modèles sont déjà entraînés |
| | | • Examiner `sweep_results.csv` : résultats du hyperparameter sweep existant |
| | | • Documenter les F1-scores actuels par entité |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : Clone et audit REST-interface** | |
| | | • `git clone https://github.com/longeacc/REST-interface.git` |
| | | • Lire le README et identifier l'architecture du projet |
| | | • Identifier les points d'intégration avec ESMO2025 |
| | | • Mapper les composants REST vers l'architecture cible DuraXELL |
| **12:30–13:30** | **Déjeuner + marche** | Repas équilibré puis 30 min de marche digestive |
| **13:30–15:00** | **Bloc 4 : Setup environnement** | |
| | | • Créer un virtualenv unifié : `python -m venv .venv_duraxell` |
| | | • Installer toutes les dépendances : eco2ai, pandas, transformers, datasets, seqeval |
| | | • Vérifier que tous les scripts ESMO2025 s'exécutent sans erreur |
| | | • Exécuter `E_templeability.py` et vérifier la sortie `templeability_analysis.json` |
| | | • Exécuter `E_risk_context.py` et vérifier `risk_context_full.json` |
| | | • Exécuter `E_homogeneity.py` et vérifier `homogeneity_analysis.csv` |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : Exécution arbre de décision** | |
| | | • Exécuter `E_creation_arbre_decision.py` sur les données actuelles |
| | | • Comparer les résultats obtenus avec le `output_decision.txt` existant |
| | | • Documenter : quelles entités reçoivent quelle recommandation (Rules/ML/Transformer/LLM) |
| | | • Identifier les seuils actuels dans `THRESHOLDS` (TE_HIGH=0.5, TE_LOW=0.2, etc.) |
| | | • Noter les divergences éventuelles avec l'arbre théorique (6 critères, 6 feuilles) |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Synthèse et planification** | |
| | | • Rédiger un document `AUDIT_24FEV.md` : état des lieux complet |
| | | • Lister les bugs, manques, et améliorations identifiés |
| | | • Prioriser les tâches pour les jours suivants |
| | | • Commit initial : `git add . && git commit -m "Audit initial DuraXELL + setup env"` |
| **18:00–19:00** | **Marche vespérale** | 45 min, rythme modéré. Objectif cumulé : 10 000 pas |
| 19:00–20:00 | Dîner | |
| 20:00–21:00 | Lecture légère | Relire l'article Dahl et al. (2025) — section méthodes |
| 21:30 | Écrans coupés | |
| 22:00 | Coucher | |

---

### Mercredi 25 février — RAFFINEMENT DES MÉTRIQUES

**Objectif du jour** : auditer et améliorer chaque métrique (Te, He, R, Freq) dans les scripts `E_*.py`. S'assurer de la robustesse des calculs avant d'attaquer l'arbre de décision.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–8:00 | Réveil + marche matinale | 30 min de marche |
| 8:00–8:15 | Petit-déjeuner | |
| **8:15–9:45** | **Bloc 1 : Raffinement E_templeability.py** | |
| | | • Auditer `analyze_pattern_complexity()` : la normalisation "HER2 3+" → "XXXD D+" est-elle exhaustive ? |
| | | • Vérifier que le score Te est cohérent : TNM devrait avoir Te élevé (formaté), Ki-67 moyen |
| | | • Ajouter des tests unitaires : `test_templeability.py` avec 5 cas connus |
| | | • Vérifier le calcul des bonus sémantiques (%, mots-clés fixes) |
| | | • Recalculer sur l'ensemble du corpus d'entraînement et comparer avec les résultats existants |
| 9:45–10:00 | Pause | |
| **10:00–11:30** | **Bloc 2 : Raffinement E_homogeneity.py** | |
| | | • Auditer la formule He = (Te_words - Ue_words) / Te_words |
| | | • Vérifier la fonction sigmoïde de normalisation |
| | | • Cas limites : entité avec 1 seule mention, entité avec 1000 mentions identiques |
| | | • Ajouter test unitaire : ER "positif 80%" répété 100x → He devrait être très élevé |
| | | • Vérifier la cohérence He vs Te : si Te élevé + He élevé → candidat idéal pour règles |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : Raffinement E_risk_context.py** | |
| | | • Auditer la classification Haut/Faible risque |
| | | • Vérifier les cas critiques : "positif" seul (haut risque) vs "HER2 positif" (faible risque) |
| | | • Ajouter la détection de négation : "HER2 non surexprimé" → risque moyen |
| | | • Ajouter la détection d'incertitude : "probable", "possible", "à confirmer" |
| | | • Tests unitaires sur 10 exemples annotés manuellement |
| **12:30–13:30** | **Déjeuner + marche** | 45 min de marche |
| **13:30–15:00** | **Bloc 4 : Raffinement E_frequency.py** | |
| | | • Vérifier le calcul de fréquence relative (proportion par rapport au corpus total) |
| | | • Calibrer le seuil `FREQ_SUFFICIENT=0.001` : est-ce adapté à la taille du corpus ? |
| | | • Calculer la distribution des fréquences pour toutes les entités |
| | | • Identifier les entités rares (< 10 occurrences) : candidates au fallback règles/LLM |
| | | • Produire un graphique de distribution des fréquences |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : Raffinement E_fesability_NER.py** | |
| | | • Auditer le calcul de faisabilité NER : sur quoi se base-t-il ? |
| | | • Vérifier la cohérence avec les résultats du sweep NER (`sweep_results.csv`) |
| | | • Compléter si nécessaire : la faisabilité NER devrait dépendre de Te + Freq + qualité annotations |
| | | • Implémenter le score de rendement d'annotation (`annotation_yield`) s'il est absent |
| | | • Documenter la formule de calcul choisie |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Génération des rapports mis à jour** | |
| | | • Exécuter les 3 générateurs de rapports : `generate_templeability_report.py`, `generate_risk_context_report.py`, `generate_homogeneity_report.py` |
| | | • Vérifier les rapports HTML générés : sont-ils cohérents avec les nouvelles métriques ? |
| | | • Commit : `"Raffinement métriques Te/He/R/Freq + tests unitaires"` |
| **18:00–19:00** | **Sport : marche rapide ou randonnée** | Objectif : 12 000 pas |
| 19:00–20:00 | Dîner | |
| 20:00–21:00 | Lecture | Article REST/templeability — préparation intégration Bazin |
| 22:00 | Coucher | |

---

### Jeudi 26 février — ARBRE DE DÉCISION : RAFFINEMENT ET TESTS

**Objectif du jour** : transformer l'arbre de décision existant en un système robuste avec seuils calibrés, gestion des cas limites, et visualisation claire.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–8:00 | Réveil + marche matinale | |
| **8:15–9:45** | **Bloc 1 : Analyse critique de E_creation_arbre_decision.py** | |
| | | • Parcourir intégralement les 344 lignes du script |
| | | • Identifier l'implémentation actuelle de `decide_method(entity)` |
| | | • Mapper chaque branche du code à l'arbre théorique (6 critères → 6 feuilles) |
| | | • Vérifier : est-ce que toutes les 6 feuilles sont atteintes ? (RÈGLES PAR DÉFAUT, NER RÈGLES, ML LÉGER NER, ML LÉGER DÉFAUT, NER TRANSFORMER, NER LLM) |
| | | • Documenter les chemins non testés et les branches mortes |
| 9:45–10:00 | Pause | |
| **10:00–11:30** | **Bloc 2 : Calibration des seuils** | |
| | | • Analyser la distribution empirique de chaque métrique pour chaque entité connue |
| | | • Utiliser les données de `output_decision.txt` comme référence (ER → ML Léger CRF, Ki67 → Transformer, HER2_FISH → LLM, etc.) |
| | | • Calibrer `TE_HIGH` : tracer la distribution Te et identifier la coupure naturelle |
| | | • Calibrer `TE_LOW` : idem, identifier le seuil entre "moyen" et "bas" |
| | | • Calibrer `HE_HIGH`, `RISK_LOW`, `FREQ_SUFFICIENT` avec la même méthode |
| | | • Documenter chaque choix de seuil avec justification statistique |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : Implémentation du rendement d'annotation (Yield)** | |
| | | • Implémenter la métrique manquante : `annotation_yield` |
| | | • Formule proposée : ratio (nombre d'annotations correctes) / (temps d'annotation estimé) |
| | | • Alternative si pas de données temporelles : proxy via (nombre d'entités concordantes GS-Prédiction) / (nombre total d'entités GS) |
| | | • Intégrer dans l'arbre de décision au nœud "Rendement d'annotation suffisant" |
| **12:30–13:30** | **Déjeuner + marche** | |
| **13:30–15:00** | **Bloc 4 : Tests exhaustifs de l'arbre** | |
| | | • Créer `test_decision_tree.py` avec les 7 entités du corpus sein : |
| | | — Estrogen_receptor (attendu : ML Léger CRF) |
| | | — Genetic_mutation (attendu : Règles par défaut) |
| | | — HER2_FISH (attendu : NER LLM) |
| | | — HER2_IHC (attendu : ML Léger CRF) |
| | | — HER2_status (attendu : ML Léger CRF) |
| | | — Ki67 (attendu : NER Transformer) |
| | | — Progesterone_receptor (attendu : ML Léger CRF) |
| | | • Vérifier que l'arbre reproduit fidèlement les résultats de `output_decision.txt` |
| | | • Ajouter les entités poumon : EGFR, ALK, ROS1, KRAS, PD-L1 (résultats attendus à définir) |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : Visualisation de l'arbre** | |
| | | • Créer un script `visualize_decision_tree.py` |
| | | • Utiliser matplotlib + graphviz pour produire une figure de l'arbre avec : |
| | | — Nœuds colorés par type (décision en bleu, feuilles colorées par méthode) |
| | | — Seuils affichés sur chaque branche |
| | | — Résultat par entité affiché dans les feuilles |
| | | • Exporter en PNG et SVG (pour l'article et la présentation) |
| | | • Sauvegarder dans `Results/decision_tree_visualization.png` |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Documentation et commit** | |
| | | • Mettre à jour `ARCHITECTURE_RECAP.md` avec les modifications |
| | | • Rédiger les docstrings de toutes les fonctions modifiées |
| | | • Commit : `"Arbre de décision calibré + tests + visualisation"` |
| **18:00–19:00** | **Marche** | 45 min |
| 19:00–22:00 | Dîner + détente | |
| 22:00 | Coucher | |

---

### Vendredi 27 février — INTÉGRATION REST-INTERFACE (Partie 1)

**Objectif du jour** : créer le module `REST_interface/` dans ESMO2025 en intégrant la méthodologie de Guillaume Bazin comme système de validation empirique bottom-up.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–8:00 | Réveil + marche matinale | |
| **8:15–9:45** | **Bloc 1 : Analyse approfondie REST-interface** | |
| | | • Étudier le dépôt cloné de Guillaume Bazin |
| | | • Identifier le cœur méthodologique : comment REST sélectionne-t-il Rules vs ML pour chaque entité ? |
| | | • Mapper la "boucle itérative 3 phases" REST sur l'arbre DuraXELL : |
| | | — Phase 1 (annotation pilote) ↔ données d'entrée des métriques Te/He |
| | | — Phase 2 (évaluation quantitative) ↔ calcul des 6 métriques |
| | | — Phase 3 (décision Rules/ML) ↔ feuilles de l'arbre de décision |
| | | • Identifier les composants réutilisables vs à réécrire |
| 9:45–10:00 | Pause | |
| **10:00–11:30** | **Bloc 2 : Création rest_annotator.py** | |
| | | • Implémenter l'outil d'annotation pilote |
| | | • Fonctionnalité : charger N dossiers patients → interface d'annotation simplifiée |
| | | • Intégrer le paradigme "highlighting" : lecture rapide du document, surlignage des biomarqueurs |
| | | • Sortie : fichiers .ann compatibles BRAT (même format que `Rules/src/Breast/`) |
| | | • Mesurer le temps d'annotation par document (pour le calcul de annotation_yield) |
| | | • Tests : annoter 3 documents synthétiques et vérifier la sortie |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : Création rest_evaluator.py** | |
| | | • Implémenter la boucle d'évaluation par entité |
| | | • Pour chaque entité annotée, calculer automatiquement : |
| | | — Nombre de patterns uniques observés |
| | | — Variabilité lexicale empirique |
| | | — Complexité contextuelle moyenne |
| | | • Sortie : rapport JSON par entité, compatible avec les entrées de l'arbre de décision |
| **12:30–13:30** | **Déjeuner + marche longue** | 1h de marche (exploration d'un nouveau parcours) |
| **13:30–15:00** | **Bloc 4 : Création rest_decision_bridge.py** | |
| | | • **Composant clé** : le pont entre l'évaluation REST empirique et l'arbre de décision théorique |
| | | • Fonctionnalité : comparer les décisions REST (empiriques) avec les décisions de l'arbre (métriques) |
| | | • Calculer un score de concordance : combien de fois REST et l'arbre convergent |
| | | • Si divergence : logger le cas et proposer un recalibrage des seuils |
| | | • Ce module valide mutuellement les deux approches (bottom-up REST ↔ top-down métriques) |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : Intégration dans la structure ESMO2025** | |
| | | • Créer le répertoire `ESMO2025/ESMO2025/REST_interface/` |
| | | • Y placer les 3 scripts créés |
| | | • Créer `REST_interface/__init__.py` avec les imports |
| | | • Mettre à jour `requirements.txt` avec les dépendances REST |
| | | • Créer un script de démonstration `REST_interface/demo_rest.py` qui : |
| | | — Charge 5 documents du corpus existant |
| | | — Exécute rest_evaluator sur chaque entité |
| | | — Compare avec les décisions de l'arbre de décision |
| | | — Affiche le rapport de concordance |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Tests et commit** | |
| | | • Exécuter `demo_rest.py` et vérifier les résultats |
| | | • Documenter l'intégration dans `ARCHITECTURE_RECAP.md` |
| | | • Commit : `"Intégration module REST-interface dans DuraXELL"` |
| **18:00–19:00** | **Sport : marche rapide** | Objectif : 12 000 pas total journée |
| 19:00–22:00 | Détente | |
| 22:00 | Coucher | |

---

### Samedi 28 février — CASCADE ORCHESTRATOR + TRACKING ÉNERGIE

**Objectif du jour** : créer le système d'orchestration cascade (Rules → ML-CRF → LLM) et unifier le tracking énergétique.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–8:00 | Réveil + marche matinale | |
| **8:15–9:45** | **Bloc 1 : Conception cascade_orchestrator.py** | |
| | | • Concevoir l'architecture du module d'orchestration |
| | | • Classe `CascadeOrchestrator` avec méthodes : |
| | | — `__init__(self, decision_tree, rules_engine, ner_model, llm_client)` |
| | | — `extract(self, document, entity_type)` : point d'entrée principal |
| | | — `_try_rules(self, text, entity_type)` : tentative extraction par règles |
| | | — `_try_ml(self, text, entity_type)` : tentative ML-CRF si rules échoue |
| | | — `_try_llm(self, text, entity_type)` : tentative LLM en dernier recours |
| | | — `_evaluate_confidence(self, result)` : score de confiance de l'extraction |
| | | • Logique de déclenchement : |
| | | — Si confiance Rules > 0.9 → accepter |
| | | — Si 0.7 < confiance Rules < 0.9 → valider avec ML |
| | | — Si confiance < 0.7 ou conflit → escalader vers LLM |
| 9:45–10:00 | Pause | |
| **10:00–11:30** | **Bloc 2 : Implémentation de la cascade** | |
| | | • Implémenter la classe `CascadeOrchestrator` |
| | | • Intégrer les règles existantes de `Rules/src/biomarker_brat_annotator.py` |
| | | • Intégrer le pipeline NER de `NER/src/3infer.py` |
| | | • Pour le LLM : créer un stub configurable (Mistral/DeepSeek via API ou local) |
| | | • Chaque étape mesure son temps d'exécution et son coût énergétique |
| | | • Résultat structuré : `{entity, value, method_used, confidence, energy_kwh, cascade_level}` |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : energy_tracker.py — Mesure unifiée** | |
| | | • Créer un wrapper autour de eco2ai pour mesure granulaire |
| | | • Tracking par extraction individuelle (pas seulement par script) |
| | | • Métriques collectées : temps CPU, RAM peak, kWh estimé, CO2e estimé |
| | | • Sortie : enrichir `Consumtion_of_Duraxell.csv` avec colonnes par méthode |
| | | • Calculer les ratios : coût Rules vs ML vs LLM par entité extraite |
| **12:30–13:30** | **Déjeuner + marche** | |
| **13:30–15:00** | **Bloc 4 : Connexion arbre → cascade** | |
| | | • Modifier `E_creation_arbre_decision.py` pour qu'il produise un fichier de configuration `decision_config.json` |
| | | • Ce fichier mappe chaque entité à sa méthode recommandée ET à un plan de cascade : |
| | | ```json |
| | | {"Estrogen_receptor": {"primary": "ML_CRF", "fallback": "Rules", "escalation": "LLM", "thresholds": {"confidence_min": 0.85}}} |
| | | ``` |
| | | • Le `CascadeOrchestrator` lit ce fichier pour configurer son comportement par entité |
| | | • Avantage : le comportement de la cascade est pilotée par les métriques, pas codé en dur |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : Test intégré cascade + énergie** | |
| | | • Créer `test_cascade.py` : exécuter la cascade sur les 7 entités sein |
| | | • Pour chaque entité, vérifier : |
| | | — La méthode primaire utilisée correspond à la recommandation de l'arbre |
| | | — Le coût énergétique est enregistré correctement |
| | | — L'escalade fonctionne quand la confiance est basse |
| | | • Produire un tableau résumé : entité | méthode | F1 | kWh | CO2e |
| | | • Comparer avec les résultats du poster de Berlin (Redjdal et al. 2024) |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Bilan semaine 1** | |
| | | • Rédiger `BILAN_SEMAINE1.md` |
| | | • Lister : ce qui est fait, ce qui reste, les problèmes identifiés |
| | | • Préparer les objectifs de la semaine 2 |
| | | • Commit et push : `"Cascade orchestrator + energy tracker + bilan S1"` |
| **18:00–19:00** | **Sport : marche longue** | 1h, parcours varié |
| 19:00–22:00 | Détente, repos | |
| 22:00 | Coucher | |

---

## PAUSE — 1, 2, 3 mars

### Dimanche 1er mars — Repos actif

| Heure | Activité |
|-------|----------|
| 8:00 | Réveil naturel (pas de réveil) |
| 9:00–10:30 | **Marche longue** (1h30, nature si possible, 8 000 pas) |
| 10:30–12:00 | Activité libre (lecture non-académique, musique, cuisine) |
| 12:00–13:00 | Déjeuner |
| 13:00–16:00 | Repos complet, sieste si besoin |
| 16:00–17:00 | **Marche légère** (30 min) |
| 17:00–21:00 | Activité libre |
| 22:00 | Coucher |

### Lundi 2 mars — Repos actif + lecture

| Heure | Activité |
|-------|----------|
| 8:00 | Réveil |
| 8:30–10:00 | **Marche matinale longue** (1h30) |
| 10:00–12:00 | Lecture de plaisir OU relecture légère de 2-3 articles clés (sans code) |
| 12:00–13:00 | Déjeuner |
| 13:00–15:00 | Repos |
| 15:00–16:00 | Préparation mentale semaine 2 : relire `BILAN_SEMAINE1.md` |
| 16:00–17:00 | **Marche** |
| 17:00–22:00 | Détente |
| 22:00 | Coucher |

### Mardi 3 mars — Repos actif + préparation

| Heure | Activité |
|-------|----------|
| 7:30 | Réveil (retour au rythme) |
| 8:00–9:00 | **Marche matinale** (retour au rythme de travail) |
| 9:00–10:30 | Relecture du code produit semaine 1 (lecture seule, pas de modifications) |
| 10:30–12:00 | Planification fine des journées Mar 4 → Dim 8 |
| 12:00–13:00 | Déjeuner |
| 13:00–14:00 | **Marche** |
| 14:00–16:00 | Lecture ciblée : documentation HuggingFace Transformers pour fine-tuning NER |
| 16:00–17:00 | Préparer les notebooks pour la semaine 2 (squelettes vides) |
| 17:00–22:00 | Détente |
| 22:00 | Coucher |

---

## SEMAINE 2 : PIPELINE NER, ÉVALUATION ET DOCUMENTATION (4–8 mars)

---

### Mercredi 4 mars — PIPELINE NER COMPLET

**Objectif du jour** : s'assurer que le pipeline NER (BRAT → CoNLL → Training → Inférence → Prédiction BRAT) fonctionne de bout en bout et est piloté par les décisions de l'arbre.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–8:00 | Réveil + marche matinale | |
| **8:15–9:45** | **Bloc 1 : Pipeline NER — Données** | |
| | | • Exécuter `1convert_brat_to_conll.py` : vérifier la conversion des annotations BRAT |
| | | • Compter les entités par type dans le CoNLL généré |
| | | • Vérifier le split train/val : ratio 80/20, stratifié par type d'entité |
| | | • Identifier les entités sous-représentées (< 30 occurrences) |
| | | • Croiser avec les décisions de l'arbre : les entités assignées à ML/Transformer ont-elles assez de données ? |
| 9:45–10:00 | Pause | |
| **10:00–11:30** | **Bloc 2 : Pipeline NER — Entraînement** | |
| | | • Auditer `2sweep_ner.py` : quels modèles sont testés (PubMedBERT, CancerBERT, CamemBERT-bio ?) |
| | | • Vérifier la configuration du sweep : learning rate, batch size, epochs |
| | | • Lancer un entraînement rapide (3 epochs) pour vérifier que le pipeline fonctionne |
| | | • Analyser `sweep_results.csv` : identifier le meilleur modèle par entité |
| | | • Comparer : les entités assignées à "NER Transformer" ont-elles les meilleurs F1 avec transformers ? |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : Pipeline NER — Inférence et prédiction** | |
| | | • Exécuter `3infer.py` avec le meilleur modèle sur les données de validation |
| | | • Exécuter `4predict_to_brat.py` : convertir les prédictions en format BRAT |
| | | • Comparer visuellement prédictions vs Gold Standard pour 3-5 documents |
| | | • Calculer F1-score par entité et comparer avec les métriques de l'arbre |
| **12:30–13:30** | **Déjeuner + marche** | |
| **13:30–15:00** | **Bloc 4 : Connexion NER → Cascade** | |
| | | • Modifier `cascade_orchestrator.py` pour appeler le vrai modèle NER (pas le stub) |
| | | • Implémenter la logique : si l'arbre recommande "NER Transformer" pour Ki67, le cascade_orchestrator charge le bon modèle |
| | | • Ajouter le scoring de confiance basé sur les probabilités softmax du modèle NER |
| | | • Tester : extraire Ki67 d'un document → passe par le transformer → résultat avec confiance |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : Connexion Rules → Cascade** | |
| | | • Auditer `Rules/src/biomarker_brat_annotator.py` et `Rules/src/lunch.py` |
| | | • Intégrer les regex existantes dans le `cascade_orchestrator` |
| | | • Pour les entités "Règles par défaut" (ex: Genetic_mutation) : |
| | | — Vérifier que les regex capturent bien les mutations EGFR, ALK, KRAS |
| | | — Ajouter des regex pour les mutations manquantes si nécessaire |
| | | • Tester : extraire Genetic_mutation → passe par Rules → résultat avec confiance |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Test intégré complet** | |
| | | • Exécuter la cascade sur un document complet avec toutes les entités |
| | | • Vérifier que chaque entité emprunte le bon chemin (Rules/ML/Transformer/LLM) |
| | | • Logger les résultats dans un tableau synthétique |
| | | • Commit : `"Pipeline NER intégré dans cascade DuraXELL"` |
| **18:00–19:00** | **Sport** | Marche rapide ou course légère 30 min + étirements |
| 19:00–22:00 | Détente | |
| 22:00 | Coucher | |

---

### Jeudi 5 mars — ÉVALUATION MULTI-CRITÈRES

**Objectif du jour** : évaluer le système complet sur les 3 axes du trilemme (Performance, Explicabilité, Énergie) et produire les résultats comparatifs.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–8:00 | Réveil + marche matinale | |
| **8:15–9:45** | **Bloc 1 : Benchmark Performance (F1)** | |
| | | • Exécuter la cascade sur TOUT le corpus de validation |
| | | • Calculer F1-score par entité, précision, rappel |
| | | • Produire la matrice de confusion par entité |
| | | • Comparer avec les résultats du poster ESMO (Redjdal et al. 2024 : F1=0.90 NER, 0.87 RE) |
| | | • Comparer avec le baseline "tout-règles" et "tout-transformer" |
| | | • Sauvegarder dans `Results/benchmark_performance.csv` |
| 9:45–10:00 | Pause | |
| **10:00–11:30** | **Bloc 2 : Benchmark Explicabilité** | |
| | | • Définir la métrique d'explicabilité formellement : |
| | | — Rules : explicabilité = 1.0 (regex traçable) |
| | | — ML-CRF : explicabilité = 0.7 (features interprétables via transitions CRF) |
| | | — Transformer : explicabilité = 0.3 (attention maps, sinon boîte noire) |
| | | — LLM : explicabilité = 0.1 (prompt traçable mais raisonnement opaque) |
| | | • Calculer le score d'explicabilité moyen pondéré par usage dans la cascade |
| | | • Comparer : cascade DuraXELL vs tout-transformer vs tout-LLM |
| | | • Sauvegarder dans `Results/benchmark_explainability.csv` |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : Benchmark Énergie** | |
| | | • Collecter les données eco2ai de chaque run |
| | | • Calculer le coût total par méthode : Rules (~0.001 kWh), ML (~0.01 kWh), Transformer (~0.1 kWh), LLM (~1 kWh) |
| | | • Calculer le coût total de la cascade vs alternatives monolithiques |
| | | • Vérifier l'hypothèse "80% par méthodes légères" : quel % d'entités est traité par Rules+ML ? |
| | | • Produire `Results/benchmark_energy.csv` |
| **12:30–13:30** | **Déjeuner + marche** | |
| **13:30–15:00** | **Bloc 4 : Score Composite Trilemme** | |
| | | • Implémenter le score composite : `Composite = α·F1 + β·Explicabilité + γ·(1 - Énergie_normalisée)` |
| | | • Tester avec α=0.4, β=0.3, γ=0.3 (pondération équilibrée) |
| | | • Tracer le front de Pareto : quelles configurations sont Pareto-optimales ? |
| | | • Valider que la cascade DuraXELL est sur ou proche du front de Pareto |
| | | • Produire les graphiques radar (spider chart) par configuration |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : Validation REST ↔ Arbre** | |
| | | • Exécuter `rest_decision_bridge.py` : comparer les décisions REST empiriques avec l'arbre |
| | | • Calculer le taux de concordance |
| | | • Identifier les cas de divergence et analyser pourquoi |
| | | • Si concordance > 80% → validation mutuelle réussie |
| | | • Si concordance < 80% → itérer sur les seuils de l'arbre |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Génération des figures** | |
| | | • Produire toutes les figures pour la publication : |
| | | — Fig 1 : Arbre de décision avec résultats par entité |
| | | — Fig 2 : Heatmap F1 par entité × méthode |
| | | — Fig 3 : Barplot comparatif énergie (cascade vs monolithique) |
| | | — Fig 4 : Radar trilemme |
| | | — Fig 5 : Concordance REST ↔ Arbre |
| | | • Sauvegarder dans `Results/figures/` |
| | | • Commit : `"Évaluation trilemme complète + figures"` |
| **18:00–19:00** | **Marche longue** | 1h, décompression |
| 19:00–22:00 | Détente | |
| 22:00 | Coucher | |

---

### Vendredi 6 mars — NOTEBOOK MAÎTRE ET REPRODUCTIBILITÉ

**Objectif du jour** : créer un notebook Jupyter maître (`commandes.ipynb` enrichi) qui exécute l'ensemble du pipeline de bout en bout, et assurer la reproductibilité complète.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–8:00 | Réveil + marche matinale | |
| **8:15–9:45** | **Bloc 1 : Notebook maître — Section 1 : Setup et données** | |
| | | • Enrichir `commandes.ipynb` (ou créer `DuraXELL_Pipeline.ipynb`) |
| | | • Section 1.1 : Installation des dépendances |
| | | • Section 1.2 : Chargement des données (annotations BRAT, corpus texte) |
| | | • Section 1.3 : Statistiques descriptives du corpus (nombre de documents, entités, distribution) |
| | | • Section 1.4 : Visualisation de la distribution des entités |
| | | • Chaque cellule doit être exécutable indépendamment |
| 9:45–10:00 | Pause | |
| **10:00–11:30** | **Bloc 2 : Notebook — Section 2 : Calcul des métriques** | |
| | | • Section 2.1 : Calcul de la Templateabilité (appel à `E_templeability.py`) |
| | | • Section 2.2 : Calcul de l'Homogénéité (appel à `E_homogeneity.py`) |
| | | • Section 2.3 : Calcul du Risque Contextuel (appel à `E_risk_context.py`) |
| | | • Section 2.4 : Calcul de la Fréquence (appel à `E_frequency.py`) |
| | | • Section 2.5 : Tableau récapitulatif des métriques par entité |
| | | • Affichage : heatmap des 4 métriques pour les 7+ entités |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : Notebook — Section 3 : Arbre de décision** | |
| | | • Section 3.1 : Exécution de l'arbre de décision |
| | | • Section 3.2 : Visualisation de l'arbre |
| | | • Section 3.3 : Tableau des recommandations par entité |
| | | • Section 3.4 : Analyse de sensibilité des seuils (faire varier TE_HIGH ± 0.1 et observer l'impact) |
| **12:30–13:30** | **Déjeuner + marche** | |
| **13:30–15:00** | **Bloc 4 : Notebook — Section 4 : Cascade et résultats** | |
| | | • Section 4.1 : Exécution de la cascade sur le corpus de validation |
| | | • Section 4.2 : Résultats Performance (F1, Précision, Rappel par entité) |
| | | • Section 4.3 : Résultats Énergie (kWh par méthode, comparaison) |
| | | • Section 4.4 : Résultats Explicabilité |
| | | • Section 4.5 : Score Composite Trilemme |
| | | • Section 4.6 : Validation croisée REST ↔ Arbre |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : README.md et documentation** | |
| | | • Créer `README.md` à la racine du projet avec : |
| | | — Description du projet DuraXELL |
| | | — Architecture du système (schéma ASCII) |
| | | — Instructions d'installation et d'exécution |
| | | — Résultats principaux (tableau F1 + énergie) |
| | | — Citation (Redjdal et al. 2024) |
| | | — Licence GPL-3.0 |
| | | • Mettre à jour `requirements.txt` avec toutes les dépendances exactes (versions pinées) |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Tests de reproductibilité** | |
| | | • Cloner le repo dans un dossier vide |
| | | • Installer les dépendances depuis `requirements.txt` |
| | | • Exécuter le notebook de bout en bout |
| | | • Vérifier que tous les résultats sont identiques |
| | | • Corriger les chemins relatifs si nécessaire |
| | | • Commit : `"Notebook maître + README + reproductibilité vérifiée"` |
| **18:00–19:00** | **Sport** | Marche rapide 45 min |
| 19:00–22:00 | Détente | |
| 22:00 | Coucher | |

---

### Samedi 7 mars — PRÉPARATION PUBLICATION FRUGALITÉ

**Objectif du jour** : préparer le matériel pour la soumission à la conférence "Frugalité" et structurer les résultats pour une publication.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–8:00 | Réveil + marche matinale | |
| **8:15–9:45** | **Bloc 1 : Structuration du résumé étendu** | |
| | | • Titre : *"Cascade intelligente Rules-ML-LLM pour l'extraction de biomarqueurs oncologiques : vers une méthodologie d'évaluation socio-écologiquement consciente"* |
| | | • Section 1 : Problématique (trilemme Performance-Explicabilité-Durabilité) |
| | | • Section 2 : Méthodologie (métriques Te/He/R/Freq → arbre → cascade) |
| | | • Section 3 : Résultats (F1 par entité, coût énergétique, score composite) |
| | | • Section 4 : Discussion (validation hypothèse 80%, concordance REST) |
| 9:45–10:00 | Pause | |
| **10:00–11:30** | **Bloc 2 : Rédaction du résumé (2 pages)** | |
| | | • Rédiger les 2 pages de résumé étendu selon le format de la conférence |
| | | • Intégrer les chiffres clés du benchmark de la veille |
| | | • Inclure 1 figure (arbre de décision ou radar trilemme) |
| | | • Inclure 1 tableau (résultats comparatifs cascade vs monolithique) |
| | | • Relecture critique : chaque phrase apporte-t-elle de l'information ? |
| 11:30–11:45 | Pause | |
| **11:45–12:30** | **Bloc 3 : Mise à jour de la présentation DuraXELL** | |
| | | • Mettre à jour les slides existantes avec les nouveaux résultats |
| | | • Ajouter la slide de l'arbre de décision avec résultats par entité |
| | | • Ajouter la slide du radar trilemme |
| | | • Ajouter la slide de concordance REST ↔ Arbre |
| **12:30–13:30** | **Déjeuner + marche** | |
| **13:30–15:00** | **Bloc 4 : Extension au cancer du poumon** | |
| | | • Définir les entités poumon : EGFR, ALK, ROS1, KRAS, BRAF, PD-L1, TNM_lung |
| | | • Calculer les métriques Te/He/R/Freq pour ces entités (si données disponibles) |
| | | • Sinon : définir les valeurs attendues théoriques basées sur la littérature |
| | | • Exécuter l'arbre de décision sur les entités poumon |
| | | • Documenter les résultats et les comparer avec les entités sein |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **Bloc 5 : Analyse de sensibilité** | |
| | | • Faire varier chaque seuil de l'arbre de ±10%, ±20% |
| | | • Observer l'impact sur les recommandations (combien d'entités changent de feuille) |
| | | • Identifier les seuils les plus sensibles vs les plus robustes |
| | | • Produire un graphique de sensibilité |
| | | • Documenter les résultats dans le notebook |
| 16:45–17:00 | Pause | |
| **17:00–18:00** | **Bloc 6 : Push final et nettoyage** | |
| | | • Nettoyer le code : supprimer les fichiers temporaires, les prints de debug |
| | | • Vérifier le `.gitignore` (pas de données patients, pas de modèles lourds) |
| | | • Commit final semaine 2 : `"Publication prep + extension poumon + analyse sensibilité"` |
| | | • Push vers GitHub |
| **18:00–19:00** | **Marche longue** | 1h de marche, bilan mental |
| 19:00–22:00 | Détente | |
| 22:00 | Coucher | |

---

### Dimanche 8 mars — CONSOLIDATION ET VISION

**Objectif du jour** : journée allégée. Consolider tout le travail, rédiger le bilan, et définir la roadmap post-vacances.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:30–8:30 | Réveil + marche matinale longue | 1h, rythme calme |
| 8:30–9:00 | Petit-déjeuner | |
| **9:00–10:30** | **Bloc 1 : Bilan global** | |
| | | • Rédiger `BILAN_VACANCES.md` avec : |
| | | — Ce qui a été accompli (checklist) |
| | | — Ce qui reste à faire |
| | | — Problèmes non résolus |
| | | — Décisions techniques prises et justifications |
| | | • Mettre à jour le README avec les résultats finaux |
| 10:30–10:45 | Pause | |
| **10:45–12:15** | **Bloc 2 : Roadmap post-vacances** | |
| | | • Définir les prochaines étapes : |
| | | — Court terme (mars) : validation sur données réelles AP-HP |
| | | — Moyen terme (avril-mai) : soumission conférence Frugalité |
| | | — Long terme (juin+) : extension multi-cancer, benchmarks multilingues |
| | | • Lister les données manquantes pour la suite (accès MIMIC-IV, données AP-HP) |
| | | • Identifier les collaborations nécessaires (Akram, Guillaume Bazin, AP-HP) |
| **12:15–13:30** | **Déjeuner + marche** | |
| **13:30–15:00** | **Bloc 3 : Email de synthèse à Dr. Redjdal** | |
| | | • Rédiger un email de synthèse pour Akram avec : |
| | | — Résumé des avancées (3-5 points clés) |
| | | — Résultats quantitatifs principaux |
| | | — Questions en suspens |
| | | — Proposition de réunion pour la semaine suivante |
| | | • Préparer 2-3 slides de synthèse rapide pour la réunion |
| 15:00 | **FIN DU TRAVAIL** | |
| 15:00–16:00 | **Marche** | |
| 16:00–22:00 | Repos complet, détente, préparation de la reprise | |
| 22:00 | Coucher | |

---

## Récapitulatif des livrables

| Livrable | Jour cible | Statut initial |
|----------|-----------|----------------|
| `AUDIT_24FEV.md` — état des lieux complet | 24 fév | À créer |
| Scripts `E_*.py` audités et testés | 25 fév | Existants → améliorés |
| `test_templeability.py`, `test_decision_tree.py` | 25-26 fév | À créer |
| `E_creation_arbre_decision.py` calibré + visualisation | 26 fév | Existant → raffiné |
| `visualize_decision_tree.py` | 26 fév | À créer |
| `REST_interface/` (3 scripts + demo) | 27 fév | À créer |
| `cascade_orchestrator.py` | 28 fév | À créer |
| `energy_tracker.py` | 28 fév | À créer |
| `decision_config.json` (config par entité) | 28 fév | À créer |
| Pipeline NER connecté à la cascade | 4 mars | Existant → intégré |
| `Results/benchmark_*.csv` (3 fichiers) | 5 mars | À créer |
| Figures publication (5 figures) | 5 mars | À créer |
| `DuraXELL_Pipeline.ipynb` — notebook maître | 6 mars | commandes.ipynb → enrichi |
| `README.md` complet | 6 mars | À créer |
| Résumé étendu conférence Frugalité (2 pages) | 7 mars | À créer |
| Extension entités poumon + analyse sensibilité | 7 mars | À créer |
| `BILAN_VACANCES.md` + roadmap post-vacances | 8 mars | À créer |

---

## Récapitulatif quotidien de l'activité physique

| Jour | Marche matin | Marche midi | Marche soir | Total estimé |
|------|-------------|-------------|-------------|--------------|
| 24 fév | 30 min | 30 min | 45 min | ~10 000 pas |
| 25 fév | 30 min | 45 min | 30 min | ~12 000 pas |
| 26 fév | 30 min | 30 min | 45 min | ~10 000 pas |
| 27 fév | 30 min | 1h | 30 min | ~13 000 pas |
| 28 fév | 30 min | 30 min | 1h | ~13 000 pas |
| 1 mars (pause) | 1h30 | — | 30 min | ~10 000 pas |
| 2 mars (pause) | 1h30 | — | 30 min | ~10 000 pas |
| 3 mars (pause) | 30 min | 1h | — | ~8 000 pas |
| 4 mars | 30 min | 30 min | 30 min + sport | ~12 000 pas |
| 5 mars | 30 min | 30 min | 1h | ~13 000 pas |
| 6 mars | 30 min | 30 min | 45 min | ~10 000 pas |
| 7 mars | 30 min | 30 min | 1h | ~13 000 pas |
| 8 mars | 1h | 30 min | 30 min | ~10 000 pas |

**Total estimé sur 13 jours : ~144 000 pas (~115 km)**

---

## Note méthodologique (HDR)

Ce planning a été construit selon trois principes directeurs :

1. **ESMO2025 comme colonne vertébrale** — Le dépôt n'est pas un composant annexe, c'est le projet DuraXELL lui-même. Chaque tâche part de l'existant dans ce repo, l'améliore, l'étend, le teste. Aucun développement "from scratch" n'est justifié quand du code fonctionnel existe déjà.

2. **REST-interface comme validation croisée** — Le projet de Guillaume Bazin n'est pas un concurrent de l'arbre de décision, il en est le miroir empirique. L'approche top-down (métriques calculées → arbre → décision) et l'approche bottom-up (annotation pilote → observation → décision) doivent converger. Le `rest_decision_bridge.py` est le composant qui formalise cette convergence.

3. **Progressivité cognitive** — Les jours de la semaine 1 suivent une montée en complexité (audit → métriques → arbre → REST → cascade). La pause de 3 jours permet la consolidation mémorielle. La semaine 2 se concentre sur l'intégration et l'évaluation, tâches qui requièrent une vision synthétique que la pause aura facilitée.
