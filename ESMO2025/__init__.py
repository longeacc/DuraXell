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

from .E_annotation_yield import AnnotationYieldScorer
from .E_creation_arbre_decision import DecisionTreeBuilder
from .E_frequency import FrequencyScorer
from .E_homogeneity import HomogeneityScorer
from .E_risk_context import RiskContextScorer
from .E_templeability import TempleabilityScorer

# Alias for backward compatibility if needed, else just use Builder
DecisionTree = DecisionTreeBuilder

from .cascade_orchestrator import CascadeOrchestrator
from .E_composite_scorer import CompositeScorer
from .energy_tracker import EnergyTracker

__version__ = "2.0.0"
__all__ = [
    "TempleabilityScorer",
    "HomogeneityScorer",
    "RiskContextScorer",
    "FrequencyScorer",
    "AnnotationYieldScorer",
    "DecisionTree",
    "CascadeOrchestrator",
    "EnergyTracker",
    "CompositeScorer",
]
