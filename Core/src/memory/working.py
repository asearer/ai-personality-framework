from typing import Any, Dict


class WorkingMemory:
    """Short-term operational memory."""

    def __init__(self):
        self.buffer = []

    def store(self, item: Any, context: Dict[str, Any]):
        self.buffer.append({"item": item, "context": context})

    def retrieve(self, query: str):
        pass
