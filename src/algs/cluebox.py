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
