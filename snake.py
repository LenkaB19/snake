import pyglet
from pyglet.window import key

STRANA_CTVERCE = 64
ROZMER_POLE = 10
VELIKOST_OKNA = STRANA_CTVERCE*ROZMER_POLE


souradnice = [(0, 0), (1, 0), (2, 0)]
seznam_jidel = [(2,3)]
smer = [(0, 1)]
window = pyglet.window.Window(width=VELIKOST_OKNA, height=VELIKOST_OKNA)

obrazek = pyglet.image.load('obrazek.png')
jablko = pyglet.image.load('apple.png')
had = pyglet.sprite.Sprite(obrazek)
jidlo = pyglet.sprite.Sprite(jablko)

def vykresli():
    window.clear()

    for x, y in souradnice:
        had.x = x*STRANA_CTVERCE
        had.y = y*STRANA_CTVERCE
        had.draw()

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



