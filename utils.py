from random import randint as rand

def randbool(r):                            # Метод для определения вероятности какого-либо события (от 0 до 100%)
    t = rand(0, 100)
    return (t <= r)

def randcell(w, h):                         # Возвращает случайную координату на карте
    rw = rand(0, w - 1)
    rh = rand(0, h - 1)
    return (rw, rh)
       
def randcell2(x, y):                        # Метод выбирает случайную соседнюю клетку. 0 - наверх, 1 - направо, 2 - вниз, 3 - налево    
    t = rand(0,3)
    moves = [(-1,0), (0,1), (1,0), (0,-1)]
    dx, dy = moves[t][0], moves[t][1]
    return (x + dx, y + dy)