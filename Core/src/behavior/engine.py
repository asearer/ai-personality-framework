from src.core.events import Event, EventBus


class BehaviorEngine:
    """
    Evaluates candidate behaviors based on context, personality, state, and goals.
    Does not allow LLM to independently decide the entire behavioral response.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def select_behavior(
        self, candidates: list, context, state, active_motivation, personality
    ):
        """Placeholder for complex evaluation."""
        if active_motivation == "self_protection":
            return "defensive_response"
        elif active_motivation == "exploration":
            return "seek_information"
        return candidates[0] if candidates else "neutral_response"

    def handle_motivation_updated(self, event: Event):
        """Listens for motivation changes and selects a behavioral intent."""
        active_motivation = event.observations.get("active_motivation")

        candidates = ["agree", "disagree", "comfort", "challenge"]

        # We need the current state, but for simplicity we'll pass None and rely on motivation
        selected_intent = self.select_behavior(
            candidates, {}, None, active_motivation, None
        )

        behavior_event = Event(
            type="BEHAVIOR_SELECTED",
            source="BehaviorEngine",
            observations={
                "behavior_intent": selected_intent,
                "motivation": active_motivation,
            },
            correlation_id=event.correlation_id,
        )
        self.event_bus.publish(behavior_event)
