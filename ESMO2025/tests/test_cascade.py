import sys
import os
from unittest.mock import MagicMock, patch
import pandas as pd
import pytest

# Ensure root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Pre-mock eco2ai to prevent import side effects
sys.modules["eco2ai"] = MagicMock()

from ESMO2025.structs import ExtractionResult
from ESMO2025.cascade_orchestrator import CascadeOrchestrator
from ESMO2025.energy_tracker import EnergyTracker

# FORCE HAS_ECO2AI to False for all tests in this file
import ESMO2025.energy_tracker
ESMO2025.energy_tracker.HAS_ECO2AI = False

# Mock Connectors
class MockRulesConnector:
    def predict(self, text, entity):
        if entity == "Estrogen_receptor":
            return ExtractionResult(
                entity_type=entity,
                value="Positive",
                method_used="Rules",
                confidence=1.0,
                cascade_level=1
            )
        return ExtractionResult(entity, None, "Rules", 0.0)

class MockNERConnector:
    def predict(self, text, entity):
        if entity == "Ki67":
            return ExtractionResult(
                entity_type=entity,
                value="20%",
                method_used="Transformer",
                confidence=0.8,
                cascade_level=2
            )
        return ExtractionResult(entity, None, "Transformer", 0.0)

@pytest.fixture
def orchestrator():
    # Patch HAS_ECO2AI to False globally for the orchestrator fixture
    # This prevents the real eco2ai Tracker from initializing and starting threads
    with patch("ESMO2025.energy_tracker.HAS_ECO2AI", False):
        tracker = EnergyTracker()
        
    return CascadeOrchestrator(
        rules_engine=MockRulesConnector(),
        ner_model=MockNERConnector(),
        energy_tracker=tracker
    )

def test_extract_rules_success(orchestrator):
    # Configure decision to prefer Rules for Estrogen
    # Ensure orchestrator respects config
    orchestrator.decision_config = {
        "Estrogen_receptor": {"method": "REGLES"}
    }
    
    # Patch eco2ai check to ensure simulation
    with patch("ESMO2025.energy_tracker.HAS_ECO2AI", False):
        res = orchestrator.extract("Patient has ER positive tumor.", "Estrogen_receptor")
     
    assert res.value == "Positive"
    assert res.method_used == "Rules"
    assert res.confidence == 1.0
    # Check that energy calculation occurred (simulation returns > 0)
    assert res.energy_kwh > 0.0

def test_extract_transformer_fallback(orchestrator):
    # Case: Entity configured for Transformer
    orchestrator.decision_config = {
        "Ki67": {"method": "Transformer"}
    }
    
    with patch("ESMO2025.energy_tracker.HAS_ECO2AI", False):
        res = orchestrator.extract("Ki67 index is 20%.", "Ki67")
        
    assert res.value == "20%"
    assert res.method_used == "Transformer"
    assert res.cascade_level == 2
    assert res.energy_kwh > 0.0

def test_energy_tracking_integration(orchestrator):
    orchestrator.decision_config = {"Estrogen_receptor": {"method": "REGLES"}}
    
    # Mock the tracker.measure context manager behavior
    # We want measure() to return a mock object that acts as context manager
    # AND yields a metrics dict that we can control.
    
    metric_mock = {"kwh": 0.005, "co2": 0.25, "duration": 10.0}
    
    # Proper context manager mock
    cm = MagicMock()
    cm.__enter__.return_value = metric_mock
    cm.__exit__.return_value = None
    
    orchestrator.energy_tracker.measure = MagicMock(return_value=cm)
        
    res = orchestrator.extract("Text", "Estrogen_receptor")
    
    # Verify measure was called
    orchestrator.energy_tracker.measure.assert_called_with("Rules", "Estrogen_receptor")
    
    # Verify kwh was propagated from metric_mock to result
    # If orchestrator correctly uses "with measure() as metrics:"
    assert res.energy_kwh == metric_mock["kwh"]

def test_batch_extraction(orchestrator):
    docs = ["Doc 1", "Doc 2"]
    ents = ["Estrogen_receptor", "Ki67"]
    
    # Setup config for mixed methods
    orchestrator.decision_config = {
        "Estrogen_receptor": {"method": "REGLES"},
        "Ki67": {"method": "Transformer"}
    }
    
    with patch("ESMO2025.energy_tracker.HAS_ECO2AI", False):
        df = orchestrator.extract_batch(docs, ents)
    
    assert len(df) == 4 # 2 docs * 2 entities
    assert "energy_kwh" in df.columns
    # Check that we have results for both types
    assert "Rules" in df["method_used"].values
    assert "Transformer" in df["method_used"].values
