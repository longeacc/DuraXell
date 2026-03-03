# DuraXELL : Sustainable Information Extraction for LLM en Cancérologie

DuraXELL est un pipeline d'extraction d'informations médicales (biomarqueurs) conçu pour optimiser le **Trilemme : Performance, Explicabilité, Frugalité**. Au lieu d'utiliser systématiquement des LLM très coûteux en énergie, DuraXELL utilise un arbre de décision pour router chaque entité vers la méthode la plus légère possible (Règles > ML > Transformer > LLM).

## Architecture en Cascade
```
<img width="750" height="628" alt="image" src="https://github.com/user-attachments/assets/a1eb2d82-b719-4ee3-9703-ca913cb9bef2" />

```

## Résultats Principaux (Front de Pareto)

| Biomarqueur | Méthode Recommandée | F1-Score | Énergie (kWh) | Score Composite |
|-------------|---------------------|----------|---------------|-----------------|
| ER          | Règles              | 0.95     | 0.000001      | 0.98            |
| Ki67        | ML_CRF              | 0.82     | 0.000050      | 0.85            |
| Grade       | Règles              | 0.70     | 0.000001      | 0.88            |
| PD-L1       | LLM                 | 0.96     | 0.015000      | 0.45            |

## Installation et Exécution Reproductible

1. **Cloner le dépôt** :

   ```bash
   git clone <url_du_repo>
   cd DuraXELL
   ```

2. **Créer un environnement virtuel et installer les dépendances** :

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Exécuter le pipeline complet** :
   Ouvrez et exécutez le notebook maître :

   ```bash
   jupyter notebook Reports/DuraXELL_Pipeline.ipynb
   ```

   Ou exécutez le script de rapport :

   ```bash
   python run_full_pipeline_report.py
   ```

## Références et Citation

Ce travail s'appuie sur les recherches de **Redjdal et al. 2024** concernant l'extraction d'informations en oncologie et l'évaluation de la frugalité des modèles de langage.

**Citation :**
> Redjdal, C., et al. (2024). *Le juste usage des LLM et méthode NLP en cancérologie : Vers une approche frugale et explicable*. ESIEE Paris.

