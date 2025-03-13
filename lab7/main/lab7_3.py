""""
Draw circle - a red ball of size 50 x 50 (radius = 25) on white background. 
 When user presses Up, Down, Left, Right arrow keys on keyboard, the ball should move by 20 pixels in the direction of pressed key.
 The ball should not leave the screen, i.e. user input that leads the
 ball to leave of the screen should be ignored
"""""

import pygame

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255,255,255)

activated = True

while activated: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            activated = False

    screen.fill(WHITE)

    pygame.display.flip()


pygame.quit()