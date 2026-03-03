# Architecture du module ESMO2025

Ce document résume le rôle de chaque fichier et fonction dans le pipeline d'analyse NLP.

## 1. Scripts d'Analyse (Cœur Logique)

### `templeability.py`
**But :** Calcule le score de "Templeabilité" ($Te$) qui mesure la régularité structurelle des entités.
*   **`parse_ann_file(ann_path)`** : Lit les fichiers d'annotations `.ann` (format BRAT) pour extraire les entités textuelles.
*   **`load_all_documents()`** : Parcourt récursivement les dossiers de données (Gold Standard et Prédictions), charge les annotations et dédoublonne les fichiers par nom.
*   **`analyze_pattern_complexity(values, entity_type)`** : Fonction centrale.
    *   Normalise les valeurs (ex: "HER2 3+" $\rightarrow$ "XXXD D+").
    *   Identifie les motifs dominants.
    *   Calcule le score $Te$ basé sur la couverture des motifs, la diversité des valeurs, et les bonus sémantiques (présence de %, de mots-clés fixes).
*   **`generate_report()`** : Lance l'analyse pour toutes les entités trouvées.
*   **`save_report_to_json/csv`** : Sauvegarde les résultats bruts.

### `risk_context.py`
**But :** Évalue le "Risque Contextuel" ($R$), la probabilité qu'une valeur soit ambiguë sans son contexte.
*   **`parse_ann_file(ann_path)`** : Extraction des mentions textuelles depuis les fichiers `.ann`.
*   **`calculate_risk_score(values, entity_type)`** : Analyse chaque mention pour la classer :
    *   *Haut Risque* : Termes polysémiques ("Positif", "Score 3") ou chiffres nus ("10%").
    *   *Faible Risque* : Mentions "auto-décrites" contenant le nom du biomarqueur (ex: "HER2 Positif") ou formats structurés complexes ("pT2N0").
*   **`run_analysis(output_dir)`** : Exécute l'analyse globale, trie les entités par risque décroissant et génère les fichiers de résultats `risk_context_full.json`.

### `homogeneity.py`
**But :** Calcule l'Homogénéité Linguistique ($He$) mesurant la redondance du vocabulaire.
*   **`tokenize(text)`** : Découpe le texte en mots simples.
*   **`calculate_word_stats(entities_values)`** : Compte le nombre total de mots ($Te_{words}$) et de mots uniques ($Ue_{words}$).
*   **`run_homogeneity_analysis()`** : 
    *   Récupère les données de `templeability.py`.
    *   Applique la formule $He = \frac{Te - Ue}{Te}$.
    *   Transforme le résultat via une fonction Sigmoïde pour obtenir un score normalisé.
*   **`generate_html(...)`** : Génère le rapport HTML spécifique à l'homogénéité (inclus directement dans ce fichier d'analyse).

---

## 2. Générateurs de Rapports (Visualisation HTML)

### `generate_templeability_report.py`
**But :** Créer une vue HTML riche pour les résultats de templeabilité.
*   **`generate_html_report(json_file, csv_file, output_file)`** :
    *   Lit `templeability_analysis.json`.
    *   Restaure les métriques détaillées (Couverture, Diversité, Fréquence).
    *   Génère le HTML avec les styles CSS (dégradés violets), les barres de progression, et les listes déroulantes d'échantillons ("Sample Values").
    *   Inclut la section méthodologie complète.

### `generate_risk_context_report.py`
**But :** Créer la vue HTML pour le risque contextuel.
*   **`generate_html_report(json_file, csv_file, output_file)`** :
    *   Lit `risk_context_full.json`.
    *   Trie les entités par score de risque.
    *   Applique le code couleur (Rouge=Haut Risque, Vert=Faible Risque).
    *   Ajoute les explications pédagogiques (notamment "Pourquoi mon score est de 0 ?").

### `generate_homogeneity_report.py`
**But :** Script utilitaire pour régénérer le rapport HTML d'homogénéité indépendamment du calcul.
*   **`generate_html_report(csv_file, output_file)`** :
    *   Lit le fichier CSV `homogeneity_analysis.csv`.
    *   Produit le tableau HTML comparatif (Homogénéité vs Templeabilité) avec les formules mathématiques visibles.

---

## 3. Données & Structure
Les scripts sont configurés pour lire une **liste unifiée de répertoires** située dans `ESMO2025/Rules/src/Breast`, incluant à la fois les données "Gold Standard" (Validation) et les Prédictions, avec une priorité donnée aux fichiers GS pour éviter les doublons.
