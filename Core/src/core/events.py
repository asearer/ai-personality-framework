import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class EventState(Enum):
    START = "START"
    UPDATE = "UPDATE"
    CONTINUE = "CONTINUE"
    END = "END"
    POINT = "POINT"


@dataclass
class Event:
    """Universal Event Schema as defined in the architectural prompt."""

    type: str
    source: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    subject: Optional[str] = None
    target: Optional[str] = None
    observations: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    salience: float = 1.0
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    lifecycle: EventState = EventState.POINT
    correlation_id: Optional[str] = None


class EventBus:
    """Universal event bus for source-agnostic events."""

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: str, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event: Event):
        if event.type in self._subscribers:
            for callback in self._subscribers[event.type]:
                callback(event)


class EventStore:
    """Persistent storage for events."""

    def __init__(self):
        self._events = []

    def save(self, event: Event):
        self._events.append(event)

    def get_all(self) -> List[Event]:
        return self._events
