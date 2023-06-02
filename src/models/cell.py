from src.models.observer import Observer

class Cell:
    def __init__(self, state = False):
        self.id = None
        self.observers = []
        self.state = state
        
    def add_observer(self, observer: Observer):
        if not isinstance(observer, Observer):
            raise TypeError("observer must implement the Observer interface")
        self.observers.append(observer)

    def set_state(self, state):
        self.state = state
        self.notify_observers()
        
    def flip(self):
        self.state = not self.state
        self.notify_observers()

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
            
    def __str__(self):
        return str(self.state)
            