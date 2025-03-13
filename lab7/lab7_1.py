import pygame as pg
import time

curr = time.time()

print(time.strftime("%H:%M:%S", time.localtime(curr)))

pg.init()
screen = pg.display.set_mode((1280, 720))
running = True

clock_img = pg.image.load("assets/clock.png")

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("white")

    pg.display.flip()
    screen.blit(clock_img, (500, 500))


pg.quit()