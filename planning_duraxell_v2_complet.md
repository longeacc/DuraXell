# Planning DuraXELL — Édition Complète Sans Contrainte de Temps
## Version HDR — Itération 2 (Auto-évaluée et corrigée)

> **Nota bene (auto-correction v2)** : La version précédente traitait encore le calendrier comme une variable contraignante. Cette version adopte une posture différente : *le temps n'est pas une ressource à optimiser, c'est un espace à habiter*. Chaque journée est planifiée pour être soutenable sur le long terme, avec une qualité d'implémentation qui ne sacrifie rien à la vitesse.

---

# PARTIE I — STRUCTURE COMPLÈTE DU PROJET : FICHIER PAR FICHIER

## Décision architecturale fondamentale (niveau HDR)

**ESMO2025 n'est pas un composant de DuraXELL. ESMO2025 EST DuraXELL.**

Le dépôt `longeacc/ESMO2025` contient déjà : les métriques fondamentales (Te, He, R, Freq), l'arbre de décision opérationnel (`E_creation_arbre_decision.py`), le pipeline NER complet (BRAT → CoNLL → Training → Inférence → BRAT), et le système de règles. Toute l'architecture décrite ci-dessous *part de ce qui existe* et l'enrichit. Le projet de Guillaume Bazin (REST-interface) est intégré non pas comme un module externe mais comme une **couche de validation empirique bottom-up**, miroir de l'approche top-down des métriques.

---

## Arborescence complète du projet

```
ESMO2025/                                          ← RACINE DuraXELL
│
├── README.md                                      ← À CRÉER — documentation maître
├── ARCHITECTURE_RECAP.md                          ← EXISTANT — à enrichir
├── AUDIT_24FEV.md                                 ← À CRÉER (J1)
├── BILAN_VACANCES.md                              ← À CRÉER (dernier jour)
├── requirements.txt                               ← À UNIFIER (virtualenv duraxell)
├── .gitignore                                     ← EXISTANT — à vérifier
├── decision_config.json                           ← À CRÉER — config seuils par entité
├── Consumtion_of_Duraxell.csv                     ← EXISTANT — suivi eco2ai
├── breast_cancer_biomarker_eval_summary.csv       ← EXISTANT
│
├── ESMO2025/                                      ← MODULE PRINCIPAL — métriques + décision
│   ├── __init__.py                                ← À CRÉER — exports des classes publiques
│   │
│   ├── E_templeability.py                         ← EXISTANT — métrique Te
│   ├── E_homogeneity.py                           ← EXISTANT — métrique He
│   ├── E_risk_context.py                          ← EXISTANT — métrique R
│   ├── E_frequency.py                             ← EXISTANT — métrique Freq
│   ├── E_annotation_yield.py                      ← À CRÉER — métrique rendement annotation
│   ├── E_fesability_NER.py                        ← EXISTANT — score de faisabilité (à compléter)
│   ├── E_creation_arbre_decision.py               ← EXISTANT — arbre de décision (à raffiner)
│   ├── E_composite_scorer.py                      ← À CRÉER — score composite trilemme
│   │
│   ├── cascade_orchestrator.py                    ← À CRÉER — orchestre Rules→ML→LLM
│   ├── energy_tracker.py                          ← À CRÉER — mesure kWh/CO2 par appel
│   ├── visualize_decision_tree.py                 ← À CRÉER — visualisation arbre
│   ├── sensitivity_analysis.py                    ← À CRÉER — analyse sensibilité seuils
│   │
│   ├── tests/                                     ← À CRÉER
│   │   ├── __init__.py
│   │   ├── test_templeability.py                  ← Tests unitaires Te
│   │   ├── test_homogeneity.py                    ← Tests unitaires He
│   │   ├── test_risk_context.py                   ← Tests unitaires R
│   │   ├── test_frequency.py                      ← Tests unitaires Freq
│   │   ├── test_annotation_yield.py               ← Tests unitaires Yield
│   │   ├── test_decision_tree.py                  ← Tests intégration arbre (7 entités sein)
│   │   ├── test_cascade.py                        ← Tests intégration cascade
│   │   └── test_rest_bridge.py                    ← Tests concordance REST ↔ arbre
│   │
│   └── REST_interface/                            ← INTÉGRATION Guillaume Bazin
│       ├── __init__.py
│       ├── rest_annotator.py                      ← Outil annotation pilote ~40 dossiers
│       ├── rest_evaluator.py                      ← Boucle évaluation par entité
│       ├── rest_decision_bridge.py                ← Pont REST ↔ arbre de décision
│       ├── rest_pipeline.py                       ← Pipeline complet REST (driver)
│       ├── yield_calculator.py                    ← Calcul annotation_yield empirique
│       ├── convergence_analyzer.py                ← Analyse divergences REST vs arbre
│       ├── demo_rest.py                           ← Script de démonstration
│       └── templates/
│           ├── annotation_template.html           ← Interface highlighting
│           ├── evaluation_form.html               ← Formulaire évaluation expert
│           └── results_dashboard.html             ← Dashboard résultats
│
├── NER/
│   ├── data/
│   │   ├── Breast/
│   │   │   ├── train/                             ← Annotations BRAT (*.ann + *.txt)
│   │   │   ├── val/
│   │   │   └── test/
│   │   └── Lung/                                  ← À CRÉER — extension poumon
│   │       ├── train/
│   │       ├── val/
│   │       └── test/
│   ├── models/
│   │   ├── best_model/                            ← Meilleur modèle entraîné
│   │   └── sweep_results.csv                      ← EXISTANT — résultats hyperparameter sweep
│   └── src/
│       ├── 1convert_brat_to_conll.py              ← EXISTANT
│       ├── 2sweep_ner.py                          ← EXISTANT
│       ├── 3infer.py                              ← EXISTANT
│       ├── 4predict_to_brat.py                    ← EXISTANT
│       ├── 5evaluate_ner.py                       ← À CRÉER — évaluation complète par entité
│       └── ner_cascade_connector.py               ← À CRÉER — connecteur NER → cascade
│
├── Rules/
│   └── src/
│       ├── Breast/
│       │   ├── biomarker_brat_annotator.py        ← EXISTANT
│       │   ├── rules_evaluator.py                 ← EXISTANT ou À CRÉER
│       │   └── rules_cascade_connector.py         ← À CRÉER
│       └── Lung/                                  ← À CRÉER — extension poumon
│           ├── lung_biomarker_rules.py
│           └── lung_rules_evaluator.py
│
├── Results/
│   ├── benchmark_performance.csv                  ← À CRÉER (J-évaluation)
│   ├── benchmark_explainability.csv               ← À CRÉER
│   ├── benchmark_energy.csv                       ← À CRÉER
│   ├── benchmark_cascade_vs_mono.csv              ← À CRÉER
│   ├── sensitivity_output.csv                     ← À CRÉER
│   ├── figures/
│   │   ├── decision_tree_visualization.png        ← À CRÉER
│   │   ├── radar_trilemma.png                     ← À CRÉER
│   │   ├── benchmark_comparison.png               ← À CRÉER
│   │   ├── sensitivity_analysis.png               ← À CRÉER
│   │   └── rest_convergence_plot.png              ← À CRÉER
│   └── REST_results/
│       ├── annotation_yield_by_entity.json        ← À CRÉER
│       └── convergence_tree_vs_rest.json          ← À CRÉER
│
└── reports/
    ├── DuraXELL_Pipeline.ipynb                    ← À CRÉER (évolution de commandes.ipynb)
    ├── conference_frugalite_abstract.md            ← À CRÉER
    ├── conference_frugalite_slides.pptx            ← À CRÉER
    └── BILAN_VACANCES.md                          ← À CRÉER
```

---

## Description détaillée fichier par fichier

### `README.md`

**Rôle** : Documentation maître du projet DuraXELL / ESMO2025.

**Contenu attendu** :
```markdown
# DuraXELL — Cascade intelligente pour l'extraction de biomarqueurs oncologiques

## Contexte
[Description du trilemme Performance-Explicabilité-Énergie]
[Position dans le projet de thèse CIFRE Sorbonne 2027-2030]

## Architecture
[Schéma ASCII de la cascade Rules→ML→LLM]
[Schéma de l'arbre de décision]

## Installation
pip install -r requirements.txt

## Utilisation
# Calcul des métriques
python ESMO2025/E_templeability.py --input data/corpus.json --output templeability.json
# Arbre de décision
python ESMO2025/E_creation_arbre_decision.py --config decision_config.json
# Cascade complète
python ESMO2025/cascade_orchestrator.py --document data/report.txt --entity all

## Résultats
[Tableau F1 par entité]
[Coût énergétique comparatif]
[Score composite trilemme]

## Référence
Redjdal et al. (2024) — ESMO Congress Berlin
```

---

### `decision_config.json`

**Rôle** : Fichier de configuration généré par `E_creation_arbre_decision.py`. Pilote le comportement de `cascade_orchestrator.py` pour chaque entité.

**Structure** :
```json
{
  "version": "2.0",
  "generated_at": "2026-02-26T10:00:00",
  "global_thresholds": {
    "TE_HIGH": 0.5,
    "TE_LOW": 0.2,
    "HE_HIGH": 0.6,
    "RISK_LOW": 0.3,
    "FREQ_SUFFICIENT": 0.001,
    "YIELD_MIN": 0.7
  },
  "entities": {
    "Estrogen_receptor": {
      "primary_method": "ML_CRF",
      "fallback_method": "Rules",
      "escalation_method": "LLM",
      "confidence_threshold": 0.85,
      "metrics": {
        "Te": 0.72,
        "He": 0.81,
        "R": 0.15,
        "Freq": 0.023,
        "Yield": 0.88
      },
      "leaf": "ML_LEGER_NER"
    },
    "HER2_FISH": {
      "primary_method": "LLM",
      "fallback_method": null,
      "escalation_method": null,
      "confidence_threshold": 0.75,
      "metrics": {
        "Te": 0.18,
        "He": 0.29,
        "R": 0.82,
        "Freq": 0.003,
        "Yield": 0.41
      },
      "leaf": "NER_LLM"
    },
    "Genetic_mutation": {
      "primary_method": "Rules",
      "fallback_method": "ML_CRF",
      "escalation_method": null,
      "confidence_threshold": 0.90,
      "metrics": {
        "Te": 0.91,
        "He": 0.89,
        "R": 0.05,
        "Freq": 0.018,
        "Yield": 0.95
      },
      "leaf": "REGLES_PAR_DEFAUT"
    }
  }
}
```

---

### `ESMO2025/__init__.py`

**Rôle** : Exporter les interfaces publiques du module ESMO2025.

```python
"""
DuraXELL / ESMO2025
===================
Module principal d'extraction de biomarqueurs oncologiques
par cascade intelligente Rules→ML→LLM.

Exports principaux :
- TempleabilityScorer : calcul de la métrique Te
- HomogeneityScorer : calcul de la métrique He
- RiskContextScorer : calcul de la métrique R
- FrequencyScorer : calcul de la métrique Freq
- AnnotationYieldScorer : calcul du rendement annotation
- DecisionTree : arbre de décision 6-critères
- CascadeOrchestrator : orchestrateur Rules→ML→LLM
- EnergyTracker : suivi consommation énergétique
"""

from .E_templeability import TempleabilityScorer
from .E_homogeneity import HomogeneityScorer
from .E_risk_context import RiskContextScorer
from .E_frequency import FrequencyScorer
from .E_annotation_yield import AnnotationYieldScorer
from .E_creation_arbre_decision import DecisionTree
from .cascade_orchestrator import CascadeOrchestrator
from .energy_tracker import EnergyTracker
from .E_composite_scorer import CompositeScorer

__version__ = "2.0.0"
__all__ = [
    "TempleabilityScorer", "HomogeneityScorer", "RiskContextScorer",
    "FrequencyScorer", "AnnotationYieldScorer", "DecisionTree",
    "CascadeOrchestrator", "EnergyTracker", "CompositeScorer"
]
```

---

### `ESMO2025/E_templeability.py` (Existant — à auditer et raffiner)

**Rôle** : Calcule le score de Templateabilité (Te) pour chaque entité biomédicale. Te mesure le degré de prédictibilité structurelle des patterns d'expression d'une entité dans le corpus clinique.

**API attendue après raffinement** :
```python
class TempleabilityScorer:
    def __init__(self, corpus: list[dict]):
        """
        Args:
            corpus: liste de documents annotés {text: str, annotations: list[BratAnnotation]}
        """

    def compute(self, entity_type: str) -> float:
        """
        Retourne un score Te ∈ [0, 1].
        Te élevé (> 0.5) → patterns réguliers, prévisibles → candidat Règles.
        Te faible (< 0.2) → haute variabilité → candidat LLM.

        Méthode :
        1. Extraire toutes les mentions de entity_type dans le corpus
        2. Normaliser les patterns : "HER2 3+" → "XXX D+" (regex abstraction)
        3. Calculer l'entropie de la distribution des patterns normalisés
        4. Te = 1 - (entropie_normalisée) + bonus_sémantique
        """

    def normalize_pattern(self, text: str) -> str:
        """Normalise un texte d'entité en template abstrait."""

    def compute_all(self) -> dict[str, float]:
        """Calcule Te pour toutes les entités du corpus."""

    def to_json(self, output_path: str) -> None:
        """Sauvegarder les résultats dans templeability_analysis.json"""
```

**Points de raffinement identifiés** :
- Vérifier l'exhaustivité de la normalisation regex (cas "HER2 3+", "ER >80%", "Ki67 15-20%")
- Ajouter test unitaire : TNM ("T2N1M0") devrait avoir Te > 0.8
- Ajouter test unitaire : texte libre ("mutation probablement activatrice") devrait avoir Te < 0.2
- Calibrer le bonus sémantique (termes standardisés SNOMED/LOINC)

---

### `ESMO2025/E_homogeneity.py` (Existant — à auditer et raffiner)

**Rôle** : Calcule le score d'Homogénéité (He). He mesure la redondance linguistique : une entité avec He élevé est exprimée de manière quasi-identique à chaque occurrence.

**Formule** : `He = (Te_words - Ue_words) / Te_words` avec normalisation sigmoïde.

**Points de raffinement** :
- Vérifier le cas limite : entité avec 1 seule occurrence (He = 1.0 par convention ou 0.0 ?)
- Vérifier la cohérence avec Te : si Te élevé ET He élevé → score de faisabilité Rules optimal
- Calibrer la fonction sigmoïde : paramètre k (pente) et x₀ (point d'inflexion)
- Test canonique : "ER positif 80%" répété 100 fois → He doit être proche de 1.0

---

### `ESMO2025/E_risk_context.py` (Existant — à auditer et raffiner)

**Rôle** : Calcule le score de Risque Contextuel (R). R mesure la complexité du contexte linguistique entourant l'entité : négations, incertitudes, conflits, ambiguïtés.

**Points de raffinement** :
- Ajouter détection de négation : patterns "non", "ne pas", "absent", "négatif" dans fenêtre ±3 tokens
- Ajouter détection d'incertitude : "probable", "possible", "à confirmer", "suspecté"
- Ajouter détection de contradiction : entité positive ET négative dans le même document
- Test critique : "HER2 non surexprimé" → R devrait être **moyen** (négation simple bien définie)
- Test critique : "statut HER2 discordant entre biopsie et pièce opératoire" → R devrait être **élevé**

---

### `ESMO2025/E_frequency.py` (Existant — à auditer et raffiner)

**Rôle** : Calcule la fréquence relative (Freq) de chaque entité dans le corpus.

**Points de raffinement** :
- Vérifier le calcul : Freq = (nb_occurrences_entité) / (nb_total_tokens_corpus) ou / (nb_documents) ?
- Calibrer le seuil `FREQ_SUFFICIENT=0.001` : à ajuster selon la taille réelle du corpus
- Identifier les entités rares (< 10 occurrences) : décision automatique → LLM ou Règles par défaut
- Produire l'histogramme de distribution des fréquences (logarithmique)

---

### `ESMO2025/E_annotation_yield.py` (À créer)

**Rôle** : Calcule le rendement d'annotation (Yield) — métrique manquante dans la version actuelle de l'arbre.

**Définition** : `Yield = (nb_annotations_concordantes_GS_pred) / (nb_annotations_GS_total)` — qualité des annotations existantes relativement à un Gold Standard ou à une annotation de référence. En l'absence de données temporelles, Yield peut être estimé via le F1-score des règles sur le corpus annoté.

```python
class AnnotationYieldScorer:
    """
    Calcule le rendement d'annotation pour chaque type d'entité.
    
    Le yield mesure la proportion d'annotations correctement capturées
    par les méthodes légères (règles) sur l'ensemble du corpus annoté.
    Un yield élevé indique que les patterns de l'entité sont réguliers
    et bien capturés par des règles simples.
    """

    def __init__(self, corpus: list[dict], rules_engine=None):
        """
        Args:
            corpus: annotations BRAT (Gold Standard)
            rules_engine: moteur de règles pour comparaison
        """

    def compute(self, entity_type: str) -> float:
        """
        Retourne Yield ∈ [0, 1].
        
        Si rules_engine fourni :
            Yield = F1(rules_predictions, gold_standard) pour entity_type
        Sinon (proxy) :
            Yield = nb_patterns_captures_par_regex / nb_total_annotations
        """

    def compute_from_timing(self, annotation_times: dict, quality_scores: dict) -> float:
        """
        Calcule un yield temporel si des données de temps d'annotation sont disponibles.
        Yield_temp = qualité / (temps_normalisé)
        """
```

---

### `ESMO2025/E_creation_arbre_decision.py` (Existant — à raffiner seuils + yield)

**Rôle** : Construit et exécute l'arbre de décision à 6 critères. Génère `decision_config.json` et `output_decision.txt`.

**Structure de l'arbre (6 critères, 6 feuilles)** :
```
Racine
├── [1] Te > TE_HIGH ?
│   ├── OUI → [2] He > HE_HIGH ?
│   │          ├── OUI → [3] Yield > YIELD_MIN ?
│   │          │           ├── OUI → 🌿 RÈGLES PAR DÉFAUT
│   │          │           └── NON → 🌿 NER RÈGLES
│   │          └── NON → 🌿 ML LÉGER DÉFAUT
│   └── NON → [4] Te > TE_LOW ?
│              ├── OUI → [5] R < RISK_LOW ?
│              │           ├── OUI → [6] Freq > FREQ_SUFFICIENT ?
│              │           │           ├── OUI → 🌿 ML LÉGER NER
│              │           │           └── NON → 🌿 NER RÈGLES
│              │           └── NON → 🌿 NER TRANSFORMER
│              └── NON → 🌿 NER LLM
```

**Raffinements à apporter** :
- Intégrer le critère Yield dans les nœuds 1-3 (actuellement absent)
- Ajouter la génération de `decision_config.json` (maps entité → méthode + thresholds)
- Ajouter la visualisation graphique (appel à `visualize_decision_tree.py`)
- Calibrer les seuils par analyse de distribution empirique sur le corpus existant
- Documenter la justification statistique de chaque seuil dans `THRESHOLDS_JUSTIFICATION.md`

**Sorties attendues** :
- `output_decision.txt` : recommandation textuelle par entité
- `decision_config.json` : configuration machine-lisible pour la cascade
- `decision_tree_visualization.png` : figure pour publication

---

### `ESMO2025/E_composite_scorer.py` (À créer)

**Rôle** : Calcule le score composite du trilemme Performance-Explicabilité-Énergie.

```python
class CompositeScorer:
    """
    Évalue chaque configuration (méthode × entité) sur 3 axes :
    - Performance : F1-score sur corpus de validation
    - Explicabilité : score qualitatif (Rules=1.0, CRF=0.7, Transformer=0.3, LLM=0.1)
    - Énergie : coût normalisé (kWh / extraction)
    
    Score composite : C = α·F1 + β·Expl + γ·(1 - E_norm)
    Valeurs par défaut : α=0.4, β=0.3, γ=0.3
    """

    EXPLAINABILITY_SCORES = {
        "Rules": 1.0,
        "ML_CRF": 0.7,
        "Transformer": 0.3,
        "LLM": 0.1
    }

    def compute(self, f1: float, method: str, energy_kwh: float,
                alpha: float = 0.4, beta: float = 0.3, gamma: float = 0.3) -> float:
        """Calcule le score composite pour une extraction."""

    def pareto_analysis(self, results: pd.DataFrame) -> pd.DataFrame:
        """Identifie les configurations Pareto-optimales (F1, Expl, -Énergie)."""

    def radar_plot(self, results: pd.DataFrame, output_path: str) -> None:
        """Génère le graphique radar (spider chart) pour la publication."""
```

---

### `ESMO2025/cascade_orchestrator.py` (À créer — pièce maîtresse)

**Rôle** : Orchestrateur central de la cascade Rules → ML-CRF → Transformer → LLM. Lit `decision_config.json` pour configurer le comportement par entité.

```python
class CascadeOrchestrator:
    """
    Orchestrateur principal de DuraXELL.
    
    Pour chaque document et chaque type d'entité :
    1. Consulte decision_config.json → méthode primaire recommandée
    2. Tente l'extraction avec la méthode primaire
    3. Si confiance < seuil → tente le fallback
    4. Si confiance < seuil_critique → escalade vers LLM
    5. Enregistre : entité, valeur, méthode_utilisée, confiance, kWh, niveau_cascade
    """

    def __init__(
        self,
        config_path: str = "decision_config.json",
        rules_engine=None,          # RulesCascadeConnector
        ner_model=None,             # NERCascadeConnector
        llm_client=None,            # LLMClient (Mistral/DeepSeek)
        energy_tracker=None         # EnergyTracker
    ):
        ...

    def extract(
        self,
        document: str,
        entity_type: str
    ) -> ExtractionResult:
        """
        Point d'entrée principal.
        Retourne un ExtractionResult avec :
        - entity_type: str
        - value: str | None
        - span: tuple[int, int] | None
        - method_used: str ("Rules" | "ML_CRF" | "Transformer" | "LLM")
        - confidence: float
        - energy_kwh: float
        - cascade_level: int (1=Rules, 2=ML, 3=Transformer, 4=LLM)
        - execution_time_ms: float
        """

    def extract_all(self, document: str) -> list[ExtractionResult]:
        """Extrait toutes les entités configurées d'un document."""

    def extract_batch(
        self,
        documents: list[str],
        entity_types: list[str] | None = None
    ) -> pd.DataFrame:
        """Traitement par lot — retourne un DataFrame de résultats."""

    def _try_rules(self, text: str, entity_type: str) -> ExtractionResult:
        """Tente l'extraction par règles regex."""

    def _try_ml(self, text: str, entity_type: str) -> ExtractionResult:
        """Tente l'extraction par modèle ML-CRF."""

    def _try_transformer(self, text: str, entity_type: str) -> ExtractionResult:
        """Tente l'extraction par modèle Transformer (PubMedBERT/CancerBERT)."""

    def _try_llm(self, text: str, entity_type: str) -> ExtractionResult:
        """Appelle le LLM en dernier recours — mesure précise de l'énergie."""

    def _evaluate_confidence(self, result: ExtractionResult) -> float:
        """Calcule le score de confiance selon la méthode utilisée."""
```

---

### `ESMO2025/energy_tracker.py` (À créer)

**Rôle** : Wrapper autour de eco2ai pour mesure granulaire par extraction individuelle.

```python
class EnergyTracker:
    """
    Suivi de la consommation énergétique à granularité fine.
    Mesure le kWh et CO2e pour chaque extraction individuelle.
    
    Complète Consumtion_of_Duraxell.csv avec colonnes par méthode.
    """

    REFERENCE_COSTS_KWH = {
        "Rules": 1e-6,          # regex : ~0.000001 kWh/extraction
        "ML_CRF": 1e-5,         # CRF : ~0.00001 kWh
        "Transformer": 1e-4,    # BERT : ~0.0001 kWh
        "LLM_7B": 1e-3,         # LLM local 7B : ~0.001 kWh
        "LLM_API": 1e-2         # LLM API (Mistral/GPT) : ~0.01 kWh
    }

    def __init__(self, output_csv: str = "Consumtion_of_Duraxell.csv"):
        self.tracker = eco2ai.Tracker(...)

    @contextmanager
    def measure(self, method: str, entity_type: str):
        """Context manager : mesure kWh et CO2e d'un bloc de code."""

    def log(self, method: str, entity_type: str, kwh: float,
            co2_g: float, duration_ms: float) -> None:
        """Enregistre une mesure dans le CSV."""

    def summary(self) -> pd.DataFrame:
        """Retourne un résumé agrégé par méthode."""

    def cost_ratio(self, method_a: str, method_b: str) -> float:
        """Calcule le ratio de coût entre deux méthodes."""
```

---

### `ESMO2025/visualize_decision_tree.py` (À créer)

**Rôle** : Génère une visualisation graphique de l'arbre de décision pour la publication et la présentation.

```python
def visualize_decision_tree(
    decision_config: dict,
    entity_results: dict,
    output_path: str = "Results/figures/decision_tree_visualization.png",
    format: str = "png"  # "png" | "svg" | "pdf"
) -> None:
    """
    Génère une figure de l'arbre de décision avec :
    - Nœuds de décision colorés en bleu (#2196F3)
    - Feuilles colorées par méthode :
        * Règles → vert (#4CAF50)
        * ML-CRF → jaune (#FFC107)
        * Transformer → orange (#FF9800)
        * LLM → rouge (#F44336)
    - Seuils affichés sur chaque branche (TE_HIGH=0.5, etc.)
    - Entités assignées listées dans chaque feuille
    - Score composite affiché sous chaque entité
    """
```

---

### `ESMO2025/sensitivity_analysis.py` (À créer)

**Rôle** : Analyse de sensibilité des seuils de l'arbre de décision.

```python
def run_sensitivity_analysis(
    corpus: list[dict],
    base_config: dict,
    thresholds_to_vary: list[str] = ["TE_HIGH", "TE_LOW", "HE_HIGH", "RISK_LOW"],
    perturbation_pct: list[float] = [-0.2, -0.1, 0.1, 0.2]
) -> pd.DataFrame:
    """
    Pour chaque seuil × chaque perturbation :
    1. Recalcule les décisions de l'arbre
    2. Compte combien d'entités changent de feuille
    3. Mesure l'impact sur le score composite
    
    Retourne un DataFrame avec colonnes :
    threshold | perturbation | n_entities_changed | delta_composite | robustness_score
    """
```

---

### `ESMO2025/REST_interface/rest_annotator.py` (À créer)

**Rôle** : Outil d'annotation pilote inspiré de la méthodologie REST de Guillaume Bazin. Permet d'annoter ~40 dossiers patients avec le paradigme "highlighting" (simulation du regard expert).

```python
class RESTAnnotator:
    """
    Outil d'annotation pilote selon la méthodologie REST.
    
    Paradigme "highlighting" :
    - Affiche un CR clinique → l'annotateur surligne les biomarqueurs
    - Mesure le temps par document
    - Produit des annotations BRAT compatibles avec Rules/src/Breast/
    - Calcule automatiquement l'annotation_yield par entité
    
    Objectif : réduire le temps d'annotation de 15-20 min → 3-5 min par CR.
    """

    def annotate_batch(
        self,
        documents: list[str],
        n_pilot: int = 40,
        mode: str = "highlighting"  # "highlighting" | "brat_classic"
    ) -> list[BratAnnotation]:
        """
        Annote un lot de documents.
        Mesure le temps par document pour le calcul du yield temporel.
        """

    def export_to_brat(self, annotations: list[BratAnnotation],
                       output_dir: str) -> None:
        """Exporte en format .ann compatibles avec le pipeline NER existant."""
```

---

### `ESMO2025/REST_interface/rest_evaluator.py` (À créer)

**Rôle** : Boucle d'évaluation par entité — analyse empirique bottom-up des annotations pilotes.

```python
class RESTEvaluator:
    """
    Analyse empirique des annotations pilotes.
    
    Pour chaque entité annotée, calcule :
    - Nombre de patterns uniques observés → proxy pour Te empirique
    - Variabilité lexicale (TTR Token-Type Ratio) → proxy pour He empirique
    - Complexité contextuelle (présence négation/incertitude) → proxy pour R empirique
    
    Ces métriques empiriques sont comparées aux métriques calculées (E_*.py)
    dans rest_decision_bridge.py.
    """

    def evaluate_entity(
        self,
        entity_type: str,
        annotations: list[BratAnnotation],
        context_window: int = 5
    ) -> RESTEntityReport:
        """
        Retourne un rapport JSON par entité avec :
        - empirical_te: float     # templateabilité observée
        - empirical_he: float     # homogénéité observée
        - empirical_r: float      # risque contextuel observé
        - n_unique_patterns: int
        - annotation_yield: float
        - recommended_method: str  # décision bottom-up REST
        """
```

---

### `ESMO2025/REST_interface/rest_decision_bridge.py` (À créer — composant clé)

**Rôle** : Composant de validation croisée entre l'approche top-down (métriques calculées → arbre) et l'approche bottom-up (annotations pilotes → REST). **Ce module est le cœur de la validation méthodologique de DuraXELL.**

```python
class RESTDecisionBridge:
    """
    Pont de validation croisée bidirectionnelle.
    
    Approche top-down (DuraXELL/ESMO2025) :
        Corpus → E_*.py → métriques → arbre → décision
    
    Approche bottom-up (REST/Bazin) :
        Annotation pilote → RESTEvaluator → décision empirique
    
    Ce composant compare les décisions des deux approches :
    - Si concordance > 80% : validation mutuelle → les métriques sont fiables
    - Si divergence : identifier les entités problématiques → recalibrer les seuils
    
    Sortie : convergence_tree_vs_rest.json
    """

    def compare(
        self,
        tree_decisions: dict[str, str],
        rest_decisions: dict[str, str]
    ) -> ConvergenceReport:
        """
        Retourne :
        - concordance_rate: float
        - concordant_entities: list[str]
        - divergent_entities: list[dict]  # {entity, tree_decision, rest_decision, delta_metrics}
        - recalibration_suggestions: list[dict]
        """

    def suggest_recalibration(
        self,
        divergent_cases: list[dict]
    ) -> dict[str, float]:
        """
        Pour les cas divergents, suggère des ajustements de seuils
        dans decision_config.json.
        """
```

---

### `ESMO2025/REST_interface/convergence_analyzer.py` (À créer)

**Rôle** : Analyse fine des divergences et génère des visualisations de convergence.

```python
def analyze_convergence(bridge_report: ConvergenceReport) -> None:
    """
    1. Scatter plot : décision REST (axe X) vs décision arbre (axe Y) par entité
    2. Heatmap de concordance par (entité × méthode)
    3. Identification des clusters : entités systématiquement divergentes
    4. Recommandations de recalibration avec intervalles de confiance
    
    Sauvegarde : Results/REST_results/convergence_tree_vs_rest.json
                 Results/figures/rest_convergence_plot.png
    """
```

---

### `NER/src/5evaluate_ner.py` (À créer)

**Rôle** : Évaluation complète et fine du pipeline NER par entité, en complément de `sweep_results.csv`.

```python
def evaluate_ner_complete(
    predictions_brat_dir: str,
    gold_standard_dir: str,
    entity_types: list[str]
) -> pd.DataFrame:
    """
    Calcule pour chaque entité :
    - Précision, Rappel, F1 (strict et partiel)
    - Matrice de confusion inter-entités (confusions Estrogen_receptor / Progesterone_receptor ?)
    - Analyse des erreurs : faux positifs typiques, faux négatifs typiques
    
    Compare avec les décisions de l'arbre :
    - Les entités assignées à "NER Transformer" ont-elles les F1 les plus élevés avec Transformer ?
    - Validation empirique de la cohérence arbre → performance
    """
```

---

### `NER/src/ner_cascade_connector.py` (À créer)

**Rôle** : Adaptateur entre le pipeline NER existant et `cascade_orchestrator.py`.

```python
class NERCascadeConnector:
    """
    Adaptateur permettant à CascadeOrchestrator d'utiliser
    les modèles NER entraînés (3infer.py).
    
    Encapsule le chargement du modèle, l'inférence,
    et le calcul de confiance basé sur les probabilités softmax.
    """

    def __init__(self, model_path: str, device: str = "cpu"):
        self.model = load_model(model_path)

    def predict(
        self,
        text: str,
        entity_type: str
    ) -> ExtractionResult:
        """
        Appelle 3infer.py sur le texte et retourne un ExtractionResult
        avec confidence = max(softmax_probabilities).
        """
```

---

### `Rules/src/Breast/rules_cascade_connector.py` (À créer)

**Rôle** : Adaptateur entre les règles regex existantes et `cascade_orchestrator.py`.

```python
class RulesCascadeConnector:
    """
    Adaptateur permettant à CascadeOrchestrator d'utiliser
    le moteur de règles (biomarker_brat_annotator.py).
    
    Convertit les résultats de l'annotateur BRAT en ExtractionResult
    avec un score de confiance basé sur la précision historique de la règle.
    """

    def predict(
        self,
        text: str,
        entity_type: str
    ) -> ExtractionResult:
        """
        Applique les règles regex correspondant à entity_type.
        confidence = précision_estimée_de_la_règle (issue de Rules/evaluator)
        """
```

---

### `reports/DuraXELL_Pipeline.ipynb` (À créer — évolution de commandes.ipynb)

**Structure du notebook** :

```
Section 0 : Introduction et contexte DuraXELL
Section 1 : Configuration et installation
  1.1 : Dépendances
  1.2 : Chargement des données (BRAT → Python)
  1.3 : Statistiques descriptives du corpus
  1.4 : Visualisation de la distribution des entités

Section 2 : Calcul des métriques ESMO2025
  2.1 : Templateabilité (Te) — appel E_templeability.py
  2.2 : Homogénéité (He) — appel E_homogeneity.py
  2.3 : Risque Contextuel (R) — appel E_risk_context.py
  2.4 : Fréquence (Freq) — appel E_frequency.py
  2.5 : Rendement d'annotation (Yield) — appel E_annotation_yield.py
  2.6 : Heatmap des 5 métriques × 7 entités

Section 3 : Arbre de décision
  3.1 : Exécution E_creation_arbre_decision.py
  3.2 : Visualisation de l'arbre
  3.3 : Tableau des recommandations
  3.4 : Analyse de sensibilité des seuils

Section 4 : Validation REST
  4.1 : Exécution de l'annotation pilote (REST)
  4.2 : Rapport d'évaluation REST par entité
  4.3 : Concordance REST ↔ Arbre

Section 5 : Cascade et résultats
  5.1 : Exécution de la cascade sur le corpus de validation
  5.2 : Performance (F1 par entité)
  5.3 : Énergie (kWh par méthode)
  5.4 : Explicabilité
  5.5 : Score Composite Trilemme
  5.6 : Front de Pareto

Section 6 : Extension cancer du poumon
  6.1 : Métriques Te/He/R/Freq pour EGFR, ALK, ROS1, KRAS, PD-L1
  6.2 : Arbre de décision — cancer du poumon
  6.3 : Comparaison sein vs poumon

Section 7 : Conclusions et perspectives
  7.1 : Vérification de l'hypothèse "80% par méthodes légères"
  7.2 : Comparaison avec baseline tout-transformer
  7.3 : Roadmap AP-HP et conférence Frugalité
```

---

# PARTIE II — PLANNING JOURNALIER HEURE PAR HEURE

## Règles d'hygiène de vie (invariantes)

| Règle | Détail |
|-------|--------|
| **Lever** | 7h00 (constante, y compris weekends de travail) |
| **Marche matinale** | 30–45 min, avant ou après petit-déjeuner léger — obligatoire |
| **Blocs de travail profond** | 90 min MAX, suivis de 15 min de pause active |
| **Marche midi** | 30–60 min avec le déjeuner |
| **Marche vespérale** | 30–60 min — décompression |
| **Écrans coupés** | 21h30 — sans exception |
| **Coucher** | 22h00–22h30 |
| **Hydratation** | 2L/jour minimum |
| **Caféine** | Interdite après 14h00 |
| **Nutrition** | Petit-déjeuner : protéines + glucides complexes. Déjeuner : complet. Dîner : léger. |

---

## PHASE 0 — Pré-lancement (Lundi 23 février — veille de démarrage)

**Objectif** : préparer l'environnement mental et technique avant de commencer.

| Heure | Activité | Détail |
|-------|----------|--------|
| 7:00–7:30 | Réveil + routine matinale | Hydratation, 5 min de respiration intentionnelle |
| 7:30–8:15 | **Marche matinale** | 45 min, rythme libre, pas de téléphone |
| 8:15–8:30 | Petit-déjeuner | |
| **9:00–10:00** | **Lecture de cadrage** | Relire `ARCHITECTURE_RECAP.md` (ESMO2025) et le README de REST-interface. Prendre des notes sur papier uniquement |
| **10:00–10:30** | **Setup mental** | Sur papier : lister les 5 choses les plus importantes à faire ces 2 semaines, dans l'ordre de valeur scientifique |
| 10:30–12:00 | Activité libre | |
| 12:00–13:00 | Déjeuner + marche | |
| **13:00–14:00** | **Vérification technique** | S'assurer d'avoir accès à GitHub (push/pull), Python ≥ 3.10, GPU/CPU disponible, eco2ai installé |
| 14:00–22:00 | Repos + détente | Coucher 22h00 — le lendemain est chargé |

---

## SEMAINE 1 — FONDATIONS ET MÉTRIQUES

---

### Mardi 24 février — AUDIT COMPLET ET SETUP

**Objectif** : état des lieux exhaustif du code ESMO2025, clone de REST-interface, environnement reproductible.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:15 | Réveil + hydratation | 500 ml d'eau |
| 7:15–8:00 | **Marche matinale** | 45 min, rythme soutenu, 4 000 pas |
| 8:00–8:20 | Petit-déjeuner | Œufs + flocons d'avoine + fruit |
| **8:20–9:50** | **BLOC 1 — Audit ESMO2025 : Métriques** | |
| | | • Ouvrir le dépôt ESMO2025 dans VSCode avec la vue "Explorer" ouverte |
| | | • Lire intégralement `ARCHITECTURE_RECAP.md` : noter les fichiers existants et leurs rôles |
| | | • Exécuter `E_templeability.py` seul : noter les arguments, la sortie, les fichiers produits |
| | | • Exécuter `E_homogeneity.py` : noter le format de sortie `.csv` |
| | | • Exécuter `E_risk_context.py` : noter `risk_context_full.json` |
| | | • Exécuter `E_frequency.py` : noter la distribution obtenue |
| | | • Pour chaque script : noter dans `AUDIT_24FEV.md` → `{script: entrées, sorties, bugs, qualité}` |
| 9:50–10:05 | Pause | Debout, étirements rachis, eau |
| **10:05–11:35** | **BLOC 2 — Audit ESMO2025 : Pipeline NER** | |
| | | • Ouvrir `NER/src/` et lire chaque script dans l'ordre (1 → 4) |
| | | • Pour `1convert_brat_to_conll.py` : vérifier le format de sortie CoNLL, compter les entités |
| | | • Pour `2sweep_ner.py` : identifier les modèles testés (PubMedBERT ? CancerBERT ? CamemBERT-bio ?) |
| | | • Ouvrir `sweep_results.csv` : quel modèle obtient le meilleur F1 ? Sur quelles entités ? |
| | | • Pour `3infer.py` : identifier comment charger le meilleur modèle |
| | | • Pour `4predict_to_brat.py` : vérifier la conversion en format BRAT |
| | | • Compter les fichiers dans `NER/data/Breast/` : combien de documents annotés ? |
| | | • Documenter dans `AUDIT_24FEV.md` → section "Pipeline NER" |
| 11:35–11:50 | Pause | |
| **11:50–12:30** | **BLOC 3 — Audit ESMO2025 : Arbre de décision** | |
| | | • Lire intégralement `E_creation_arbre_decision.py` (344 lignes) |
| | | • Identifier la fonction `decide_method(entity)` et tracer son flow sur papier |
| | | • Lire `output_decision.txt` : vérifier les 7 recommandations (Estrogen_receptor → ML CRF, etc.) |
| | | • Identifier les seuils actuels dans `THRESHOLDS` |
| | | • Vérifier si Yield est présent : si non → noter comme manquant |
| | | • Documenter dans `AUDIT_24FEV.md` → section "Arbre de décision" |
| **12:30–13:30** | **Déjeuner + marche** | 30 min de marche digestive après le repas |
| **13:30–14:30** | **BLOC 4 — Clone et audit REST-interface** | |
| | | • `git clone https://github.com/longeacc/REST-interface.git` |
| | | • Lire le README et identifier : quel problème résout ce projet ? Quelle est son architecture ? |
| | | • Identifier les points de contact avec ESMO2025 : |
| | |   — Quels formats de données utilise REST ? BRAT ? JSON ? CSV ? |
| | |   — Comment REST décide-t-il Rules vs ML ? Quels critères ? |
| | |   — Quels scripts sont réutilisables tels quels vs à adapter ? |
| | | • Mapper la "boucle 3 phases REST" sur l'arbre DuraXELL (voir `rest_decision_bridge.py` spec) |
| | | • Documenter dans `AUDIT_24FEV.md` → section "REST-interface" |
| 14:30–14:45 | Pause | |
| **14:45–16:15** | **BLOC 5 — Setup environnement reproductible** | |
| | | • `python -m venv .venv_duraxell && source .venv_duraxell/bin/activate` |
| | | • Installer : `pip install eco2ai pandas numpy matplotlib seaborn scikit-learn` |
| | | • Installer : `pip install transformers datasets seqeval tokenizers accelerate` |
| | | • Installer : `pip install networkx graphviz pytest black isort` |
| | | • Vérifier que tous les scripts `E_*.py` s'exécutent sans erreur |
| | | • Vérifier eco2ai : `import eco2ai; eco2ai.Tracker(project_name="duraxell_test").start()` |
| | | • Créer `requirements.txt` avec `pip freeze > requirements.txt` |
| | | • Tester la reproductibilité : nouveau dossier vide → install → exécution |
| 16:15–16:30 | Pause | |
| **16:30–17:30** | **BLOC 6 — Exécution arbre de décision + synthèse audit** | |
| | | • Exécuter `E_creation_arbre_decision.py` |
| | | • Comparer les résultats avec `output_decision.txt` existant |
| | | • Documenter les divergences éventuelles |
| | | • Finaliser `AUDIT_24FEV.md` : état des lieux complet, liste des bugs, liste des améliorations priorisées |
| | | • Commit : `git add . && git commit -m "feat: audit initial DuraXELL + setup env reproductible"` |
| **17:30–18:30** | **Marche vespérale** | 1h, rythme modéré. Pas de podcast, pas de musique. Réflexion libre sur l'audit |
| 18:30–19:30 | Dîner | Repas complet, léger |
| 19:30–21:00 | Lecture | Relire l'article Redjdal et al. (2024) — sections Méthodes et Résultats. Annoter les points à reproduire dans la cascade |
| 21:30 | Écrans coupés | |
| 22:00 | Coucher | |

---

### Mercredi 25 février — RAFFINEMENT DES MÉTRIQUES (Te, He, R, Freq)

**Objectif** : auditer et améliorer chaque script `E_*.py` existant. Robustesse, tests unitaires, cohérence inter-métriques.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:45 | Réveil + marche | 45 min, 4 000 pas |
| 7:45–8:00 | Petit-déjeuner | |
| **8:00–9:30** | **BLOC 1 — Raffinement E_templeability.py** | |
| | | • Ouvrir le script et identifier `analyze_pattern_complexity()` |
| | | • Tester la normalisation regex : "HER2 3+" → "XXX D+" — est-ce exhaustif ? |
| | | • Cas à tester manuellement : "ER ≥ 80%", "Ki67 entre 15 et 20%", "T2N1M0", "mutation G719X" |
| | | • Si la normalisation manque des patterns → l'améliorer (ajouter des règles de substitution) |
| | | • Créer `tests/test_templeability.py` avec au moins 5 cas :  |
| | |   — `assert scorer.compute("Genetic_mutation") > 0.8`  (Te doit être élevé → Règles) |
| | |   — `assert scorer.compute("HER2_FISH") < 0.3`  (Te doit être faible → LLM) |
| | |   — `assert scorer.compute("Estrogen_receptor") > 0.6` |
| | | • `pytest tests/test_templeability.py` → tous verts |
| | | • Recalculer Te pour toutes les entités après raffinement → noter les changements |
| 9:30–9:45 | Pause | |
| **9:45–11:15** | **BLOC 2 — Raffinement E_homogeneity.py** | |
| | | • Auditer la formule : `He = (Te_words - Ue_words) / Te_words` |
| | | • Vérifier la fonction sigmoïde de normalisation (paramètres k et x₀) |
| | | • Cas limite 1 : entité avec 1 seule mention → He = 1.0 par convention |
| | | • Cas limite 2 : entité avec 1000 mentions toutes identiques → He ≈ 1.0 |
| | | • Cas limite 3 : entité avec 1000 mentions toutes différentes → He ≈ 0.0 |
| | | • Créer `tests/test_homogeneity.py` |
| | | • Vérifier la cohérence croisée : si Te(e) élevé ET He(e) élevé → faisabilité Règles optimale |
| | | • Recalculer He pour toutes les entités |
| 11:15–11:30 | Pause | |
| **11:30–12:15** | **BLOC 3 — Raffinement E_risk_context.py** | |
| | | • Auditer la classification Haut/Faible risque contextuel |
| | | • Ajouter la détection de **négation** : patterns dans une fenêtre ±3 tokens |
| | |   → `["non", "ne pas", "absent", "négatif", "sans", "ni"]` |
| | | • Ajouter la détection d'**incertitude** : `["probable", "possible", "suspecté", "à confirmer"]` |
| | | • Ajouter la détection de **contradiction** : même entité positive ET négative dans le document |
| | | • Créer `tests/test_risk_context.py` avec 10 cas annotés manuellement |
| | |   — "HER2 non surexprimé" → R moyen (négation simple bien définie) |
| | |   — "statut HER2 discordant entre biopsie et pièce" → R élevé |
| | |   — "TNM T2N1M0" → R faible |
| **12:15–13:15** | **Déjeuner + marche** | 45 min de marche — pas de téléphone |
| **13:15–14:45** | **BLOC 4 — Raffinement E_frequency.py** | |
| | | • Vérifier la formule : Freq relative ou absolue ? (à clarifier dans la docstring) |
| | | • Recommandation : `Freq = nb_occurrences_entité / nb_total_documents` (plus interprétable) |
| | | • Calibrer `FREQ_SUFFICIENT=0.001` : analyser la distribution pour ajuster |
| | | • Produire l'histogramme de distribution en échelle log (matplotlib) |
| | | • Identifier les entités rares (< 10 occurrences) → décision automatique : LLM ou Règles |
| | | • Créer `tests/test_frequency.py` |
| 14:45–15:00 | Pause | |
| **15:00–16:30** | **BLOC 5 — Raffinement E_fesability_NER.py + création E_annotation_yield.py** | |
| | | • Auditer `E_fesability_NER.py` : comment est calculé le score de faisabilité ? |
| | | • Vérifier la cohérence avec `sweep_results.csv` : les entités "faisables" ont-elles les meilleurs F1 ? |
| | | • Créer `E_annotation_yield.py` selon la spec décrite dans la Partie I |
| | | • Formule principale : `Yield = F1(règles_sur_corpus_annoté, gold_standard)` |
| | | • Tester sur les 7 entités sein |
| | | • Créer `tests/test_annotation_yield.py` |
| 16:30–16:45 | Pause | |
| **16:45–17:45** | **BLOC 6 — Génération des rapports mis à jour** | |
| | | • Exécuter tous les scripts `E_*.py` et vérifier la cohérence des sorties mises à jour |
| | | • Vérifier les rapports HTML générés (si existants) |
| | | • Comparer les nouvelles valeurs de métriques avec les valeurs pré-raffinement : |
| | |   — Documenter les changements dans `AUDIT_24FEV.md` → section "Métriques v2" |
| | | • Commit : `git commit -m "refactor: raffinement métriques Te/He/R/Freq + Yield + tests unitaires"` |
| **17:45–18:45** | **Marche rapide** | 1h — parcours différent du matin. Objectif : 12 000 pas cumulés |
| 18:45–19:45 | Dîner | |
| 19:45–21:00 | Lecture | Approfondir la partie REST-interface : comprendre la boucle 3 phases pour préparer J4 |
| 21:30 | Écrans coupés | |
| 22:00 | Coucher | |

---

### Jeudi 26 février — ARBRE DE DÉCISION : RAFFINEMENT, CALIBRATION, VISUALISATION

**Objectif** : transformer `E_creation_arbre_decision.py` en un système robuste avec Yield intégré, seuils calibrés, et visualisation de publication.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:45 | Réveil + marche | |
| 7:45–8:00 | Petit-déjeuner | |
| **8:00–9:30** | **BLOC 1 — Analyse critique de l'arbre existant** | |
| | | • Lire les 344 lignes de `E_creation_arbre_decision.py` ligne par ligne |
| | | • Tracer l'arbre sur papier : chaque nœud de décision, chaque feuille |
| | | • Vérifier que les 6 feuilles sont toutes atteignables (chercher les branches mortes) |
| | | • Mapper chaque branche du code à la spec théorique : |
| | |   — Feuille 1 : RÈGLES PAR DÉFAUT (Te élevé + He élevé + Yield élevé) |
| | |   — Feuille 2 : NER RÈGLES (Te élevé + He élevé + Yield faible) |
| | |   — Feuille 3 : ML LÉGER DÉFAUT (Te élevé + He faible) |
| | |   — Feuille 4 : ML LÉGER NER (Te moyen + R faible + Freq élevée) |
| | |   — Feuille 5 : NER TRANSFORMER (Te moyen + R élevé) |
| | |   — Feuille 6 : NER LLM (Te faible) |
| | | • Identifier où insérer le critère Yield (nœud 3 dans la spec) |
| 9:30–9:45 | Pause | |
| **9:45–11:15** | **BLOC 2 — Calibration des seuils par analyse de distribution** | |
| | | • Pour chaque seuil à calibrer, tracer la distribution empirique sur les entités connues : |
| | | • `TE_HIGH` : distribution Te de {Genetic_mutation=0.91, HER2_IHC=0.65, Ki67=0.42, HER2_FISH=0.18} |
| | |   → Identifier la coupure naturelle entre "élevé" et "moyen" |
| | | • `TE_LOW` : identifier la coupure entre "moyen" et "faible" |
| | | • `HE_HIGH`, `RISK_LOW`, `FREQ_SUFFICIENT` : même méthode |
| | | • Utiliser matplotlib pour tracer les histogrammes et identifier les seuils |
| | | • Créer `THRESHOLDS_JUSTIFICATION.md` : pour chaque seuil, sa valeur et sa justification statistique |
| | | • Si la distribution est trop resserrée → explorer des transformations (log, sigmoïde) |
| 11:15–11:30 | Pause | |
| **11:30–12:15** | **BLOC 3 — Intégration du critère Yield dans l'arbre** | |
| | | • Modifier `E_creation_arbre_decision.py` pour intégrer le critère Yield |
| | | • Le nœud Yield intervient APRÈS Te élevé + He élevé : |
| | |   → Yield > YIELD_MIN (0.7 par défaut) → RÈGLES PAR DÉFAUT |
| | |   → Yield ≤ YIELD_MIN → NER RÈGLES |
| | | • Cette distinction est cruciale : elle différencie le cas où les règles fonctionnent bien (Yield élevé) du cas où elles fonctionnent mal (Yield faible) malgré des patterns réguliers |
| | | • Recalculer les recommandations pour les 7 entités sein → vérifier que les résultats sont cohérents avec `output_decision.txt` |
| **12:15–13:15** | **Déjeuner + marche** | |
| **13:15–14:45** | **BLOC 4 — Génération de decision_config.json** | |
| | | • Modifier `E_creation_arbre_decision.py` pour exporter `decision_config.json` |
| | | • Implémenter la structure JSON décrite dans la Partie I |
| | | • Tester sur les 7 entités sein |
| | | • Tester sur 5 entités poumon (valeurs théoriques si pas de données) : EGFR, ALK, ROS1, KRAS, PD-L1 |
| | | • Vérifier que le JSON est valide : `python -c "import json; json.load(open('decision_config.json'))"` |
| 14:45–15:00 | Pause | |
| **15:00–16:30** | **BLOC 5 — Visualisation de l'arbre (visualize_decision_tree.py)** | |
| | | • Créer `visualize_decision_tree.py` selon la spec de la Partie I |
| | | • Utiliser `matplotlib.patches` et `matplotlib.lines` pour dessiner l'arbre manuellement (plus de contrôle que graphviz) |
| | | • OU utiliser `graphviz.Digraph` si préféré (bibliothèque `graphviz`) |
| | | • Code couleur : nœuds de décision en bleu (#2196F3), feuilles colorées par méthode |
| | | • Afficher dans chaque feuille : la méthode + les entités assignées + leur score composite |
| | | • Exporter en PNG (300 dpi) et SVG |
| | | • Sauvegarder dans `Results/figures/decision_tree_visualization.png` |
| 16:30–16:45 | Pause | |
| **16:45–17:45** | **BLOC 6 — Tests exhaustifs de l'arbre + commit** | |
| | | • Créer `tests/test_decision_tree.py` avec les 7 entités sein :  |
| | |   — `assert tree.decide("Estrogen_receptor") == "ML_LEGER_NER"` |
| | |   — `assert tree.decide("Genetic_mutation") == "REGLES_PAR_DEFAUT"` |
| | |   — `assert tree.decide("HER2_FISH") == "NER_LLM"` |
| | |   — `assert tree.decide("Ki67") == "NER_TRANSFORMER"` |
| | | • `pytest tests/test_decision_tree.py` → tous verts |
| | | • Commit : `git commit -m "feat: arbre de décision calibré + Yield + decision_config.json + visualisation"` |
| **17:45–18:45** | **Marche** | 1h |
| 18:45–21:30 | Dîner + détente | |
| 22:00 | Coucher | |

---

### Vendredi 27 février — INTÉGRATION REST-INTERFACE (Parties 1 et 2)

**Objectif** : créer le module `REST_interface/` complet — outil d'annotation, évaluateur, pont de décision, analyse de convergence.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:45 | Réveil + marche | |
| 7:45–8:00 | Petit-déjeuner | |
| **8:00–9:30** | **BLOC 1 — Analyse profonde de REST-interface + plan d'intégration** | |
| | | • Relire le dépôt cloné de Guillaume Bazin avec le prisme de l'intégration |
| | | • Sur papier, mapper la "boucle 3 phases REST" sur ESMO2025 : |
| | |   — Phase 1 REST (annotation pilote) ↔ données d'entrée pour E_templeability + E_homogeneity |
| | |   — Phase 2 REST (évaluation quantitative) ↔ calcul des 5 métriques ESMO2025 |
| | |   — Phase 3 REST (décision Rules/ML) ↔ feuilles de l'arbre de décision |
| | | • Identifier précisément ce que REST fait que l'arbre ne fait pas (empirisme bottom-up) |
| | | • Identifier ce que l'arbre fait que REST ne fait pas (formalisation des seuils, Yield, énergie) |
| | | • Ces deux lacunes mutuelles justifient leur complémentarité |
| | | • Créer le répertoire `ESMO2025/REST_interface/` |
| 9:30–9:45 | Pause | |
| **9:45–11:15** | **BLOC 2 — Création rest_annotator.py** | |
| | | • Implémenter `RESTAnnotator` selon la spec de la Partie I |
| | | • Fonctionnalité minimale viable : charger N dossiers → retourner des annotations format BRAT |
| | | • Paradigme "highlighting" : simuler le regard expert (fenêtre glissante sur le document, annotation des spans identifiés) |
| | | • Mesure du temps : `import time; start = time.perf_counter()` avant/après chaque document |
| | | • Sortie `.ann` : format BRAT strict `T1\tEntity_type start end\tspantext` |
| | | • Test : annoter 3 documents du corpus existant → vérifier le format de sortie |
| 11:15–11:30 | Pause | |
| **11:30–12:15** | **BLOC 3 — Création rest_evaluator.py** | |
| | | • Implémenter `RESTEvaluator` selon la spec de la Partie I |
| | | • Calcul du TTR (Token-Type Ratio) pour l'homogénéité empirique |
| | | • Détection de patterns uniques (via normalisation de E_templeability) → proxy Te empirique |
| | | • Calcul du contexte : même logique que E_risk_context mais sur annotations pilotes |
| | | • Sortie JSON : `{entity_type: {empirical_te, empirical_he, empirical_r, n_unique, annotation_yield, recommended_method}}` |
| **12:15–13:30** | **Déjeuner + marche longue** | 1h de marche — explorer un nouveau parcours |
| **13:30–15:00** | **BLOC 4 — Création rest_decision_bridge.py** | |
| | | • **Composant central de la validation DuraXELL** |
| | | • Charger `decision_config.json` → décisions de l'arbre (top-down) |
| | | • Charger `REST_results/annotation_yield_by_entity.json` → décisions REST (bottom-up) |
| | | • Calculer le taux de concordance : `concordance = len(concordant) / len(total_entities)` |
| | | • Pour les cas divergents : calculer la différence de métriques entre les deux approches |
| | | • Seuil de validation : concordance ≥ 0.80 → les métriques sont validées empiriquement |
| | | • Si concordance < 0.80 → logger les entités problématiques et suggérer des recalibrages |
| | | • Sauvegarder : `Results/REST_results/convergence_tree_vs_rest.json` |
| 15:00–15:15 | Pause | |
| **15:15–16:45** | **BLOC 5 — Création convergence_analyzer.py + demo_rest.py** | |
| | | • `convergence_analyzer.py` : visualisation de la concordance (scatter plot + heatmap) |
| | | • `demo_rest.py` : script driver qui enchaîne les 3 modules :  |
| | |   1. Charger 5 documents du corpus existant |
| | |   2. Annoter avec `RESTAnnotator` |
| | |   3. Évaluer avec `RESTEvaluator` |
| | |   4. Comparer avec l'arbre via `RESTDecisionBridge` |
| | |   5. Afficher le rapport de concordance |
| | | • Créer `REST_interface/__init__.py` avec les exports |
| | | • Tests : `tests/test_rest_bridge.py` |
| 16:45–17:00 | Pause | |
| **17:00–17:45** | **BLOC 6 — Tests, documentation, commit** | |
| | | • `python REST_interface/demo_rest.py` → vérifier les résultats |
| | | • Mettre à jour `ARCHITECTURE_RECAP.md` : ajouter la section REST_interface |
| | | • Mettre à jour `requirements.txt` si nouvelles dépendances |
| | | • Commit : `git commit -m "feat: intégration module REST-interface — annotateur + évaluateur + pont décision"` |
| **17:45–18:45** | **Marche** | 1h — objectif : 13 000 pas cumulés |
| 18:45–21:30 | Dîner + détente | |
| 22:00 | Coucher | |

---

### Samedi 28 février — CASCADE ORCHESTRATOR + ENERGY TRACKER

**Objectif** : créer la pièce maîtresse de l'architecture — l'orchestrateur cascade piloté par `decision_config.json` — et le système de tracking énergétique.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:45 | Réveil + marche | |
| 7:45–8:00 | Petit-déjeuner | |
| **8:00–9:30** | **BLOC 1 — Conception et architecture cascade_orchestrator.py** | |
| | | • Sur papier : dessiner l'architecture de classe `CascadeOrchestrator` |
| | | • Flow de `extract(document, entity_type)` : |
| | |   1. Lire `decision_config[entity_type].primary_method` |
| | |   2. Appeler `_try_{method}(text, entity_type)` |
| | |   3. Si `result.confidence < config[entity_type].confidence_threshold` → essayer le fallback |
| | |   4. Si fallback échoue aussi → escalader vers LLM (si configuré) |
| | |   5. Retourner `ExtractionResult` |
| | | • Définir la `dataclass ExtractionResult` : entity_type, value, span, method_used, confidence, energy_kwh, cascade_level, execution_time_ms |
| | | • Logique de confiance par méthode : |
| | |   — Rules : confiance = précision estimée de la règle (depuis `rules_evaluator`) |
| | |   — ML-CRF : confiance = score de la classe prédite par le CRF |
| | |   — Transformer : confiance = max(softmax) sur la séquence |
| | |   — LLM : confiance = score d'auto-évaluation du LLM (ou 0.8 par défaut) |
| 9:30–9:45 | Pause | |
| **9:45–11:15** | **BLOC 2 — Implémentation de cascade_orchestrator.py** | |
| | | • Implémenter la classe `CascadeOrchestrator` selon la spec de la Partie I |
| | | • `_try_rules()` : appelle `RulesCascadeConnector.predict()` (stub si le connecteur n'est pas encore créé) |
| | | • `_try_ml()` : appelle `NERCascadeConnector.predict()` (stub) |
| | | • `_try_llm()` : appelle un client LLM simple (requête HTTP Mistral API ou stub local) |
| | | • `extract_batch()` : boucle sur `extract()` avec un tqdm pour le suivi de progression |
| | | • Intégrer `EnergyTracker` (à créer juste après) : chaque appel est wrappé dans `tracker.measure()` |
| 11:15–11:30 | Pause | |
| **11:30–12:15** | **BLOC 3 — Création energy_tracker.py** | |
| | | • Implémenter `EnergyTracker` selon la spec de la Partie I |
| | | • `@contextmanager def measure(method, entity_type)` : mesure kWh + CO2e + durée |
| | | • Si eco2ai disponible : utiliser son tracker sous-jacent |
| | | • Sinon : estimations théoriques depuis `REFERENCE_COSTS_KWH` |
| | | • `log()` : append une ligne dans `Consumtion_of_Duraxell.csv` |
| | | • `summary()` : retourne un DataFrame agrégé par méthode (total kWh, moyen, CO2e, durée) |
| **12:15–13:15** | **Déjeuner + marche** | |
| **13:15–14:45** | **BLOC 4 — Connecteurs Rules et NER (vrais connecteurs)** | |
| | | • Créer `Rules/src/Breast/rules_cascade_connector.py` selon la spec |
| | |   → Appelle `biomarker_brat_annotator.py` sur un texte donné pour une entité donnée |
| | |   → Retourne un `ExtractionResult` avec confiance |
| | | • Créer `NER/src/ner_cascade_connector.py` selon la spec |
| | |   → Charge le meilleur modèle depuis `NER/models/best_model/` |
| | |   → Appelle `3infer.py` (ou sa logique) sur le texte |
| | |   → Retourne un `ExtractionResult` avec `confidence = max(softmax)` |
| | | • Remplacer les stubs dans `cascade_orchestrator.py` par les vrais connecteurs |
| 14:45–15:00 | Pause | |
| **15:00–16:30** | **BLOC 5 — Tests intégrés cascade + énergie** | |
| | | • Créer `tests/test_cascade.py` |
| | | • Tester l'extraction de chaque entité sein :  |
| | |   — Estrogen_receptor → doit utiliser ML_CRF en primaire |
| | |   — Genetic_mutation → doit utiliser Rules en primaire |
| | |   — HER2_FISH → doit utiliser LLM (ou son stub) |
| | |   — Ki67 → doit utiliser Transformer |
| | | • Vérifier que l'EnergyTracker enregistre des entrées dans le CSV |
| | | • Produire le premier tableau résumé : entité | méthode_utilisée | F1 | kWh | CO2e |
| | | • Comparer les kWh avec les valeurs théoriques de `REFERENCE_COSTS_KWH` |
| 16:30–16:45 | Pause | |
| **16:45–17:45** | **BLOC 6 — Bilan Semaine 1 + commit final** | |
| | | • Rédiger `BILAN_SEMAINE1.md` : |
| | |   — Ce qui est fait : liste des fichiers créés/modifiés |
| | |   — Ce qui reste : liste priorisée pour S2 |
| | |   — Problèmes non résolus |
| | |   — Décisions techniques prises et justifications |
| | | • Mettre à jour le notebook `commandes.ipynb` avec les nouvelles imports |
| | | • Commit final S1 : `git commit -m "feat: cascade orchestrator + energy tracker + connecteurs + bilan S1"` |
| | | • Push : `git push origin main` |
| **17:45–18:45** | **Marche longue** | 1h — bilan mental de la semaine |
| 18:45–22:00 | Dîner + détente complète | |
| 22:00 | Coucher | |

---

## PAUSE — 1, 2, 3 mars

### Dimanche 1er mars — Repos actif

| Heure | Activité |
|-------|----------|
| 7:30 | Réveil naturel |
| 8:00–9:30 | **Marche longue** (1h30, nature si possible) |
| 9:30–12:00 | Petit-déjeuner tardif + activité libre totale (lecture de plaisir, musique, cuisine, sieste) |
| 12:00–13:00 | Déjeuner |
| 13:00–16:00 | Repos complet, sieste si besoin. **Aucun code, aucune lecture académique.** |
| 16:00–17:00 | **Marche légère** (30 min) |
| 17:00–22:00 | Activité libre |
| 22:00 | Coucher |

### Lundi 2 mars — Repos actif + consolidation mentale

| Heure | Activité |
|-------|----------|
| 7:30 | Réveil |
| 8:00–9:30 | **Marche matinale longue** (1h30 — nouveau parcours) |
| 9:30–11:00 | Lecture légère : 1 ou 2 articles de fond, **sans code**. Objectif : comprendre, pas faire |
| 11:00–12:00 | Notes libres sur papier : idées qui émergent, connections non vues en semaine 1 |
| 12:00–13:00 | Déjeuner |
| 13:00–15:00 | Repos complet |
| 15:00–16:00 | Relire `BILAN_SEMAINE1.md` — seule lecture autorisée — et noter mentalement les priorités S2 |
| 16:00–17:00 | **Marche** |
| 17:00–22:00 | Détente |
| 22:00 | Coucher |

### Mardi 3 mars — Repos actif + préparation S2

| Heure | Activité |
|-------|----------|
| 7:00 | Réveil (retour au rythme) |
| 7:30–8:30 | **Marche matinale** |
| 8:30–9:30 | Relecture du code produit en S1 (lecture seule, annotations mentales) |
| 9:30–10:30 | Planification fine des journées 4 → fin des vacances : vérifier que l'ordre des tâches est optimal |
| 10:30–12:00 | Lecture ciblée : documentation HuggingFace Trainer + seqeval pour évaluation NER |
| 12:00–13:00 | Déjeuner |
| 13:00–14:00 | **Marche** |
| 14:00–16:00 | Créer les squelettes (fichiers vides avec docstrings) des scripts à créer en S2 |
| 16:00–22:00 | Détente |
| 22:00 | Coucher |

---

## SEMAINE 2 — PIPELINE NER, ÉVALUATION MULTI-CRITÈRES, DOCUMENTATION

---

### Mercredi 4 mars — PIPELINE NER COMPLET ET CONNECTÉ À LA CASCADE

**Objectif** : s'assurer que le pipeline NER fonctionne de bout en bout et est piloté par `decision_config.json`.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:45 | Réveil + marche | |
| 7:45–8:00 | Petit-déjeuner | |
| **8:00–9:30** | **BLOC 1 — Pipeline NER : données et conversion BRAT → CoNLL** | |
| | | • Exécuter `1convert_brat_to_conll.py` |
| | | • Vérifier les statistiques de conversion : |
| | |   — Nombre de documents train / val / test |
| | |   — Nombre d'annotations par entité dans le split train |
| | |   — Vérifier la stratification : proportions similaires train/val/test par entité |
| | | • Identifier les entités sous-représentées (< 30 occurrences en train) |
| | | • Croiser avec `decision_config.json` : les entités "ML Léger NER" ou "NER Transformer" ont-elles ≥ 50 exemples en train ? |
| | | • Si non → documenter le problème de données insuffisantes |
| 9:30–9:45 | Pause | |
| **9:45–11:15** | **BLOC 2 — Pipeline NER : entraînement et analyse du sweep** | |
| | | • Ouvrir `sweep_results.csv` et analyser finement : |
| | |   — Quel modèle (PubMedBERT, CancerBERT, etc.) a le meilleur F1 global ? |
| | |   — Quel modèle a le meilleur F1 par entité ? (le meilleur global n'est pas forcément le meilleur par entité) |
| | |   — Quel learning rate et batch size sont optimaux ? |
| | | • Produire un tableau : entité × modèle → F1 |
| | | • Vérifier la cohérence avec l'arbre : les entités "NER Transformer" ont-elles le meilleur gain avec les transformers vs règles ? |
| | | • Si un sweep rapide est nécessaire (nouveaux modèles) : lancer `2sweep_ner.py` avec 3 epochs |
| 11:15–11:30 | Pause | |
| **11:30–12:15** | **BLOC 3 — Pipeline NER : inférence et conversion BRAT** | |
| | | • Charger le meilleur modèle avec `3infer.py` sur les données de validation |
| | | • Exécuter `4predict_to_brat.py` : convertir les prédictions en format BRAT |
| | | • Comparer visuellement prédictions vs Gold Standard pour 3 documents |
| | | • Créer `5evaluate_ner.py` avec calcul de F1 strict par entité + analyse des erreurs |
| **12:15–13:15** | **Déjeuner + marche** | |
| **13:15–14:45** | **BLOC 4 — Connexion NER → Cascade (remplacement du stub)** | |
| | | • Finaliser `NER/src/ner_cascade_connector.py` |
| | | • Remplacer le stub dans `cascade_orchestrator.py._try_transformer()` |
| | | • Tester : extraire Ki67 d'un document → le cascade_orchestrator doit charger le bon modèle et retourner un `ExtractionResult` avec confidence basée sur softmax |
| | | • Vérifier le tracking énergie : l'appel au transformer est-il enregistré dans le CSV ? |
| 14:45–15:00 | Pause | |
| **15:00–16:30** | **BLOC 5 — Connexion Rules → Cascade + tests entités sein** | |
| | | • Finaliser `Rules/src/Breast/rules_cascade_connector.py` |
| | | • Remplacer le stub dans `cascade_orchestrator.py._try_rules()` |
| | | • Tester la cascade complète sur les 7 entités sein : |
| | |   — Chaque entité emprunte-t-elle le bon chemin ? |
| | |   — Les résultats sont-ils corrects (comparaison avec Gold Standard) ? |
| | |   — L'énergie est-elle correctement trackée ? |
| | | • Produire le tableau : entité | méthode_utilisée | confiance | F1_approx | kWh |
| 16:30–16:45 | Pause | |
| **16:45–17:45** | **BLOC 6 — Test de bout en bout + commit** | |
| | | • Exécuter la cascade sur 10 documents complets (avec toutes les entités) |
| | | • Logger les résultats dans `Results/benchmark_performance.csv` (première version) |
| | | • Commit : `git commit -m "feat: pipeline NER intégré cascade + connecteurs vrais + premiers benchmarks"` |
| **17:45–18:45** | **Sport** | 1h marche rapide ou footing léger 30 min + étirements |
| 18:45–22:00 | Dîner + détente | |
| 22:00 | Coucher | |

---

### Jeudi 5 mars — ÉVALUATION MULTI-CRITÈRES COMPLÈTE

**Objectif** : évaluer le système sur les 3 axes du trilemme, valider la concordance REST, produire les figures de publication.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:45 | Réveil + marche | |
| 7:45–8:00 | Petit-déjeuner | |
| **8:00–9:30** | **BLOC 1 — Benchmark Performance (F1)** | |
| | | • Exécuter la cascade sur **tout** le corpus de validation |
| | | • Calculer pour chaque entité : Précision, Rappel, F1 (strict et partiel) |
| | | • Produire la matrice de confusion inter-entités |
| | | • Comparer avec : |
| | |   — Baseline "tout-règles" (exécuter uniquement le moteur de règles) |
| | |   — Baseline "tout-transformer" (exécuter uniquement le NER Transformer) |
| | |   — Résultats publiés (Redjdal et al. 2024 : F1=0.90 NER, 0.87 RE) |
| | | • Sauvegarder `Results/benchmark_performance.csv` |
| 9:30–9:45 | Pause | |
| **9:45–11:15** | **BLOC 2 — Benchmark Explicabilité** | |
| | | • Implémenter `E_composite_scorer.py` selon la spec de la Partie I |
| | | • Définir formellement les scores d'explicabilité : Rules=1.0, ML_CRF=0.7, Transformer=0.3, LLM=0.1 |
| | | • Calculer le score d'explicabilité moyen pondéré par la proportion d'usage dans la cascade |
| | | • Ex : si 60% des extractions utilisent Rules, 30% ML_CRF, 10% Transformer : |
| | |   → Expl_cascade = 0.6×1.0 + 0.3×0.7 + 0.1×0.3 = 0.84 |
| | | • Comparer : cascade DuraXELL (0.84) vs tout-transformer (0.3) vs tout-LLM (0.1) |
| | | • Sauvegarder `Results/benchmark_explainability.csv` |
| 11:15–11:30 | Pause | |
| **11:30–12:15** | **BLOC 3 — Benchmark Énergie** | |
| | | • Collecter les données eco2ai de chaque run depuis `Consumtion_of_Duraxell.csv` |
| | | • Calculer le coût total de la cascade pour traiter le corpus de validation |
| | | • Calculer le coût hypothétique en mode "tout-LLM" (même nombre d'extractions, tout via API) |
| | | • Calculer le ratio : économie d'énergie de la cascade vs tout-LLM |
| | | • **Vérifier l'hypothèse centrale** : quel % des extractions est traité par Rules + ML_CRF ? |
| | |   → Hypothèse : ≥ 80%. Si résultat < 80% → identifier pourquoi et ajuster l'arbre |
| | | • Sauvegarder `Results/benchmark_energy.csv` |
| **12:15–13:15** | **Déjeuner + marche** | |
| **13:15–14:45** | **BLOC 4 — Score Composite Trilemme + Front de Pareto** | |
| | | • Exécuter `E_composite_scorer.compute()` pour chaque configuration (méthode × entité) |
| | | • Tester les pondérations : `α=0.4, β=0.3, γ=0.3` (équilibré) ET `α=0.6, β=0.2, γ=0.2` (priorité performance) |
| | | • `E_composite_scorer.pareto_analysis()` : identifier les configurations Pareto-optimales |
| | | • Vérifier que la cascade DuraXELL est sur ou proche du front de Pareto |
| | | • `E_composite_scorer.radar_plot()` : générer le graphique radar |
| 14:45–15:00 | Pause | |
| **15:00–16:30** | **BLOC 5 — Validation REST ↔ Arbre** | |
| | | • Exécuter `REST_interface/demo_rest.py` sur l'ensemble du corpus disponible |
| | | • `rest_decision_bridge.py` : calculer le taux de concordance |
| | | • **Seuil cible** : concordance ≥ 0.80 |
| | | • Si concordance ≥ 0.80 → validation mutuelle réussie → les métriques sont robustes |
| | | • Si concordance < 0.80 → itérer : identifier les entités divergentes → recalibrer les seuils |
| | | • Sauvegarder `Results/REST_results/convergence_tree_vs_rest.json` |
| 16:30–16:45 | Pause | |
| **16:45–17:45** | **BLOC 6 — Génération des 5 figures de publication** | |
| | | • **Fig 1** : Arbre de décision avec résultats par entité (depuis `visualize_decision_tree.py`) |
| | | • **Fig 2** : Heatmap F1 par entité × méthode (benchmarks performance) |
| | | • **Fig 3** : Barplot comparatif énergie — cascade vs tout-transformer vs tout-LLM |
| | | • **Fig 4** : Radar trilemme (Performance / Explicabilité / Énergie) |
| | | • **Fig 5** : Concordance REST ↔ Arbre (scatter plot ou graphe biparti) |
| | | • Sauvegarder toutes les figures dans `Results/figures/` à 300 dpi |
| | | • Commit : `git commit -m "feat: évaluation trilemme complète + 5 figures publication"` |
| **17:45–18:45** | **Marche longue** | 1h — décompression |
| 18:45–22:00 | Dîner + détente | |
| 22:00 | Coucher | |

---

### Vendredi 6 mars — NOTEBOOK MAÎTRE ET REPRODUCTIBILITÉ COMPLÈTE

**Objectif** : créer `DuraXELL_Pipeline.ipynb` — notebook reproductible qui exécute l'intégralité du pipeline de bout en bout.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:45 | Réveil + marche | |
| 7:45–8:00 | Petit-déjeuner | |
| **8:00–9:30** | **BLOC 1 — Notebook S0 et S1 : Setup, données, métriques** | |
| | | • Créer `reports/DuraXELL_Pipeline.ipynb` (ou enrichir `commandes.ipynb`) |
| | | • **Section 0** : Introduction DuraXELL, contexte, objectifs |
| | | • **Section 1** : Installation + chargement des données + statistiques descriptives + visualisation |
| | | • **Section 2.1–2.6** : Appels aux `E_*.py` + heatmap des 5 métriques |
| | | • Chaque cellule : commentaire en Markdown + code + sortie interprétée |
| 9:30–9:45 | Pause | |
| **9:45–11:15** | **BLOC 2 — Notebook S3 et S4 : Arbre de décision** | |
| | | • **Section 3.1** : Exécution de `E_creation_arbre_decision.py` |
| | | • **Section 3.2** : Visualisation de l'arbre (inline dans le notebook) |
| | | • **Section 3.3** : Tableau des recommandations par entité |
| | | • **Section 3.4** : Analyse de sensibilité en temps réel (slider interactif pour les seuils si Jupyter Widgets) |
| | | • **Section 4** : Validation REST (import de `rest_decision_bridge` + affichage concordance) |
| 11:15–11:30 | Pause | |
| **11:30–12:15** | **BLOC 3 — Notebook S5 : Cascade et résultats** | |
| | | • **Section 5.1** : Exécution de `cascade_orchestrator.extract_batch()` sur le corpus |
| | | • **Section 5.2–5.5** : Performance, Énergie, Explicabilité, Score Composite |
| | | • **Section 5.6** : Front de Pareto (figure interactive) |
| | | • **Section 6** : Extension cancer du poumon (métriques + arbre + comparaison) |
| **12:15–13:15** | **Déjeuner + marche** | |
| **13:15–14:45** | **BLOC 4 — README.md complet** | |
| | | • Créer `README.md` à la racine selon la spec de la Partie I |
| | | • Schéma ASCII de l'architecture cascade |
| | | • Tableau des résultats principaux (F1 par entité, coût énergétique, score composite) |
| | | • Instructions d'installation et d'exécution reproductible |
| | | • Référence Redjdal et al. 2024 + informations de citation |
| | | • Mise à jour `requirements.txt` avec versions pinées |
| 14:45–15:00 | Pause | |
| **15:00–16:30** | **BLOC 5 — Tests de reproductibilité totale** | |
| | | • Cloner le dépôt dans un dossier `ESMO2025_test/` |
| | | • `python -m venv .venv_test && pip install -r requirements.txt` |
| | | • Exécuter `DuraXELL_Pipeline.ipynb` de A à Z |
| | | • Vérifier que toutes les cellules passent et que les résultats sont identiques |
| | | • Corriger les chemins relatifs si nécessaire |
| | | • Supprimer `ESMO2025_test/` après vérification |
| 16:30–16:45 | Pause | |
| **16:45–17:45** | **BLOC 6 — Documentation complète + commit** | |
| | | • Vérifier que toutes les fonctions ont des docstrings (outils : `pylint`, `pydocstyle`) |
| | | • Formater le code : `black ESMO2025/ && isort ESMO2025/` |
| | | • Vérifier le `.gitignore` : pas de données patients, pas de modèles lourds, pas de fichiers temporaires |
| | | • Commit : `git commit -m "feat: notebook maître reproductible + README complet + documentation"` |
| | | • Push |
| **17:45–18:45** | **Marche** | 45 min |
| 18:45–22:00 | Dîner + détente | |
| 22:00 | Coucher | |

---

### Samedi 7 mars — EXTENSION POUMON + ANALYSE DE SENSIBILITÉ + PRÉPARATION PUBLICATION

**Objectif** : étendre DuraXELL au cancer du poumon, finaliser l'analyse de sensibilité, rédiger le résumé étendu pour la conférence Frugalité.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:00–7:45 | Réveil + marche | |
| 7:45–8:00 | Petit-déjeuner | |
| **8:00–9:30** | **BLOC 1 — Extension cancer du poumon : métriques** | |
| | | • Définir les entités poumon : EGFR, ALK, ROS1, KRAS, BRAF, PD-L1, TNM_lung |
| | | • Si données disponibles : calculer Te/He/R/Freq/Yield sur les données poumon |
| | | • Si pas de données : définir les valeurs théoriques attendues par extrapolation de la littérature :  |
| | |   — EGFR (mutations ponctuelles) : Te élevé (≈0.85), He moyen (≈0.55), R faible → Règles |
| | |   — PD-L1 (scoring complexe TPS/CPS) : Te faible (≈0.25), R élevé → LLM probable |
| | |   — TNM_lung : Te très élevé (≈0.92), He très élevé (≈0.88) → Règles par défaut |
| | | • Exécuter l'arbre de décision sur les entités poumon |
| | | • Comparer les recommandations sein vs poumon |
| 9:30–9:45 | Pause | |
| **9:45–11:15** | **BLOC 2 — Analyse de sensibilité des seuils** | |
| | | • Créer `sensitivity_analysis.py` selon la spec de la Partie I |
| | | • Faire varier chaque seuil : TE_HIGH, TE_LOW, HE_HIGH, RISK_LOW de ±10%, ±20% |
| | | • Pour chaque variation : recalculer les décisions de l'arbre sur les entités sein + poumon |
| | | • Mesurer : combien d'entités changent de feuille ? Quel impact sur le score composite ? |
| | | • Identifier les seuils les plus **sensibles** vs les plus **robustes** |
| | | • Produire la figure `Results/figures/sensitivity_analysis.png` |
| | | • Sauvegarder `Results/sensitivity_output.csv` |
| 11:15–11:30 | Pause | |
| **11:30–12:15** | **BLOC 3 — Résumé étendu conférence Frugalité (ébauche)** | |
| | | • Créer `reports/conference_frugalite_abstract.md` |
| | | • Titre : *"Cascade intelligente Rules-ML-LLM pour l'extraction de biomarqueurs oncologiques : vers une méthodologie d'évaluation socio-écologiquement consciente"* |
| | | • Section 1 : Problématique (trilemme Performance-Explicabilité-Durabilité) |
| | | • Section 2 : Méthodologie (métriques Te/He/R/Freq/Yield → arbre → cascade → REST) |
| | | • Section 3 : Résultats (F1 par entité, coût énergétique, score composite, concordance REST) |
| | | • Section 4 : Discussion (validation 80% par méthodes légères, front de Pareto) |
| **12:15–13:15** | **Déjeuner + marche** | |
| **13:15–14:45** | **BLOC 4 — Rédaction du résumé étendu (finalisation)** | |
| | | • Rédiger les 2 pages du résumé étendu selon le format de la conférence |
| | | • Intégrer les chiffres clés des benchmarks |
| | | • Intégrer 1 figure (arbre de décision ou radar trilemme) |
| | | • Intégrer 1 tableau (résultats comparatifs cascade vs monolithique) |
| | | • Relecture critique : chaque phrase apporte-t-elle une information ? |
| 14:45–15:00 | Pause | |
| **15:00–16:30** | **BLOC 5 — Mise à jour de la présentation DuraXELL** | |
| | | • Mettre à jour `reports/conference_frugalite_slides.pptx` (ou créer si inexistant) |
| | | • Slide 1 : Titre + institution + cadre |
| | | • Slide 2 : Le trilemme (DuraXELL en 1 graphique) |
| | | • Slide 3 : Les 5 métriques ESMO2025 (Te, He, R, Freq, Yield) |
| | | • Slide 4 : Arbre de décision avec résultats |
| | | • Slide 5 : Intégration REST-interface (concordance bottom-up ↔ top-down) |
| | | • Slide 6 : Cascade + énergie |
| | | • Slide 7 : Score composite + front de Pareto |
| | | • Slide 8 : Extension poumon + perspectives AP-HP |
| 16:30–16:45 | Pause | |
| **16:45–17:45** | **BLOC 6 — Nettoyage final + commit** | |
| | | • Supprimer les fichiers temporaires, prints de debug, fichiers `__pycache__` |
| | | • Vérifier le `.gitignore` (exclusions critiques : données patients, modèles > 100 Mo) |
| | | • `pytest ESMO2025/tests/` → tous les tests passent |
| | | • Commit : `git commit -m "feat: extension poumon + sensibilité + préparation publication Frugalité"` |
| | | • Push |
| **17:45–18:45** | **Marche longue** | 1h — bilan mental |
| 18:45–22:00 | Dîner + repos | |
| 22:00 | Coucher | |

---

### Dimanche 8 mars — CONSOLIDATION, BILAN ET VISION

**Objectif** : journée allégée, consolidation du travail, rédaction du bilan, définition de la roadmap post-vacances.

| Heure | Activité | Détail technique |
|-------|----------|-----------------|
| 7:30–8:30 | Réveil + marche longue | 1h, rythme calme, pas de téléphone |
| 8:30–9:00 | Petit-déjeuner tardif | |
| **9:00–10:30** | **BLOC 1 — Bilan global (BILAN_VACANCES.md)** | |
| | | • Rédiger `reports/BILAN_VACANCES.md` avec : |
| | |   — Liste complète des fichiers créés / modifiés |
| | |   — Résultats quantitatifs obtenus (F1, kWh, concordance REST, % méthodes légères) |
| | |   — Problèmes non résolus et hypothèses à tester |
| | |   — Décisions techniques prises et leurs justifications |
| | | • Mettre à jour le README avec les résultats finals |
| 10:30–10:45 | Pause | |
| **10:45–12:15** | **BLOC 2 — Roadmap post-vacances** | |
| | | • **Court terme (mars 2026)** : |
| | |   — Validation sur données réelles AP-HP (accès Clinical Data Warehouse) |
| | |   — Tests d'anonymisation (RGPD) pour les données AP-HP |
| | |   — Extension des règles Lung (données réelles TCGA-LUAD/LUSC) |
| | | • **Moyen terme (avril-mai 2026)** : |
| | |   — Soumission résumé conférence Frugalité (déadline à vérifier) |
| | |   — Validation de la méthodologie "highlighting" vs BRAT classique |
| | |   — Benchmarks multilingues (anglais, français, espagnol) |
| | | • **Long terme (juin 2026+)** : |
| | |   — Extension multi-cancer (colorectal, prostate, ovaire) |
| | |   — ClinJEPA (application JEPA au NER biomédical) |
| | |   — Préparation CIFRE Sorbonne 2027 : dossier, publications, recommandations |
| **12:15–13:30** | **Déjeuner + marche** | |
| **13:30–15:00** | **BLOC 3 — Email de synthèse à Dr. Redjdal** | |
| | | • Rédiger l'email de synthèse à Akram Redjdal avec : |
| | |   — Résumé des avancées (5 points clés + chiffres) |
| | |   — Les fichiers / scripts créés (liste avec rôle de chacun) |
| | |   — Questions en suspens (données AP-HP, validation highlighting, extension poumon) |
| | |   — Proposition de réunion pour la semaine suivante |
| | | • Préparer 3 slides de synthèse rapide (1 slide = 1 message fort) |
| 15:00 | **FIN DU TRAVAIL** | |
| 15:00–16:00 | **Marche** | |
| 16:00–22:00 | Repos complet — préparation de la reprise | |
| 22:00 | Coucher | |

---

## PHASE 3 — Post-Vacances : Validation et Publication (9–31 mars)

> **Note** : cette phase est esquissée ici pour la continuité. Elle sera détaillée à la fin de la Phase 2 dans le `BILAN_VACANCES.md`.

### Semaine du 9 mars — Validation AP-HP et extension poumon

- Réunion avec Dr. Redjdal : présentation des avancées, validation des choix techniques
- Demande d'accès aux données AP-HP (protocole éthique, RGPD)
- Exécution des règles Lung sur les données TCGA-LUAD/LUSC (public)
- Validation de l'annotation "highlighting" vs BRAT classique sur 20 documents

### Semaine du 16 mars — Benchmark multilingue et soumission

- Tests sur corpus anglais (TCGA) + français (AP-HP si accès) + espagnol (si corpus disponible)
- Finalisation du résumé Frugalité (relecture, vérification du format)
- Soumission à la conférence Frugalité

### Semaine du 23 mars — Préparation ESMO et ClinJEPA

- Préparation de la contribution ESMO 2025 (si déadline compatible)
- Démarrage de la réflexion sur l'architecture ClinJEPA
- Revue de la littérature JEPA appliqué au NER (arXiv récents)

---

# PARTIE III — RÉCAPITULATIFS

## Récapitulatif des livrables

| Livrable | Fichier cible | Jour cible | Statut initial |
|----------|--------------|-----------|----------------|
| État des lieux complet | `AUDIT_24FEV.md` | 24 fév | À créer |
| Métriques raffinées + tests | `E_*.py` + `tests/test_*.py` | 24–25 fév | Existants → améliorés |
| Métrique Yield | `E_annotation_yield.py` | 25 fév | À créer |
| Arbre calibré + Yield + visualisation | `E_creation_arbre_decision.py` + `visualize_decision_tree.py` | 26 fév | Existant → raffiné + nouveau |
| Configuration machine-lisible | `decision_config.json` | 26 fév | À créer |
| Seuils justifiés | `THRESHOLDS_JUSTIFICATION.md` | 26 fév | À créer |
| Module REST-interface complet | `REST_interface/` (7 fichiers) | 27 fév | À créer |
| Orchestrateur cascade | `cascade_orchestrator.py` | 28 fév | À créer |
| Tracking énergie | `energy_tracker.py` | 28 fév | À créer |
| Connecteurs Rules et NER | `rules_cascade_connector.py`, `ner_cascade_connector.py` | 28 fév–4 mars | À créer |
| Pipeline NER complet + évaluation | `5evaluate_ner.py` | 4 mars | À créer |
| Score composite | `E_composite_scorer.py` | 5 mars | À créer |
| Benchmarks (4 fichiers CSV) | `Results/benchmark_*.csv` | 5 mars | À créer |
| Figures publication (5 PNG) | `Results/figures/` | 5 mars | À créer |
| Résultats REST | `Results/REST_results/` | 5 mars | À créer |
| Notebook maître reproductible | `DuraXELL_Pipeline.ipynb` | 6 mars | `commandes.ipynb` → enrichi |
| README complet | `README.md` | 6 mars | À créer |
| Analyse de sensibilité | `sensitivity_analysis.py` | 7 mars | À créer |
| Extension poumon | `Rules/Lung/`, `NER/data/Lung/` | 7 mars | À créer |
| Résumé conférence Frugalité | `conference_frugalite_abstract.md` | 7 mars | À créer |
| Présentation conférence | `conference_frugalite_slides.pptx` | 7 mars | À créer |
| Bilan vacances + roadmap | `BILAN_VACANCES.md` | 8 mars | À créer |

---

## Récapitulatif activité physique quotidienne

| Jour | Matin | Midi | Soir | Estimé total |
|------|-------|------|------|--------------|
| 23 fév (pré-lancement) | 45 min | 30 min | — | ~6 000 pas |
| 24 fév | 45 min | 30 min | 60 min | ~12 000 pas |
| 25 fév | 45 min | 45 min | 60 min | ~14 000 pas |
| 26 fév | 45 min | 30 min | 60 min | ~13 000 pas |
| 27 fév | 45 min | 60 min | 60 min | ~15 000 pas |
| 28 fév | 45 min | 30 min | 60 min | ~13 000 pas |
| 1 mars (pause) | 90 min | — | 30 min | ~10 000 pas |
| 2 mars (pause) | 90 min | — | 60 min | ~12 000 pas |
| 3 mars (pause) | 60 min | 60 min | — | ~10 000 pas |
| 4 mars | 45 min | 30 min | 60 min + sport | ~14 000 pas |
| 5 mars | 45 min | 30 min | 60 min | ~13 000 pas |
| 6 mars | 45 min | 30 min | 45 min | ~11 000 pas |
| 7 mars | 45 min | 30 min | 60 min | ~13 000 pas |
| 8 mars | 60 min | 30 min | 60 min | ~12 000 pas |

**Total estimé sur 14 jours : ~162 000 pas (~130 km)**

---

## Note méthodologique finale (HDR — auto-évaluation v2)

Ce planning V2 est construit sur trois corrections critiques par rapport à la V1 :

**Correction 1 : ESMO2025 comme tissu conjonctif, pas comme module**
Chaque tâche est ancrée dans un fichier précis du dépôt ESMO2025. Il n'y a pas de tâche "générique" — chaque bloc de 90 minutes modifie ou crée un fichier identifié, avec une spec précise de ses entrées, sorties et API. La Partie I (Structure fichier par fichier) remplit exactement ce rôle : avant de coder, on sait exactement ce qu'on construit.

**Correction 2 : REST-interface comme validation, pas comme duplication**
La valeur de REST-interface de Guillaume Bazin n'est pas dans ses algorithmes (qui recoupent les métriques ESMO2025) mais dans son **empirisme**. REST valide les métriques en partant d'observations sur des annotations pilotes réelles. Le `rest_decision_bridge.py` est le composant qui formalise cette validation croisée. Si concordance ≥ 80%, les deux approches se valident mutuellement — c'est une contribution méthodologique publishable.

**Correction 3 : Temps illimité → qualité illimitée**
Sans contrainte de temps, la tâche principale n'est plus "avancer vite" mais "avancer juste". Cela se traduit concrètement par : des tests unitaires pour chaque métrique, une analyse de sensibilité des seuils, une vérification de reproductibilité complète, et une documentation qui permet à un tiers de reprendre le projet sans perte d'information. Ces éléments ne sont pas du luxe — ils sont la condition de la publiabilité et de la réutilisabilité du travail.
