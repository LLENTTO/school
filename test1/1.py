# add three background image to the snake game
# backgrounds should swap when the snake increases its speed
# add a sound that denotes that the background has changes



""""
REQS:

3 backgrounds = color?
if speed +=1 >> background = new background
SFX when def speedchange activates


FILES:

SFX: crash.wav => same dir?
BACKGROUD: => RGB?

"""

import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

actual_white = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


background1 = pygame.image.load("bg1.png")
background2 =pygame.image.load("bg2.png")


saclebg1 = pygame.transform.scale(background1,(800,600))
saclebg2 = pygame.transform.scale(background2, (800,600))

threshold =(background1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 25)

snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = "RIGHT"
food_pos = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
food_spawn = True
score = 0
level = 1
speed = 10

def show_score_and_level():
    score_text = font.render(f"Score: {score}  Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))

def check_collision(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

def generate_food():
    while True:
        pos = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
               random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        if pos not in snake:
            return pos


if score % 2 == 0 and score != 0:  
    level += 1
    speed += 2


counter = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != "DOWN":
        snake_dir = "UP"
    if keys[pygame.K_DOWN] and snake_dir != "UP":
        snake_dir = "DOWN"
    if keys[pygame.K_LEFT] and snake_dir != "RIGHT":
        snake_dir = "LEFT"
    if keys[pygame.K_RIGHT] and snake_dir != "LEFT":
        snake_dir = "RIGHT"

    head_x, head_y = snake[0]
    if snake_dir == "UP":
        head_y -= CELL_SIZE
    if snake_dir == "DOWN":
        head_y += CELL_SIZE
    if snake_dir == "LEFT":
        head_x -= CELL_SIZE
    if snake_dir == "RIGHT":
        head_x += CELL_SIZE
    new_head = (head_x, head_y)

    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        print("Game Over! You hit the wall.")
        running = False

    if new_head in snake:
        print("Game Over! You collided with yourself.")
        running = False

    snake.insert(0, new_head)

    if check_collision(new_head, food_pos):
        score += 1
        food_spawn = False
        if score % 4 == 0:  
            level += 1
            speed += 2
            pygame.mixer.Sound('crash.wav').play()
            counter +=1
            if counter % 2 != 0:
                threshold = saclebg1
            else:
                threshold = saclebg2
            print(threshold)
            
    else:
        snake.pop()  
    if not food_spawn:
        food_pos = generate_food()
        food_spawn = True

    screen.blit(threshold,(0,0))


    #screen.fill(threshold)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
    show_score_and_level()


    pygame.display.flip()

    clock.tick(speed)

pygame.quit()