"""Routage simplifié DuraXell — Arbre à 4 nœuds, 3 sorties."""

from typing import Dict, Tuple

def compute_routing(
    metrics: Dict[str, float], thresholds: Dict[str, float]
) -> Tuple[str, str]:
    """Arbre de décision simplifié : Te++ → He++ → R− → RÈGLES | Feas++ → TBM | LLM.

    Args:
        metrics: Métriques de l'entité (Te, He, R, Feas sur échelle [0-1]).
        thresholds: Seuils de routage (Te, He, R, Feas sur échelle [0-1]).

    Returns:
        Tuple (méthode, justification).
    """
    Te: float = metrics.get("Te", 0)
    He: float = metrics.get("He", 0)
    R: float = metrics.get("R", 0)
    Feas: float = metrics.get("Feas", 0)

    # Seuils par défaut (échelle 0-1, cohérent avec metrics.py)
    t_te: float = thresholds.get("Te", 0.70)
    t_he: float = thresholds.get("He", 0.70)
    t_r: float = thresholds.get("R", 0.30)
    t_feas: float = thresholds.get("Feas", 0.60)

    # Branche RÈGLES : Te élevée + He élevée + R faible
    if Te >= t_te and He >= t_he and R <= t_r:
        return "RÈGLES", f"Te={Te:.2f}≥{t_te}, He={He:.2f}≥{t_he}, R={R:.3f}≤{t_r}"

    # Branche TBM : Faisabilité suffisante
    if Feas >= t_feas:
        return "TBM", f"Feas={Feas:.3f}≥{t_feas}"

    # Branche LLM : fallback
    return "LLM", "Conditions RÈGLES et TBM non satisfaites"
