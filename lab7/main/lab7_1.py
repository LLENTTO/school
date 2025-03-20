import pygame as pg
import time

pg.init()

screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("Mickey Clock")
running = True

clock_img = pg.image.load("/home/llinn/Desktop/VSC/test/school/lab7/assets/clock.png")
minute_hand_img = pg.image.load("/home/llinn/Desktop/VSC/test/school/lab7/assets/rightarm.png")
second_hand_img = pg.image.load("/home/llinn/Desktop/VSC/test/school/lab7/assets/leftarm.png")

clock_center = (640, 360)  

def rotate_image(image, angle, position):
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=position)
    return rotated_image, new_rect

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    curr_time = time.localtime()
    minutes = curr_time.tm_min
    seconds = curr_time.tm_sec

    minute_angle = -6 * minutes  
    second_angle = -6 * seconds  

    screen.fill("white")

    screen.blit(clock_img, (-40,-180))  

    rotated_minute_hand, minute_hand_rect = rotate_image(minute_hand_img, minute_angle, clock_center)
    screen.blit(rotated_minute_hand, minute_hand_rect)

    rotated_second_hand, second_hand_rect = rotate_image(second_hand_img, second_angle, clock_center)
    screen.blit(rotated_second_hand, second_hand_rect)

    pg.display.flip()

pg.quit()