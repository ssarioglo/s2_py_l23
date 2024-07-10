from utils import randcell

class Helicopter:
    def __init__(self, w, h):
        rc = randcell(w, h)
        self.x, self.y = rc[0], rc[1]
        self.h, self.w = h, w
        self.tank = 0
        self.mxtank = 1
        self.score = 0
        self.lives = 100



    def move(self, dx, dy):
        nx, ny = dx + self.x, dy + self.y
        if (nx >= 0 and ny >= 0 and nx < self.h and ny < self.w):
            self.x, self.y = nx, ny

    def print_stats(self):                  # Выводит показатели вертолета
        print(f"🪣: {self.tank}/{self.mxtank} | 🌟: {self.score} | 🤍: {self.lives}")

    def export_data(self):                  # Экспорт
        return {"score": self.score,
                "lives": self.lives,
                "x": self.x, "y": self.y,
                "tank": self.tank, "mxtank": self.mxtank}
    
    def import_data(self, data):            # Импорт
        self.x = data["x"] or 0
        self.y = data["y"] or 0
        self.tank = data["tank"] or 0
        self.mxtank = data["mxtank"] or 1
        self.lives = data["lives"] or 3
        self.score = data["score"] or 0