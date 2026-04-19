from dataclasses import dataclass, field


@dataclass
class ExtractionResult:
    entity_type: str
    value: str | None
    method_used: str
    confidence: float
    energy_kwh: float = 0.0
    cascade_level: int = 0
    span: tuple[int, int] | None = None
    metadata: dict = field(default_factory=dict)
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
