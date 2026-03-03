import time

class YieldCalculator:
    """
    Simulates the calculation of annotation yield based on time.
    Calculates how easy it is to empirically build rules or annotations for a given entity.
    """
    
    def __init__(self):
        self.metrics = {}

    def start_timing(self, entity_type):
        self.metrics[entity_type] = {"start": time.time(), "end": None, "yield": 0.0}

    def stop_timing(self, entity_type):
        if entity_type in self.metrics:
            self.metrics[entity_type]["end"] = time.time()
            # Mock formula for yield based on arbitrary timing
            duration = self.metrics[entity_type]["end"] - self.metrics[entity_type]["start"]
            # Inverse relationship: fast annotation = high yield
            self.metrics[entity_type]["yield"] = max(0.0, min(1.0, 1.0 - (duration / 60.0)))
            return self.metrics[entity_type]["yield"]
        return 0.0
