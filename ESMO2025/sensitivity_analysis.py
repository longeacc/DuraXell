import copy
import json
import os
import sys

import pandas as pd

# Import du constructeur d'arbre pour pouvoir le ré-exécuter
# On suppose que E_creation_arbre_decision.py contient une classe utilisable
# Sinon, on devrait importer la logique. Pour l'instant, on simule la logique ici
# ou on importe si possible.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from E_creation_arbre_decision import DecisionTreeBuilder
except ImportError:
    # Si l'import échoue (ex: code non encapsulé dans une classe), on définit une version simplifiée
    # pour l'analyse de sensibilité.
    class DecisionTreeBuilder:
        def __init__(self):
            self.thresholds = {
                "TE_HIGH": 0.5,
                "TE_LOW": 0.2,
                "HE_HIGH": 0.7,
                "RISK_LOW": 0.5,
                "FREQ_HIGH": 0.05,
                "YIELD_HIGH": 0.75,
            }

        def decide(self, metrics, thresholds=None):
            th = thresholds if thresholds else self.thresholds
            # Logique répliquée de l'arbre
            if metrics.get("Te", 0) > th["TE_HIGH"]:
                if metrics.get("Risk", 1) < th["RISK_LOW"]:
                    return "REGLES"
                else:
                    return "ML_NER"
            # ... suite simplifiée ...
            return "ML_NER"  # Default


def run_sensitivity_analysis(
    metrics_data: dict,  # Les métriques brutes pour chaque entité
    base_config: dict,
    thresholds_to_vary: list = ["TE_HIGH", "TE_LOW", "HE_HIGH", "RISK_LOW"],
    perturbation_pct: list = [-0.2, -0.1, 0.1, 0.2],
) -> pd.DataFrame:
    """
    Analyse de sensibilité des seuils.
    """
    builder = DecisionTreeBuilder()
    base_thresholds = builder.thresholds.copy()

    results = []

    # Évaluation de base
    base_decisions = {}
    for entity, metrics in metrics_data.items():
        base_decisions[entity] = builder.decide(metrics, base_thresholds)

    # Perturbations
    for threshold_name in thresholds_to_vary:
        if threshold_name not in base_thresholds:
            continue

        original_val = base_thresholds[threshold_name]

        for pct in perturbation_pct:
            new_val = original_val * (1 + pct)

            # Config temporaire
            temp_thresholds = base_thresholds.copy()
            temp_thresholds[threshold_name] = new_val

            # Recalcul des décisions
            changes = 0
            changed_entities = []

            for entity, metrics in metrics_data.items():
                new_decision = builder.decide(metrics, temp_thresholds)
                if new_decision != base_decisions[entity]:
                    changes += 1
                    changed_entities.append(entity)

            results.append(
                {
                    "threshold": threshold_name,
                    "perturbation": f"{pct*100:+.0f}%",
                    "original_value": original_val,
                    "new_value": new_val,
                    "n_changes": changes,
                    "changed_entities": ", ".join(changed_entities),
                    "robustness": (
                        1.0 - (changes / len(metrics_data)) if metrics_data else 1.0
                    ),
                }
            )

    return pd.DataFrame(results)


if __name__ == "__main__":
    # Mock data pour test
    metrics_mock = {
        "ER": {"Te": 0.6, "He": 0.8, "Risk": 0.1},
        "HER2": {"Te": 0.8, "He": 0.9, "Risk": 0.2},
        "Tumeur": {"Te": 0.1, "He": 0.2, "Risk": 0.8},
    }

    df = run_sensitivity_analysis(metrics_mock, {})
    print(df)
