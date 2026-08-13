from dataclasses import dataclass


@dataclass
class Trait:
    """Structured dimensional data for a trait/facet."""

    id: str
    name: str
    baseline: float
    min: float = 0.0
    max: float = 1.0
    stability: float = 0.8
    plasticity: float = 0.2
    context_sensitivity: float = 0.5
    expression_strength: float = 1.0
