import os
import sys
import unittest

# Add the Core directory to the Python path so it can find the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.events import Event, EventBus  # noqa: E402


class TestEventBus(unittest.TestCase):
    def test_event_publish_subscribe(self):
        bus = EventBus()
        received_events = []

        def handler(event):
            received_events.append(event)

        bus.subscribe("USER_MESSAGE_RECEIVED", handler)

        event = Event(type="USER_MESSAGE_RECEIVED", source="text_provider")
        bus.publish(event)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0].type, "USER_MESSAGE_RECEIVED")
        self.assertEqual(received_events[0].source, "text_provider")


if __name__ == "__main__":
    unittest.main()
