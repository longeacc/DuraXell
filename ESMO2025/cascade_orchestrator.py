import json
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional, Union

import pandas as pd

# Ensure root path is available
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ESMO2025.structs import ExtractionResult

# Conditional imports to avoid hard crashes if modules are missing during dev
try:
    from ESMO2025.Rules.src.Breast.rules_cascade_connector import \
        RulesCascadeConnector
except ImportError:
    RulesCascadeConnector = None

try:
    from NER.src.ner_cascade_connector import NERCascadeConnector
except ImportError:
    NERCascadeConnector = None


class CascadeOrchestrator:
    """
    Orchestrateur principal de DuraXELL.
    Gère la cascade : Rules -> ML -> Transformer -> LLM
    Le niveau d'escalade maximal est contrôlé par l'arbre de décision.
    """

    CONFIDENCE_THRESHOLDS = {"HIGH": 0.9, "MEDIUM": 0.7, "LOW": 0.4}

    # Mapping méthode recommandée → niveau max d'escalade dans la cascade
    METHOD_MAX_LEVEL = {
        "RÈGLES": 1,
        "RÈGLES PAR DÉFAUT": 1,
        "ML LÉGER": 2,
        "ML LÉGER PAR DÉFAUT": 2,
        "TRANSFORMER BIDIRECTIONNEL": 3,
        "LLM": 4,
    }

    def __init__(
        self,
        config_path: str = "decision_config.json",
        rules_engine=None,  # RulesCascadeConnector
        ner_model=None,  # NERCascadeConnector
        llm_client=None,  # LLMClient
        energy_tracker=None,  # EnergyTracker
    ):
        self.config_path = config_path
        self.decision_config = self._load_config()

        # Initialize default connectors if available and not provided
        if rules_engine is None and RulesCascadeConnector:
            self.rules_engine = RulesCascadeConnector()
        else:
            self.rules_engine = rules_engine

        if ner_model is None and NERCascadeConnector:
            # Initialize with default discovery
            self.ner_model = NERCascadeConnector()
        else:
            self.ner_model = ner_model

        self.llm_client = llm_client
        self.energy_tracker = energy_tracker

        # Coûts énergétiques estimés par défaut si pas de tracker
        self.DEFAULT_ENERGY = {
            "Rules": 1e-6,
            "ML_CRF": 1e-5,
            "Transformer": 1e-4,
            "LLM": 1e-2,
        }

    def _load_config(self) -> Dict:
        """Charge la configuration de décision générée par l'arbre."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            print(f"Warning: {self.config_path} not found. Using defaults.")
            return {}

    def _get_entity_config(self, entity_type: str) -> Dict:
        """Récupère la config d'une entité depuis decision_config.json (gestion nesting 'entities')."""
        entities = self.decision_config.get("entities", self.decision_config)
        return entities.get(entity_type, {})

    def extract(self, document: str, entity_type: str) -> ExtractionResult:
        """
        Point d'entrée principal. Exécute la logique de cascade.
        Le niveau d'escalade est contrôlé par la méthode recommandée par l'arbre.
        """
        start_time = time.time()

        # 1. Déterminer la méthode recommandée par l'arbre de décision
        entity_cfg = self._get_entity_config(entity_type)
        recommended_method = entity_cfg.get("method", "RÈGLES PAR DÉFAUT")
        max_level = self.METHOD_MAX_LEVEL.get(recommended_method, 4)

        result = None
        logging.info(f"[Cascade] Entity={entity_type}, recommended={recommended_method}, max_level={max_level}")

        # Niveau 1 : RÈGLES (toujours essayé en premier — le moins coûteux)
        result = self._try_rules(document, entity_type)
        if self._is_confident(result) or max_level <= 1:
            if result and result.value is not None:
                result.execution_time_ms = (time.time() - start_time) * 1000
                return result
            if max_level <= 1:
                return self._finalize(result, entity_type, start_time)

        # Niveau 2/3 : ML / Transformer (si arbre autorise escalade)
        if max_level >= 2:
            ml_result = self._try_transformer(document, entity_type)
            if self._is_confident(ml_result):
                ml_result.execution_time_ms = (time.time() - start_time) * 1000
                return ml_result
            if ml_result and ml_result.value is not None:
                if result is None or result.value is None or ml_result.confidence > result.confidence:
                    result = ml_result

        # Niveau 4 : LLM (si arbre autorise et client disponible)
        if max_level >= 4 and self.llm_client:
            llm_result = self._try_llm(document, entity_type)
            if llm_result and llm_result.value is not None:
                llm_result.execution_time_ms = (time.time() - start_time) * 1000
                return llm_result

        return self._finalize(result, entity_type, start_time)

    def _finalize(self, result, entity_type, start_time):
        """Retourne le meilleur résultat ou un résultat vide."""
        if result is None or result.value is None:
            return ExtractionResult(entity_type, None, "None", 0.0, 0.0, 0)
        result.execution_time_ms = (time.time() - start_time) * 1000
        return result

    def _is_confident(self, result: ExtractionResult) -> bool:
        """Vérifie si le résultat dépasse le seuil de confiance acceptable."""
        if not result or result.value is None:
            return False
        return result.confidence >= self.CONFIDENCE_THRESHOLDS["MEDIUM"]

    def _try_rules(self, text: str, entity_type: str) -> ExtractionResult:
        """Tente l'extraction par règles regex."""
        energy = self.DEFAULT_ENERGY["Rules"]

        if self.rules_engine:
            # Appel au moteur de règles réel
            try:
                # Simulation d'appel avec mesure d'énergie si tracker dispo
                if self.energy_tracker:
                    with self.energy_tracker.measure("Rules", entity_type) as metrics:
                        res = self.rules_engine.predict(text, entity_type)
                    # Update result with measured energy
                    if res and metrics:
                        res.energy_kwh = metrics.get("kwh", 0.0)
                    return res
                else:
                    return self.rules_engine.predict(text, entity_type)
            except Exception as e:
                print(f"Error in rules engine: {e}")

        # Mock si pas de moteur
        return ExtractionResult(entity_type, None, "Rules", 0.0, energy, 1)

    def _try_transformer(self, text: str, entity_type: str) -> ExtractionResult:
        """Tente l'extraction par modèle Transformer (PubMedBERT/CancerBERT)."""
        energy = self.DEFAULT_ENERGY["Transformer"]

        if self.ner_model:
            try:
                if self.energy_tracker:
                    with self.energy_tracker.measure(
                        "Transformer", entity_type
                    ) as metrics:
                        res = self.ner_model.predict(text, entity_type)
                    if res and metrics:
                        res.energy_kwh = metrics.get("kwh", 0.0)
                    return res
                else:
                    return self.ner_model.predict(text, entity_type)
            except Exception as e:
                logging.debug(f"NER model error (non-blocking): {e}")

        # Mock
        return ExtractionResult(entity_type, None, "Transformer", 0.0, energy, 3)

    def _try_llm(self, text: str, entity_type: str) -> ExtractionResult:
        """Appelle le LLM en dernier recours."""
        energy = self.DEFAULT_ENERGY["LLM"]

        if self.llm_client:
            try:
                if self.energy_tracker:
                    with self.energy_tracker.measure("LLM", entity_type) as metrics:
                        res = self.llm_client.extract(text, entity_type)
                    if res and metrics:
                        res.energy_kwh = metrics.get("kwh", 0.0)
                    return res
                else:
                    return self.llm_client.extract(text, entity_type)
            except Exception as e:
                print(f"Error in LLM client: {e}")

        # Mock
        return ExtractionResult(entity_type, None, "LLM", 0.0, energy, 4)

    def extract_batch(
        self, documents: List[str], entity_types: List[str]
    ) -> pd.DataFrame:
        """Traitement par lot."""
        results = []
        for i, doc in enumerate(documents):
            for ent in entity_types:
                res = self.extract(doc, ent)
                row = res.to_dict()
                row["doc_id"] = i
                results.append(row)
        return pd.DataFrame(results)


if __name__ == "__main__":
    # Mock Rules Engine for testing
    class MockRulesEngine:
        def predict(self, text, entity):
            # Simulation simple : si le mot clé est présent, on renvoie un succès
            if entity == "Estrogen_receptor" and "Estrogen Receptor" in text:
                return ExtractionResult(
                    entity, "positive (100%)", "Rules", 0.95, 1e-6, 1
                )
            if entity == "HER2" and "HER2" in text:
                return ExtractionResult(entity, "negative", "Rules", 0.95, 1e-6, 1)
            return ExtractionResult(entity, None, "Rules", 0.0, 1e-6, 1)

    # Test simple interactif
    print("--- Initialisation de l'Orchestrateur DuraXELL ---")

    # On passe le moteur de règles simulé
    orch = CascadeOrchestrator(rules_engine=MockRulesEngine())
    print("Moteur de décision chargé avec Règles Simulées.")

    # Simulation de documents
    test_docs = [
        "Patient presents with Estrogen Receptor positive (100%) tumor. HER2 is negative.",
        "Invasive ductal carcinoma. Ki67 is high at 80%.",
    ]

    print("\n--- Démarrage de l'extraction (Mode Cascade) ---")
    for i, doc in enumerate(test_docs):
        print(f"\nDocument {i+1}: '{doc}'")

        # Test sur 2 entités
        for entity in ["Estrogen_receptor", "HER2"]:
            result = orch.extract(doc, entity)

            print(f"  > Entité: {entity}")
            print(
                f"    - Méthode choisie : {result.method_used} (Niveau {result.cascade_level})"
            )
            print(f"    - Valeur extraite : {result.value}")
            print(f"    - Énergie estimée : {result.energy_kwh:.8f} kWh")

    print("\n--- Test terminé ---")
