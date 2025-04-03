import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 25)

snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = "RIGHT"
food_pos = None
food_spawn = False
food_timer = 0
score = 0
level = 1
speed = 10

class Food:
    def __init__(self):
        self.x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        self.y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        self.weight = random.randint(1, 3)
        self.spawn_time = time.time()

    def draw(self):
        pygame.draw.rect(screen, RED, pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))
        weight_text = font.render(str(self.weight), True, WHITE)
        screen.blit(weight_text, (self.x + CELL_SIZE // 4, self.y + CELL_SIZE // 4))

    def is_expired(self):
        return time.time() - self.spawn_time > 5  # Food disappears after 5 seconds


def show_score_and_level():
    score_text = font.render(f"Score: {score}  Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))

def check_collision(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

running = True
food = None

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

    if food and check_collision(new_head, (food.x, food.y)):
        score += food.weight
        food = None
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    if not food or (food and food.is_expired()):
        food = Food()

    screen.fill(WHITE)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    if food:
        food.draw()
    show_score_and_level()

    pygame.display.flip()

    clock.tick(speed)

pygame.quit()