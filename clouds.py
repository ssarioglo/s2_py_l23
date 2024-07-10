from utils import randbool

class Clouds:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.cells = [[0 for i in range(w)] for j in range(h)]
    
    def update(self, r = 10, g = 3):               # Метод обновляет положение облаков
        for i in range (self.h):
            for j in range (self.w):
                if (j >= 0) and (j < (self.w - 1)):
                    self.cells[i][j] = self.cells[i][j + 1]
                elif (j == (self.w - 1)):
                    if randbool(r):
                        self.cells[i][j] = 1
                    else:
                        self.cells[i][j] = 0

        for i in range (self.h):
            for j in range (self.w):
                if (self.cells[i][j] == 1):
                    if randbool(g):
                        self.cells[i][j] = 2
                elif (self.cells[i][j] == 2):
                    self.cells[i][j] = 1


    def export_data(self):                          # Экспорт
        return {"cells": self.cells}
    
    def import_data(self, data):                    # Импорт
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]