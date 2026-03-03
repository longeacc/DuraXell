import sys
from unittest.mock import MagicMock

# Force eco2ai to be missing or mocked for all tests to prevent hardware access/threading
# This simple trick simulates ImportError for eco2ai
# sys.modules["eco2ai"] = None 
# OR we can mock it if code depends on it existing but we want to control it.
# Given EnergyTracker uses try/except ImportError, setting it to None should trigger the except block.

# However, if it was already imported by another test discovery, this might be late.
# But conftest is loaded early.

# Let's try mocking it so it exists but does nothing, in case we want to test that path later.
# But for now, ensuring HAS_ECO2AI = False is safer.
sys.modules["eco2ai"] = None
