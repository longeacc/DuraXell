import math
from typing import Dict, Any

ENTITIES = ["ER", "PR", "HER2_status", "HER2_IHC", "Ki67", "HER2_FISH", "Genetic_mutation"]

DEMO_METRICS = {
    "ER": {"Te": 0.92, "He": 0.88, "R": 0.94, "Freq": 0.85, "Yield": 0.91, "Feas": 0.95, "DomainShift": 0.82, "LLM_Necessity": 0.15, "C": 0.02},
    "PR": {"Te": 0.90, "He": 0.86, "R": 0.92, "Freq": 0.83, "Yield": 0.89, "Feas": 0.93, "DomainShift": 0.80, "LLM_Necessity": 0.18, "C": 0.02},
    "HER2_status": {"Te": 0.72, "He": 0.68, "R": 0.78, "Freq": 0.75, "Yield": 0.74, "Feas": 0.85, "DomainShift": 0.70, "LLM_Necessity": 0.45, "C": 0.12},
    "HER2_IHC": {"Te": 0.68, "He": 0.65, "R": 0.72, "Freq": 0.70, "Yield": 0.70, "Feas": 0.82, "DomainShift": 0.68, "LLM_Necessity": 0.50, "C": 0.15},
    "Ki67": {"Te": 0.55, "He": 0.52, "R": 0.60, "Freq": 0.72, "Yield": 0.65, "Feas": 0.78, "DomainShift": 0.58, "LLM_Necessity": 0.62, "C": 0.25},
    "HER2_FISH": {"Te": 0.42, "He": 0.45, "R": 0.48, "Freq": 0.25, "Yield": 0.55, "Feas": 0.60, "DomainShift": 0.50, "LLM_Necessity": 0.78, "C": 0.45},
    "Genetic_mutation": {"Te": 0.35, "He": 0.38, "R": 0.40, "Freq": 0.15, "Yield": 0.48, "Feas": 0.55, "DomainShift": 0.42, "LLM_Necessity": 0.88, "C": 0.65}
}

ROUTING_COLORS = {
    "RULES": "#2E7D32",         # Vert
    "CRF": "#1976D2",           # Bleu
    "TRANSFORMER": "#F57C00",   # Orange
    "LLM": "#C62828"            # Rouge
}

def compute_routing(metrics: Dict[str, float], thresholds: Dict[str, float]) -> str:
    """
    Détermine la méthode optimale pour une entité en cascade.
    
    Args:
        metrics (Dict[str, float]): Dictionnaire de métriques pour une entité.
        thresholds (Dict[str, float]): Dictionnaire des seuils correspondants.
        
    Returns:
        str: Méthode de routage recommandée ("RULES", "CRF", "TRANSFORMER", "LLM").
    """
    Te, He, R = metrics.get("Te", 0), metrics.get("He", 0), metrics.get("R", 0)
    Freq, Yield = metrics.get("Freq", 0), metrics.get("Yield", 0)
    DS, Feas = metrics.get("DomainShift", 0), metrics.get("Feas", 0)
    
    # Niveau 1 : Rules (coût minimal)
    if Te >= thresholds["Te"] and He >= thresholds["He"] and R >= thresholds["R"]:
        return "RULES"
    
    # Niveau 2 : CRF (compromis)
    if Freq >= thresholds["Freq"] and Yield >= thresholds["Yield"]:
        return "CRF"
    
    # Niveau 3 : Transformer
    if DS >= thresholds["DomainShift"] and Feas >= thresholds["Feas"]:
        return "TRANSFORMER"
    
    # Niveau 4 : LLM (complexité maximale)
    return "LLM"
