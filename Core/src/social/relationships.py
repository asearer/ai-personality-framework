from dataclasses import dataclass
from typing import Dict


@dataclass
class Relationship:
    """Persistent object representing relationship with another agent/user."""

    id: str
    familiarity: float = 0.0
    trust: float = 0.0
    affection: float = 0.0
    respect: float = 0.0


class RelationshipEngine:
    """Manages relationship state and updates."""

    def __init__(self):
        self.relationships: Dict[str, Relationship] = {}

    def get_relationship(self, id: str) -> Relationship:
        return self.relationships.get(id, Relationship(id=id))
