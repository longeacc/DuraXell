from unittest.mock import patch

import pandas as pd

from duraxell.cascade_orchestrator import CascadeOrchestrator, ExtractionResult
from duraxell.E_composite_scorer import CompositeScorer
from duraxell.energy_tracker import EnergyTracker


class MockRulesEngine:
    def predict(self, text, entity):
        if "HER2 negative" in text and entity == "HER2":
            return ExtractionResult(entity, "Negative", "RÈGLES", 1.0, 0, 1)
        return None


class MockNERModel:
    def predict(self, text, entity):
        if "HER2 is negative" in text and entity == "HER2_status":
            return ExtractionResult(entity, "Negative", "TBM", 0.85, 0, 2)
        return None


class TestPipelineIntegration:
    @patch("duraxell.energy_tracker.HAS_ECO2AI", False)
    def test_full_validation_loop(self):
        """
        Simulate a full validation run:
        1. Initialize Orchestrator with EnergyTracker.
        2. Process a batch of documents.
        3. Collect results (Confidence, Energy).
        4. Compare with Ground Truth to get 'Performance' (Accuracy/F1).
        5. Use CompositeScorer to rate the pipeline's performance.
        """

        # 1. Setup
        tracker = EnergyTracker()
        orchestrator = CascadeOrchestrator(
            rules_engine=MockRulesEngine(),
            ner_model=MockNERModel(),
            energy_tracker=tracker,
        )

        # Documents and Ground Truth
        dataset = [
            {
                "text": "Patient has HER2 negative tumor.",
                "entity": "HER2",
                "gt": "Negative",
            },
            {
                "text": "Patient has HER2 is negative tumor.",
                "entity": "HER2_status",
                "gt": "Negative",
            },
            {
                "text": "Unknown entity.",
                "entity": "ER",
                "gt": "None",
            },  # Should fail/return None
        ]

        results_data = []

        # 2. Execution Loop
        for item in dataset:
            text = item["text"]
            entity = item["entity"]

            # Extract
            result = orchestrator.extract(text, entity)

            # 3. Collect Data
            # Simple accuracy check
            is_correct = (result.value == item["gt"]) or (
                result.value is None and item["gt"] == "None"
            )

            results_data.append(
                {
                    "Entity": entity,
                    "Method": result.method_used,
                    "Value": result.value,
                    "GroundTruth": item["gt"],
                    "IsCorrect": is_correct,
                    "Energy_kWh": result.energy_kwh,
                    "Confidence": result.confidence,
                }
            )

        df_results = pd.DataFrame(results_data)

        # 4. Compute Metrics
        # Aggregate by Method to see how each component performed
        method_group = (
            df_results.groupby("Method")
            .agg(
                {
                    "IsCorrect": "mean",  # Accuracy as proxy for F1
                    "Energy_kWh": "mean",
                }
            )
            .reset_index()
        )

        method_group.rename(columns={"IsCorrect": "F1"}, inplace=True)  # Renaming for scorer

        # 5. Composite Scoring
        scorer = CompositeScorer()

        # Compute composite score for each method used in this pipeline run
        method_group["CompositeScore"] = method_group.apply(
            lambda row: scorer.compute(
                f1=row["F1"], method=row["Method"], energy_kwh=row["Energy_kWh"]
            ),
            axis=1,
        )

        # Assertions to verify integration
        assert not df_results.empty
        assert "RÈGLES" in method_group["Method"].values
        assert "TBM" in method_group["Method"].values

        # Verify energy was captured (simulated)
        assert df_results["Energy_kWh"].sum() > 0

        # Verify composite score calculation
        assert method_group["CompositeScore"].min() >= 0.0
        assert method_group["CompositeScore"].max() <= 1.0

        print("\nPipeline Integration Results:")
        print(method_group)
