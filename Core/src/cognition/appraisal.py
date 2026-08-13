from dataclasses import dataclass

from src.core.events import Event, EventBus


@dataclass
class AppraisalResult:
    novelty: float = 0.0
    goal_relevance: float = 0.0
    threat: float = 0.0
    reward: float = 0.0
    certainty: float = 1.0


class AppraisalEngine:
    """
    Evaluates events to produce emotion, motivation, and behavior.
    Considers goal relevance, novelty, controllability, threat, etc.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def appraise(self, event, context, state, personality):
        """Appraises an incoming event and emits an APPRAISAL_COMPLETED event."""
        # Dummy logic: look at observations to determine threat or reward
        obs = event.observations

        result = AppraisalResult()

        # Example: A threatening observation
        if obs.get("is_threatening", False):
            # A neurotic personality might appraise threat higher
            neuroticism = (
                personality.get_baseline_trait("neuroticism") if personality else 0.5
            )
            result.threat = min(1.0, 0.5 + (neuroticism * 0.5))
            result.goal_relevance = 0.8

        if obs.get("is_rewarding", False):
            result.reward = 0.8
            result.goal_relevance = 0.9

        # Emit the result
        appraisal_event = Event(
            type="APPRAISAL_COMPLETED",
            source="AppraisalEngine",
            observations={"appraisal": result},
            correlation_id=event.id,
        )
        self.event_bus.publish(appraisal_event)

        return result
