import os
import re
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from duraxell.Rules.src.Breast.biomarker_brat_annotator import \
    brat_annotate_biomarkers
from duraxell.structs import ExtractionResult

# English-to-abbreviation normalization patterns for compatibility
# with the French regex engine
_ENGLISH_NORMALIZATIONS = [
    (re.compile(r'\bestrogen\s+receptors?\b', re.IGNORECASE), 'ER'),
    (re.compile(r'\bprogesterone\s+receptors?\b', re.IGNORECASE), 'PR'),
]


class RulesCascadeConnector:
    """
    Connecteur pour le moteur de règles Regex (Breast).
    Utilise biomarker_brat_annotator.py.
    """

    def __init__(self):
        # Le moteur est stateless (juste des fonctions regex), pas d'init lourd
        pass

    def predict(self, text: str, entity_type: str) -> ExtractionResult:
        """
        Exécute l'extraction par règles sur le texte.
        Mappe le type d'entité demandé vers le type de l'annotateur.
        """
        # Mapping des noms d'entités (DuraXELL -> Annotateur Regex)
        # ESTROGEN -> "Estrogen_receptor"
        # PROGESTERONE -> "Progesterone_receptor"
        # HER2 -> "HER2_status"
        # Ki67 -> "Ki67"

        target_label = entity_type
        if entity_type == "ER" or entity_type == "Estrogen Receptor":
            target_label = "Estrogen_receptor"
        elif entity_type == "PR" or entity_type == "Progesterone Receptor":
            target_label = "Progesterone_receptor"
        elif entity_type == "HER2":
            target_label = "HER2_status"

        # Appel à l'annotateur existant
        # Retourne liste de tuples: (span_text, start, end, label, value)
        annotations = brat_annotate_biomarkers(text)

        # Filtrer pour l'entité demandée
        matches = [ann for ann in annotations if ann[3] == target_label]

        # If no matches with original text, try English-to-abbreviation normalization
        if not matches:
            normalized_text = text
            for pattern, replacement in _ENGLISH_NORMALIZATIONS:
                normalized_text = pattern.sub(replacement, normalized_text)
            if normalized_text != text:
                annotations = brat_annotate_biomarkers(normalized_text)
                matches = [ann for ann in annotations if ann[3] == target_label]

        if not matches:
            return ExtractionResult(
                entity_type=entity_type,
                value=None,
                method_used="Rules",
                confidence=0.0,
                energy_kwh=0.0,  # Sera rempli par l'orchestrateur via EnergyTracker
                cascade_level=1,
            )

        # Si on a des matchs, on prend le premier (ou le plus pertinent)
        # Pour l'instant : premier match
        span_text, start, end, label, value = matches[0]

        # Confiance basée sur le Yield IoU (F1 Rules vs GS, IoU≥0.5) de l'entité.
        _YIELD_BY_ENTITY = {
            "Estrogen_receptor": 0.75, "Progesterone_receptor": 0.73,
            "Ki67": 0.92, "HER2_status": 0.47, "HER2_IHC": 0.73,
            "HER2_FISH": 0.19, "Genetic_mutation": 0.0,
        }
        base_yield = _YIELD_BY_ENTITY.get(entity_type, 0.5)
        # Confidence = base yield + 0.10 bonus pour match regex (capped at 0.95)
        confidence = min(0.95, base_yield + 0.10)

        return ExtractionResult(
            entity_type=entity_type,
            value=value,  # La valeur normalisée extraite par le regex
            method_used="Rules",
            confidence=confidence,
            energy_kwh=0.0,
            cascade_level=1,
            span=(start, end),
            metadata={"raw_span": span_text},
        )
