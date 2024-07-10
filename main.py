from map import Map
from helicopter import Helicopter as Helico
from clouds import Clouds
import time
import os
import json
from pynput import keyboard

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
#f - сохранение, g - восстановление
def process_key(key):                                   # обработчик нажатия клавиш
    global helico, tick, clouds, field
    c = key.char.lower()
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helico.move(dx, dy)
    elif (c == 'f'):
        data = {"helicopter":helico.export_data(),
                "clouds": clouds.export_data(),
                "field": field.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    elif (c == 'g'):
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            helico.import_data(data["helicopter"])
            tick = data["tick"] or 1
            field.import_data(data["field"])
            clouds.import_data(data["clouds"])

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key,)
listener.start()


TICK_SLEEP = 0.05           # Частота тиков
TREE_UPDATE = 30            # Как часто вырастают деревья, тиков
CLOUDS_UPDATE = 30          # Обновление облаков, тиков
FIRE_UPDATE = 280           # Обновление огня, тиков
FIRE_COUNT = 42              # Интенсивность огня
MAP_W, MAP_H = 15, 15       # Размер поля
tick = 1

field = Map(MAP_W,MAP_H)
clouds = Clouds(MAP_W,MAP_H)
helico = Helico(MAP_W,MAP_H)

helico.print_stats()
field.process_helicopter(helico, clouds)
field.print_map(helico, clouds)
clouds.update()


while True:
    os.system("clear")
    helico.print_stats()
    field.process_helicopter(helico, clouds)
    field.print_map(helico, clouds)

    #print("TICK", tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        field.update_fires(helico,FIRE_COUNT)
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update(10, 2)