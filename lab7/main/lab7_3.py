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
pygame.display.set_caption("Moving Red Ball")


WHITE = (255, 255, 255)
RED = (255, 0, 0)

BALL_RADIUS = 25
ball_x = WIDTH // 2  
ball_y = HEIGHT // 2  
MOVE_DISTANCE = 20

activated = True
while activated:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            activated = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                new_y = ball_y - MOVE_DISTANCE
                if new_y - BALL_RADIUS >= 0:  
                    ball_y = new_y
            elif event.key == pygame.K_DOWN:
                new_y = ball_y + MOVE_DISTANCE
                if new_y + BALL_RADIUS <= HEIGHT:  
                    ball_y = new_y
            elif event.key == pygame.K_LEFT:
                new_x = ball_x - MOVE_DISTANCE
                if new_x - BALL_RADIUS >= 0:  
                    ball_x = new_x
            elif event.key == pygame.K_RIGHT:
                new_x = ball_x + MOVE_DISTANCE
                if new_x + BALL_RADIUS <= WIDTH:  
                    ball_x = new_x

    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

    pygame.display.flip()

pygame.quit()