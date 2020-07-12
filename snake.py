import pyglet
from pyglet.window import key
from pathlib import Path

STRANA_CTVERCE = 64
ROZMER_POLE = 10
VELIKOST_OKNA = STRANA_CTVERCE*ROZMER_POLE


souradnice = [(0, 0), (1, 0), (2, 0)]
seznam_jidel = [(2,3)]
smer = [(0, 1)]
window = pyglet.window.Window(width=VELIKOST_OKNA, height=VELIKOST_OKNA)

TILES_DIRECTORY = Path('snake-tiles')

snake_tiles = dict()

for image in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[image.stem] = pyglet.image.load(image)

print(snake_tiles)

obrazek = pyglet.image.load('obrazek.png')
jablko = pyglet.image.load('apple.png')
had = pyglet.sprite.Sprite(snake_tiles['top-left'])
jidlo = pyglet.sprite.Sprite(jablko)

def nazev_casti (souradnice, pozice):
    # # hlava hada
    if pozice == len(souradnice) - 1:
        smer_x = souradnice[pozice][0] - souradnice[pozice-1][0]
        smer_y = souradnice[pozice][1] - souradnice[pozice-1][1]
        smer_tile = smer_pohybu (smer_x, smer_y)
        return smer_tile + '-head'

    if pozice == 0:
        # ocas hada
        smer_x = souradnice[pozice][0] - souradnice[pozice+1][0]
        smer_y = souradnice[pozice][1] - souradnice[pozice+1][1]
        smer_tile = smer_pohybu (smer_x, smer_y)
        return  'tail-'  + smer_tile
    # TODO telo hada
    smer_x_previous = souradnice[pozice][0] - souradnice[pozice-1][0]
    smer_y_previous = souradnice[pozice][1] - souradnice[pozice-1][1]
    smer_x_next = souradnice[pozice][0] - souradnice[pozice+1][0]
    smer_y_next = souradnice[pozice][1] - souradnice[pozice+1][1]
    smer_tile_next = smer_pohybu (smer_x_next, smer_y_next)
    smer_tile_previous = smer_pohybu(smer_x_previous, smer_y_previous)
    return smer_tile_previous + '-' + smer_tile_next

def smer_pohybu (smer_x, smer_y):
    if smer_x == 1:
        return 'left'
    if smer_x == -1:
        return 'right'
    if smer_y == 1:
        return 'bottom'
    if smer_y == -1:
        return 'top'   

def vykresli():
    window.clear()

    for i in range(len(souradnice)):
        x = souradnice[i][0]
        y = souradnice[i][1]
        nazev = nazev_casti(souradnice, i)
        obrazek = pyglet.sprite.Sprite(snake_tiles[nazev])
        obrazek.x = x*STRANA_CTVERCE
        obrazek.y = y*STRANA_CTVERCE
        obrazek.draw() 

    for x, y in seznam_jidel:
        jidlo.x = x*STRANA_CTVERCE
        jidlo.y = y*STRANA_CTVERCE
        jidlo.draw()

def stisk_klavesy(symbol, modifikatory):
    if symbol == key.LEFT:
        smer.pop()
        smer.append((-1, 0))
    if symbol == key.RIGHT:
        smer.pop()
        smer.append((1, 0))
    if symbol == key.UP:
        smer.pop()
        smer.append((0, 1))
    if symbol == key.DOWN:
        smer.pop()
        smer.append((0, -1))

def vytvor_jidlo(souradnice, jidlo):
    from random import randrange

    while True:
        nove_jidlo = (randrange(0,10), randrange(0,10))
        if nove_jidlo not in jidlo and nove_jidlo not in souradnice:
            break
    jidlo.append(nove_jidlo)

def pohyb(t):
    x = souradnice[-1][0] + smer[0][0]
    y = souradnice[-1][1] + smer[0][1]
    nove_pole = (x, y)    
    if nove_pole in souradnice or x == ROZMER_POLE or x < 0 or y == ROZMER_POLE or y < 0:
        raise ValueError('Game over')
    souradnice.append(nove_pole)
    if nove_pole in seznam_jidel:
        seznam_jidel.remove(nove_pole)
    else:
        del souradnice [0]

    if len(seznam_jidel) == 0:
        vytvor_jidlo(souradnice, seznam_jidel)

pyglet.clock.schedule_interval(pohyb, 1/2)

window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
)

pyglet.app.run()
print('Hotovo!')



