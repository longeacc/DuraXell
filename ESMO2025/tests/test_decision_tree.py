import sys
from unittest.mock import MagicMock
# Mock eco2ai BEFORE importing E_creation_arbre_decision
sys.modules["eco2ai"] = MagicMock()

import pytest
from ESMO2025.E_creation_arbre_decision import DecisionTreeBuilder

def test_decision_tree_logic():
    # Setup builder with dummy path
    builder = DecisionTreeBuilder(config_path="dummy.json")

    # Case 1: High Te (90), High He (80), Low Risk (0.1) -> FEUILLE NER À BASE DE RÈGLES
    metrics_struct = {"Te": 90.0, "He": 80.0, "R": 0.1}
    res1 = builder.analyze_entity("StructureOnly", metrics_struct)
    assert res1["method"] == "FEUILLE NER À BASE DE RÈGLES"

    # Case 2: Med Te (50), High Yield (0.8), High Freq (0.05) -> FEUILLE ML LÉGER NER
    metrics_yield = {"Te": 50.0, "He": 20.0, "Freq": 0.05, "Yield": 0.9}
    res2 = builder.analyze_entity("GoodRules", metrics_yield)
    assert res2["method"] == "FEUILLE ML LÉGER NER"

    # Case 3: High Feas (0.8), Low Domain Shift (0.1) -> FEUILLE NER TRANSFORMER BIDIRECTIONNEL
    metrics_ml = {"Te": 10.0, "He": 10.0, "R": 0.2, "Feas": 0.8, "DomainShift": 0.1}
    res3 = builder.analyze_entity("CommonEntity", metrics_ml)
    assert res3["method"] == "FEUILLE NER TRANSFORMER BIDIRECTIONNEL"

    # Case 4: High LLM Necessity (0.8) -> FEUILLE NER LLM
    metrics_llm = {"Te": 10.0, "He": 10.0, "R": 0.8, "Feas": 0.8, "DomainShift": 0.6, "LLM_Necessity": 0.8}
    res4 = builder.analyze_entity("RiskyEntity", metrics_llm)
    assert res4["method"] == "FEUILLE NER LLM"

    # Case 5: Default ML Backoff -> FEUILLE ML LÉGER PAR DÉFAUT (Freq >= 0.001)
    metrics_backoff_ml = {"Te": 10.0, "Feas": 0.0, "LLM_Necessity": 0.1, "Freq": 0.005}
    res5 = builder.analyze_entity("RareRisky", metrics_backoff_ml)
    assert res5["method"] == "FEUILLE ML LÉGER PAR DÉFAUT"

    # Case 6: Default Rules Backoff -> FEUILLE RÈGLES PAR DÉFAUT (Freq < 0.001)
    metrics_backoff_rules = {"Te": 10.0, "Feas": 0.0, "LLM_Necessity": 0.1, "Freq": 0.0001}
    res6 = builder.analyze_entity("RareSimple", metrics_backoff_rules)
    assert res6["method"] == "FEUILLE RÈGLES PAR DÉFAUT"
