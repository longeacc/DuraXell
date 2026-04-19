import pandas as pd
from unittest.mock import patch

from duraxell.energy_tracker import EnergyTracker


class TestEnergyTracker:
    def test_simulation_fallback(self):
        """Test behavior when eco2ai is not installed (simulated context)."""
        # Patch HAS_ECO2AI to False for this test
        with patch("duraxell.energy_tracker.HAS_ECO2AI", False):
            tracker = EnergyTracker()
            assert tracker.tracker is None

            with tracker.measure(method="Rules", entity_type="Gene"):
                pass

            # Verify log entry exists and has simulated values
            assert len(tracker.log_data) == 1
            entry = tracker.log_data[0]
            assert entry["method"] == "Rules"
            assert entry["energy_kwh"] > 0
            # Rough check: Rules should be very low energy
            assert entry["energy_kwh"] < 0.001

    def test_eco2ai_execution(self):
        """Test behavior when eco2ai is installed and working."""
        # Patch HAS_ECO2AI to True
        with patch("duraxell.energy_tracker.HAS_ECO2AI", True):
            # Temporarily remove pytest and unittest from sys.modules
            import sys

            original_modules = sys.modules.copy()
            sys.modules.pop("pytest", None)
            sys.modules.pop("unittest", None)

            with patch("sys.argv", ["python"]):
                try:
                    # Patch the Tracker class
                    with patch("duraxell.energy_tracker.Tracker") as MockTracker:
                        # Patch os.path.exists and pandas.read_csv to simulate reading the log file
                        with (
                            patch("os.path.exists") as mock_exists,
                            patch("pandas.read_csv") as mock_read_csv,
                        ):
                            # Setup mocks
                            mock_instance = MockTracker.return_value
                            mock_exists.return_value = True

                            # Mock the CSV dataframe returned by pandas
                            # The code expects columns: 'power_consumption(kWh)', 'CO2_emissions(kg)'
                            mock_df = pd.DataFrame(
                                {
                                    "power_consumption(kWh)": [0.0005],
                                    "CO2_emissions(kg)": [0.00025],
                                }
                            )
                            mock_read_csv.return_value = mock_df

                            tracker = EnergyTracker()
                            assert tracker.tracker is not None

                            with tracker.measure(method="ML_CRF", entity_type="Tumor"):
                                pass

                            # Verify calls
                            mock_instance.start.assert_called_once()
                            mock_instance.stop.assert_called_once()

                            # Verify log uses the mocked values
                            entry = tracker.log_data[0]
                            assert entry["energy_kwh"] == 0.0005
                            # kg to g conversion: 0.00025 * 1000 = 0.25
                            assert entry["co2_g"] == 0.25
                finally:
                    sys.modules.clear()
                    sys.modules.update(original_modules)

    def test_access_yielded_metrics(self):
        """Test accessing the mutable energy metrics yielded by the context manager."""
        with patch("duraxell.energy_tracker.HAS_ECO2AI", False):
            tracker = EnergyTracker()

            with tracker.measure(method="Rules", entity_type="Gene") as metrics:
                # Inside the block, values are initialized but zero
                assert metrics["kwh"] == 0.0
                assert metrics["co2"] == 0.0

            # After the block, values should be populated
            assert metrics["kwh"] > 0
            assert metrics["co2"] > 0
            assert metrics["duration"] >= 0

    def test_summary(self):
        tracker = EnergyTracker()
        tracker.log("Rules", "Gene", 0.001, 0.5, 100)
        tracker.log("ML", "Gene", 0.002, 1.0, 200)

        summary = tracker.summary()
        assert len(summary) == 2
        assert "energy_kwh" in summary.columns
