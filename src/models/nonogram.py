from src.models.observer import Observer

class Cell:
    def __init__(self):
        self.observers = []
        self.state = False

    def add_observer(self, observer: Observer):
        if not isinstance(observer, Observer):
            raise TypeError("observer must implement the Observer interface")
        self.observers.append(observer)

    def set_state(self, state):
        self.state = state
        self.notify_observers()

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
            
class ClueBox:
    def __init__(self, cells, clues):
        self.cells = cells
        self.clues = clues

    def calculate_clues(self):
        clues_calculated = []
        count_consecutive = 0
        for cell in self.cells:
            if cell.state:
                count_consecutive += 1
            elif count_consecutive > 0:
                clues_calculated.append(count_consecutive)
                count_consecutive = 0
        if count_consecutive > 0:
            clues_calculated.append(count_consecutive)
        return clues_calculated

class NonogramPuzzle:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = [Cell() for _ in range(rows * columns)]
        self.row_clues = [ClueBox(self.cells[i * columns:(i + 1) * columns], clues=[1]) for i in range(rows)]
        self.column_clues = [ClueBox([self.cells[i] for i in range(j, rows * columns, columns)], clues=[1]) for j in range(columns)]

    def reset(self):
        for cell in self.cells:
            cell.set_state(False)

    def validate_solution(self):
        return all(cluebox.clues == cluebox.calculate_clues() for cluebox in self.row_clues + self.column_clues)
