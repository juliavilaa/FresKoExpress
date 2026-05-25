class EventBus:
    """
    Observer Pattern Implementation.
    Allows services to communicate asynchronously without tight coupling.
    """
    def __init__(self):
        self.subscribers = []

    def subscribe(self, listener):
        self.subscribers.append(listener)

    def publish(self, event_name: str, payload: dict):
        print(f"[EVENT BUS] Publishing event: {event_name} | Payload: {payload}")
        for listener in self.subscribers:
            listener(event_name, payload)