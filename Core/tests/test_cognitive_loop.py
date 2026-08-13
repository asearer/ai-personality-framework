import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.events import Event  # noqa: E402
from src.core.loop import CognitiveLoop  # noqa: E402


class TestCognitiveLoop(unittest.TestCase):
    def test_threatening_event_pipeline(self):
        loop = CognitiveLoop()

        # Initial state checks
        initial_state = loop.state_manager.get_current_state()
        self.assertEqual(initial_state.stress, 0.0)
        self.assertEqual(initial_state.valence, 0.0)

        # Create a threatening event
        threatening_event = Event(
            type="USER_ACTION",
            source="TestRunner",
            observations={"is_threatening": True},
        )

        # Process through the loop
        loop.process_event(threatening_event)

        # Verify the cascading updates

        # 1. Appraisal should have happened (EmotionEngine should have 'fear')
        self.assertIn("fear", loop.emotion_engine.active_emotions)

        # 2. StateManager should have handled EMOTION_UPDATED and increased stress
        final_state = loop.state_manager.get_current_state()
        self.assertGreater(final_state.stress, 0.0)
        self.assertLess(final_state.valence, 0.0)  # Fear reduces valence to negative

    def test_rewarding_event_pipeline(self):
        loop = CognitiveLoop()

        reward_event = Event(
            type="USER_ACTION", source="TestRunner", observations={"is_rewarding": True}
        )

        loop.process_event(reward_event)

        self.assertIn("joy", loop.emotion_engine.active_emotions)
        final_state = loop.state_manager.get_current_state()
        self.assertGreater(final_state.valence, 0.0)  # Joy increases valence


if __name__ == "__main__":
    unittest.main()
