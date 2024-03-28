

class WebsocketNotifier:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer: callable):
        self._observers.append(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer(message)


websocket_notifier = WebsocketNotifier()
