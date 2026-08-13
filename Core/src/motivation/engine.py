from src.core.events import Event, EventBus


class MotivationEngine:
    """
    Supports multiple simultaneous drives (curiosity, affiliation, autonomy, etc).
    Handles conflicts between motivations.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.active_drives: dict[str, str] = {}

    def evaluate_drives(self, state, correlation_id: str):
        """Evaluates current state and emits active motivations."""
        active_motivation = "affiliation"  # Default baseline motivation

        # If stress is high, motivation shifts to self-protection
        if state.stress > 0.5:
            active_motivation = "self_protection"

        # If valence is highly positive, motivation might be exploration/play
        if state.valence > 0.5:
            active_motivation = "exploration"

        self.active_drives["primary"] = active_motivation

        motivation_event = Event(
            type="MOTIVATION_UPDATED",
            source="MotivationEngine",
            observations={"active_motivation": active_motivation},
            correlation_id=correlation_id,
        )
        self.event_bus.publish(motivation_event)

    def handle_state_updated(self, event: Event):
        """Triggered when StateManager finishes updating global state."""
        state = event.observations.get("state")
        if state:
            self.evaluate_drives(state, event.correlation_id or "")
