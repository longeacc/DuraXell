"""Routage simplifié DuraXell — Arbre à 4 nœuds, 3 sorties."""


def compute_routing(metrics: dict[str, float], thresholds: dict[str, float]) -> tuple[str, str]:
    """Arbre de décision simplifié : Te++ → He++ → R− → RÈGLES | Feas++ → TBM | LLM.

    Args:
        metrics: Métriques de l'entité (Te, He, R, Feas sur échelle [0-1]).
        thresholds: Seuils de routage (Te, He, R, Feas sur échelle [0-1]).

    Returns:
        Tuple (méthode, justification).
    """
    te: float = metrics.get("te", 0)
    he: float = metrics.get("he", 0)
    r: float = metrics.get("r", 0)
    feas: float = metrics.get("feas", 0)

    # Seuils par défaut (échelle 0-1, cohérent avec metrics.py)
    t_te: float = thresholds.get("Te", 0.70)
    t_he: float = thresholds.get("He", 0.70)
    t_r: float = thresholds.get("R", 0.30)
    t_feas: float = thresholds.get("Feas", 0.60)

    # Branche RÈGLES : Te élevée + He élevée + R faible
    if te >= t_te and he >= t_he and r <= t_r:
        return "RÈGLES", f"Te={te:.2f}≥{t_te}, He={he:.2f}≥{t_he}, R={r:.3f}≤{t_r}"

    # Branche TBM : Faisabilité suffisante
    if feas >= t_feas:
        return "TBM", f"Feas={feas:.3f}≥{t_feas}"

    # Branche LLM : fallback
    return "LLM", "Conditions RÈGLES et TBM non satisfaites"
