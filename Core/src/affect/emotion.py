from dataclasses import dataclass
from typing import Optional

from src.core.events import Event, EventBus


@dataclass
class Emotion:
    """Represents a specific emotional state."""

    name: str
    intensity: float
    activation: float
    valence: float
    target: Optional[str] = None
    cause: Optional[str] = None
    confidence: float = 1.0
    expression_level: float = 0.0


class EmotionEngine:
    """Manages multiple simultaneous emotional states."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.active_emotions: dict[str, Emotion] = {}

    def trigger_emotion(self, emotion: Emotion):
        self.active_emotions[emotion.name] = emotion

    def handle_appraisal(self, event: Event):
        """Processes an APPRAISAL_COMPLETED event and updates emotions."""
        appraisal = event.observations.get("appraisal")
        if not appraisal:
            return

        emotions_changed = False

        # Map threat to anxiety/fear
        if appraisal.threat > 0.3:
            intensity = min(1.0, appraisal.threat * 1.2)
            self.trigger_emotion(
                Emotion(
                    name="fear", intensity=intensity, activation=intensity, valence=-1.0
                )
            )
            emotions_changed = True

        # Map reward to joy
        if appraisal.reward > 0.3:
            intensity = appraisal.reward
            self.trigger_emotion(
                Emotion(
                    name="joy", intensity=intensity, activation=intensity, valence=1.0
                )
            )
            emotions_changed = True

        if emotions_changed:
            emotion_event = Event(
                type="EMOTION_UPDATED",
                source="EmotionEngine",
                observations={"active_emotions": self.active_emotions},
                correlation_id=event.correlation_id,
            )
            self.event_bus.publish(emotion_event)
