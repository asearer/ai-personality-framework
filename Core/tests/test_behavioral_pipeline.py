import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.events import Event  # noqa: E402
from src.core.loop import CognitiveLoop  # noqa: E402


class TestBehavioralPipeline(unittest.TestCase):
    def test_end_to_end_threatening_event(self):
        loop = CognitiveLoop()

        # We need to capture the final output event
        final_outputs = []

        def capture_output(event):
            final_outputs.append(event)

        loop.event_bus.subscribe("AGENT_RESPONSE_GENERATED", capture_output)

        # Create a threatening event
        threatening_event = Event(
            type="USER_ACTION",
            source="TestRunner",
            observations={"is_threatening": True},
        )

        # Process through the full pipeline
        loop.process_event(threatening_event)

        # Verify the final output
        self.assertEqual(len(final_outputs), 1)
        final_text = final_outputs[0].observations.get("text")

        # A threat -> fear -> high stress -> self_protection -> defensive_response -> "I don't appreciate that tone."
        self.assertEqual(final_text, "I don't appreciate that tone.")

    def test_end_to_end_rewarding_event(self):
        loop = CognitiveLoop()

        final_outputs = []

        def capture_output(event):
            final_outputs.append(event)

        loop.event_bus.subscribe("AGENT_RESPONSE_GENERATED", capture_output)

        # Create a rewarding event
        rewarding_event = Event(
            type="USER_ACTION", source="TestRunner", observations={"is_rewarding": True}
        )

        loop.process_event(rewarding_event)

        self.assertEqual(len(final_outputs), 1)
        final_text = final_outputs[0].observations.get("text")

        # A reward -> joy -> high valence -> exploration -> seek_information -> "Could you tell me more about that?"
        self.assertEqual(final_text, "Could you tell me more about that?")


if __name__ == "__main__":
    unittest.main()
