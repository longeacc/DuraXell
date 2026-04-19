from math import pi

import matplotlib.pyplot as plt
import pandas as pd


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
        "RÈGLES": 1.0,
        "TBM": 0.3,
        "LLM": 0.1,
    }

    def __init__(self, max_energy_kwh: float = 0.01):
        """
        Initialise le scorer.
        Args:
            max_energy_kwh: Seuil de référence pour normaliser l'énergie
                            (ex: 0.01 = coût estimé d'un appel API LLM lourd).
        """
        self.MAX_ENERGY_KWH = max_energy_kwh

    def compute(
        self,
        f1: float,
        method: str,
        energy_kwh: float,
        alpha: float = 0.4,
        beta: float = 0.3,
        gamma: float = 0.3,
    ) -> float:
        """
        Calcule le score composite pour une extraction.

        Args:
            f1: F1-score (0.0 à 1.0)
            method: Nom de la méthode (pour le score d'explicabilité)
            energy_kwh: Consommation en kWh
            alpha, beta, gamma: Poids respectifs (doivent sommer à 1.0 idéalement)

        Returns:
            Score composite entre 0.0 et 1.0
        """
        expl_score = self.EXPLAINABILITY_SCORES.get(method, 0.1)

        # Normalisation de l'énergie : 1.0 = très économe, 0.0 = très énergivore
        # On utilise une échelle log ou linéaire bornée. Ici linéaire bornée pour simplifier.
        # E_norm = 1 - (energy / max_energy)
        norm_energy = max(0.0, 1.0 - (energy_kwh / self.MAX_ENERGY_KWH))

        composite = (alpha * f1) + (beta * expl_score) + (gamma * norm_energy)
        return composite

    def pareto_analysis(self, results: pd.DataFrame) -> pd.DataFrame:
        """
        Identifie les configurations Pareto-optimales.
        Suppose que 'results' a les colonnes : ['Method', 'Entity', 'F1', 'Energy_kWh']
        """
        df = results.copy()

        # Ajouter colonne Explicabilité
        df["Explainability"] = df["Method"].map(lambda m: self.EXPLAINABILITY_SCORES.get(m, 0.1))

        # Ajouter colonne Énergie inversée (pour maximiser)
        df["Energy_Score"] = df["Energy_kWh"].map(
            lambda e: max(0.0, 1.0 - (e / self.MAX_ENERGY_KWH))
        )

        # Calcul du score composite
        df["Composite_Score"] = df.apply(
            lambda row: self.compute(row["F1"], row["Method"], row["Energy_kWh"]),
            axis=1,
        )

        # Identification Pareto simple (sur F1 vs Energy)
        # Une solution est dominée si une autre solution a un meilleur F1 ET une meilleure Énergie (moins de kWh)
        is_pareto = []
        for i, row in df.iterrows():
            dominated = False
            for j, other in df.iterrows():
                if i == j:
                    continue
                # Si l'autre est meilleure ou égale partout et strictement meilleure sur au moins un critère
                if (
                    other["F1"] >= row["F1"]
                    and other["Explainability"] >= row["Explainability"]
                    and other["Energy_kWh"] <= row["Energy_kWh"]
                ):
                    if (
                        other["F1"] > row["F1"]
                        or other["Explainability"] > row["Explainability"]
                        or other["Energy_kWh"] < row["Energy_kWh"]
                    ):
                        dominated = True
                        break
            is_pareto.append(not dominated)

        df["Is_Pareto"] = is_pareto
        return df

    def radar_plot(self, results: pd.DataFrame, output_path: str) -> None:
        """
        Génère le graphique radar (spider chart) comparant les méthodes.
        'results' doit être agrégé par méthode (moyenne des entités).
        """
        categories = ["Performance (F1)", "Explicabilité", "Frugalité (1-Energy)"]
        n = len(categories)

        angles = [n / float(n) * 2 * pi for n in range(n)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Pour chaque méthode
        for method in results["Method"].unique():
            row = results[results["Method"] == method].iloc[0]

            f1 = row["F1"]
            expl = self.EXPLAINABILITY_SCORES.get(method, 0.1)
            frugality = max(0.0, 1.0 - (row["Energy_kWh"] / self.MAX_ENERGY_KWH))

            values = [f1, expl, frugality]
            values += values[:1]

            ax.plot(angles, values, linewidth=1, linestyle="solid", label=method)
            ax.fill(angles, values, alpha=0.1)

        plt.xticks(angles[:-1], categories)
        plt.yticks(
            [0.2, 0.4, 0.6, 0.8, 1.0],
            ["0.2", "0.4", "0.6", "0.8", "1.0"],
            color="grey",
            size=7,
        )
        plt.ylim(0, 1)
        plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))

        plt.title("Compromis Performance-Explicabilité-Énergie")
        plt.savefig(output_path)
        plt.close()


if __name__ == "__main__":
    # Test simple
    scorer = CompositeScorer()

    # Simulation de données
    data = [
        {"Method": "Rules", "Entity": "ER", "F1": 0.95, "Energy_kWh": 0.000001},
        {"Method": "Transformer", "Entity": "ER", "F1": 0.96, "Energy_kWh": 0.0001},
        {"Method": "LLM", "Entity": "ER", "F1": 0.90, "Energy_kWh": 0.01},
    ]
    df = pd.DataFrame(data)

    print("--- Calcul des scores ---")
    df_scores = scorer.pareto_analysis(df)
    print(df_scores[["Method", "Composite_Score", "Is_Pareto"]])

    # Test radar plot (nécessite aggregation, ici on triche un peu pour le test)
    # scorer.radar_plot(df, "Results/figures/test_radar.png")
