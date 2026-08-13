from src.core.events import EventBus


class PerceptionManager:
    """Manages sensory inputs and routes them to the event bus."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.providers: list = []

    def register_provider(self, provider):
        self.providers.append(provider)


class ObservationNormalizer:
    """Normalizes raw observations into structured formats."""

    pass
