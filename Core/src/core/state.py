from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.core.events import Event, EventBus


@dataclass
class AgentState:
    """Represents temporary internal conditions of the agent."""

    valence: float = 0.0
    arousal: float = 0.0
    stress: float = 0.0
    fatigue: float = 0.0
    energy: float = 1.0
    cognitive_load: float = 0.0
    uncertainty: float = 0.0
    confidence: float = 1.0
    social_engagement: float = 0.0
    active_modes: List[str] = field(default_factory=list)


class StateManager:
    """Manages the persistent state of the agent, handling transitions and decay."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.state = AgentState()

    def update_stress(self, delta: float):
        self.state.stress = max(0.0, min(1.0, self.state.stress + delta))

    def handle_emotion_updated(self, event: Event):
        """Updates global state based on active emotions."""
        # Simple placeholder logic: map active emotions to valence/arousal/stress
        active_emotions = event.observations.get("active_emotions", {})

        # Calculate new stress based on anxiety/fear
        stress_contributors = ["anxiety", "fear"]
        new_stress = sum(
            e.intensity
            for name, e in active_emotions.items()
            if name in stress_contributors
        )
        self.state.stress = min(1.0, new_stress)

        # Calculate valence
        # Assuming positive emotions increase valence, negative decrease it
        positive = ["joy", "amusement", "interest"]
        negative = ["anxiety", "fear", "anger", "sadness"]

        pos_val = sum(
            e.intensity for name, e in active_emotions.items() if name in positive
        )
        neg_val = sum(
            e.intensity for name, e in active_emotions.items() if name in negative
        )

        # Map to -1.0 to 1.0
        self.state.valence = max(-1.0, min(1.0, pos_val - neg_val))

        state_event = Event(
            type="STATE_UPDATED",
            source="StateManager",
            observations={"state": self.state},
            correlation_id=event.correlation_id,
        )
        self.event_bus.publish(state_event)

    def get_current_state(self) -> AgentState:
        return self.state


class ContextManager:
    """Maintains situational and contextual awareness."""

    def __init__(self):
        self._context: Dict[str, Any] = {}

    def update_context(self, key: str, value: Any):
        self._context[key] = value

    def get_context(self, key: str) -> Optional[Any]:
        return self._context.get(key)
