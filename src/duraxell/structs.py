from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


@dataclass
class ExtractionResult:
    entity_type: str
    value: Optional[str]
    method_used: str
    confidence: float
    energy_kwh: float = 0.0
    cascade_level: int = 0
    span: Optional[Tuple[int, int]] = None
    metadata: Dict = field(default_factory=dict)
    execution_time_ms: float = 0.0

    def to_dict(self):
        return {
            "entity_type": self.entity_type,
            "value": self.value,
            "method_used": self.method_used,
            "confidence": self.confidence,
            "energy_kwh": self.energy_kwh,
            "cascade_level": self.cascade_level,
            "execution_time_ms": self.execution_time_ms,
            "span": self.span,
            "metadata": self.metadata,
        }
