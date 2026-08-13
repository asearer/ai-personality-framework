from src.core.events import Event, EventBus


class PromptContextBuilder:
    """Constructs prompt context from internal state and personality parameters."""

    def build(self, motivation, behavior_intent):
        return f"[System: Current motivation is '{motivation}'. Selected behavior intent is '{behavior_intent}'.]"


class LanguageModelProvider:
    """
    Replaceable cognition/language component used by the architecture.
    The LLM is NOT the personality.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.context_builder = PromptContextBuilder()

    def generate_response(self, context, behavior_intent):
        """Mock LLM Generation."""
        if behavior_intent == "defensive_response":
            return "I don't appreciate that tone."
        elif behavior_intent == "seek_information":
            return "Could you tell me more about that?"
        elif behavior_intent == "comfort":
            return "It's going to be okay."
        return "Acknowledged."

    def handle_behavior_selected(self, event: Event):
        """Final step in interaction loop: realizing text."""
        intent = event.observations.get("behavior_intent")
        motivation = event.observations.get("motivation")

        context = self.context_builder.build(motivation, intent)
        response_text = self.generate_response(context, intent)

        output_event = Event(
            type="AGENT_RESPONSE_GENERATED",
            source="LanguageModelProvider",
            observations={"text": response_text},
            correlation_id=event.correlation_id,
        )
        self.event_bus.publish(output_event)
