from src.affect.emotion import EmotionEngine
from src.behavior.engine import BehaviorEngine
from src.cognition.appraisal import AppraisalEngine
from src.core.events import Event, EventBus
from src.core.state import StateManager
from src.language.llm import LanguageModelProvider
from src.motivation.engine import MotivationEngine
from src.personality.engine import PersonalityEngine


class CognitiveLoop:
    """
    Orchestrates the fast interaction loop:
    EVENT -> APPRAISAL -> EMOTION UPDATE -> STATE UPDATE -> MOTIVATION -> BEHAVIOR -> LLM
    """

    def __init__(self):
        self.event_bus = EventBus()
        self.state_manager = StateManager(self.event_bus)
        self.personality = PersonalityEngine()

        self.appraisal_engine = AppraisalEngine(self.event_bus)
        self.emotion_engine = EmotionEngine(self.event_bus)
        self.motivation_engine = MotivationEngine(self.event_bus)
        self.behavior_engine = BehaviorEngine(self.event_bus)
        self.llm_provider = LanguageModelProvider(self.event_bus)

        self._wire_events()

    def _wire_events(self):
        # When a raw event like OBSERVATION comes in, we route it to Appraisal
        # For simplicity in this mock, we just appraise any incoming "USER_ACTION"
        self.event_bus.subscribe("USER_ACTION", self._handle_user_action)

        # When Appraisal finishes, EmotionEngine picks it up
        self.event_bus.subscribe(
            "APPRAISAL_COMPLETED", self.emotion_engine.handle_appraisal
        )

        # When Emotion finishes, StateManager updates global state and emits STATE_UPDATED
        self.event_bus.subscribe(
            "EMOTION_UPDATED", self.state_manager.handle_emotion_updated
        )

        # When State updates, MotivationEngine recalculates drives
        self.event_bus.subscribe(
            "STATE_UPDATED", self.motivation_engine.handle_state_updated
        )

        # When Motivation updates, BehaviorEngine selects a response intent
        self.event_bus.subscribe(
            "MOTIVATION_UPDATED", self.behavior_engine.handle_motivation_updated
        )

        # When Behavior selects intent, LLM realizes it into text
        self.event_bus.subscribe(
            "BEHAVIOR_SELECTED", self.llm_provider.handle_behavior_selected
        )

    def _handle_user_action(self, event: Event):
        # Empty context for now
        self.appraisal_engine.appraise(
            event,
            context={},
            state=self.state_manager.get_current_state(),
            personality=self.personality,
        )

    def process_event(self, event: Event):
        """Entry point for incoming world events."""
        self.event_bus.publish(event)
