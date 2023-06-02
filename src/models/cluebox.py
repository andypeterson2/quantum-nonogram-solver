from src.models.cell import Cell
class ClueBox:
    def __str__(self):
        return self.clues
    
    def __repr__(self):
        return f'{self.clues}, {self.cells}'
    
    def __init__(self, cells : [Cell], clues: [int]):
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
        
        if not clues_calculated:
            clues_calculated.append(0)
        
        return clues_calculated
    
    
