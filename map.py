from utils import randbool
from utils import randcell
from utils import randcell2
from random import randint as rand
import os

# 0 - поле 🟩 1 - дерево 🌳 2 - река 🌊 3 - госпиталь 🏥 4 - апгрейд 🏫 5 - огонь 🔥
#💭 🌌 🚁 🪣 🌟 ❤️‍🔥

CELL_TYPES = "🟩🌳🌊🏥💫🔥"   # Список с иконками первого слоя карты
TREE_BONUS = 100            # Бонус очков за тушение огня
TREE_COST = 50              # Стоимость сгоревшего дерева, минус к очкам
UPGRADE_COST = 5000         # Стоимость апгрейда емкости воды
LIFE_COST = 1000            # Стоимость повышения количества жизней
LIVES_GAIN = 50             # Сколько жизней прибавляется за 1 тик, когда мы в госпитале
LIVES_MAX = 200             # Максимальное количество жизней

class Map(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(40)
        self.generate_river(100)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):                           # Метод проверка на то, принадлежит ли определенная клетка с координатами нашему полю.
        if (x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True
    
    def print_map(self, helico, clouds):                    # Печать карты, облаков и деревьев
        print('🟫' * (self.w + 2))
        for ri in range(self.h):
            print('🟫',end='')
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (clouds.cells[ri][ci] == 1):
                    print('💭',end='')
                elif (clouds.cells[ri][ci] == 2):
                    print('⚡',end='')
                    if(self.cells[ri][ci] == 1):                # Если на месте молнии стоит дерево, оно загорается (помещаем в ячейку огонь 5)
                        self.cells[ri][ci] = 5
                elif (helico.x == ri and helico.y == ci):
                    print('🚁',end='')
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell],end='')
            print('🟫')
        print('🟫' * (self.w + 2))

    def generate_river(self, l):                                # Функция для генерации рек
        while True:
            rc = randcell(self.w, self.h)
            rx, ry = rc[0], rc[1]
            if self.check_bounds(rx, ry):
                self.cells[rx][ry] = 2
                break
        while l > 0:
            while True:
                rc2 = randcell2(rx, ry)
                rx2, ry2 = rc2[0], rc2[1]
                if self.check_bounds(rx2, ry2):
                    self.cells[rx2][ry2] = 2
                    rx, ry = rx2, ry2
                    l -= 1
                    break

    def generate_forest(self, r):                               # Функция для генерации леса
        for i in range(self.h):
            for j in range(self.w):
                if randbool(r):
                    self.cells[i][j] = 1

    def generate_tree(self):                                    # Функция для вырастания деревьев
        tries = 0
        while tries <= 50:
            tries += 1
            c = randcell(self.w, self.h)
            cx, cy = c[0], c[1]
            if (self.check_bounds(cx, cy) and self.cells[cx][cy] == 0):
                self.cells[cx][cy] = 1
                break

    def generate_upgrade_shop(self):                            # Функция для генерации магазина улучшений
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 4
    
    def generate_hospital(self):                                # Функция для генерации госпиталя
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if(self.cells[cx][cy] != 4):
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()

    def add_fire(self, count = 1, x = -1, y = -1):  # Функция для добавления огня в клетку
        if ((x == -1) and (y == -1)):               # В нее можно передать координаты, куда добавлять огонь. Если они не переданы, то генерируется случайно
            c = randcell(self.w, self.h)
            cx, cy = c[0], c[1]
        else:
            cx, cy = x, y
        if (self.check_bounds(cx, cy) and self.cells[cx][cy] == 1):
            self.cells[cx][cy] = 5
        count -= 1
        if (count > 0):
            self.add_fire(count)

    def update_fires(self, helico, fire_power = 4): # Функция механики сгорания и загорания деревьев
        for i in range(self.h):
            for j in range(self.w):
                cell = self.cells[i][j]
                if cell == 5:
                    if (rand(0, 1) == 1):           # Дерево тухнет не всегда, шанс 50%
                        self.cells[i][j] = 0
                        if (helico.score - TREE_COST >= 0):
                            helico.score -= TREE_COST
                        else:
                            helico.score = 0                           
                    for k in range (fire_power):    # Генерируем распространение огня рядом. Метод генерирует огонь рядом с горящим деревом, а не случайно
                        rc2 = randcell2(i, j)
                        rx2, ry2 = rc2[0], rc2[1]
                        if self.check_bounds(rx2, ry2):
                            self.add_fire(1, rx2, ry2)

    def process_helicopter(self, helico, clouds):   # Функция управляет переменными вертолета
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if (c == 2):
            helico.tank = helico.mxtank
        if ((c == 5) and (helico.tank > 0)):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1
        if ((c == 4) and (helico.score > UPGRADE_COST)):
            helico.mxtank += 1
            helico.score -= UPGRADE_COST
        if ((c == 3) and (helico.score > LIFE_COST) and (helico.lives < LIVES_MAX)):
            if (helico.lives + LIVES_GAIN <= LIVES_MAX):
                helico.lives += LIVES_GAIN
            else:
                helico.lives = LIVES_MAX
            helico.score -= LIFE_COST
        if (d == 2):
            helico.lives -= 1
            if(helico.lives == 0):
                os.system("clear")
                print(f"GAME OVER! SCORE: {helico.score}")
                exit(0)

    def export_data(self):                          # Экспорт
        return {"cells": self.cells}
    
    def import_data(self, data):                    # Импорт
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]