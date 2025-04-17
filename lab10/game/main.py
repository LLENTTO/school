import psycopg2
import pygame
import random
import sys
from datetime import datetime

conn_params = {
    "dbname": "llinn",
    "user": "llinn",
    "password": "llinn",
    "host": "localhost",
    "port": "5432"
}

def connect():
    try:
        conn = psycopg2.connect(**conn_params)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS user_scores (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    score INTEGER NOT NULL,
                    level INTEGER NOT NULL,
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cur.close()
            conn.close()

def get_user(username):
    conn = connect()
    user_id = None
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            if result:
                user_id = result[0]
            else:
                cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
                user_id = cur.fetchone()[0]
                conn.commit()
            return user_id
        except Exception as e:
            print(f"Error with user: {e}")
        finally:
            cur.close()
            conn.close()
    return None

def get_user_level(user_id):
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT level FROM user_scores WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
            result = cur.fetchone()
            return result[0] if result else 1
        except Exception as e:
            print(f"Error fetching level: {e}")
        finally:
            cur.close()
            conn.close()
    return 1

def save_game(user_id, score, level):
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO user_scores (user_id, score, level) VALUES (%s, %s, %s)",
                (user_id, score, level)
            )
            conn.commit()
            print("Game saved successfully.")
        except Exception as e:
            print(f"Error saving game: {e}")
        finally:
            cur.close()
            conn.close()

class SnakeGame:
    def __init__(self, username, user_id):
        pygame.init()
        self.width = 800
        self.height = 600
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.user_id = user_id
        self.username = username
        self.level = get_user_level(user_id)
        self.reset()

    def reset(self):
        self.direction = 'RIGHT'
        self.snake_pos = [400, 300]
        self.snake_body = [[400, 300], [380, 300], [360, 300]]
        self.food_pos = self.spawn_food()
        self.food_spawned = True
        self.score = 0
        self.paused = False
        self.game_over = False
        self.level_settings()

    def level_settings(self):
        if self.level == 1:
            self.speed = 10
            self.walls = []
        elif self.level == 2:
            self.speed = 15
            self.walls = [[200, 200, 200, 20], [600, 400, 200, 20]]
        else:
            self.speed = 20
            self.walls = [[300, 150, 20, 300], [500, 150, 20, 300]]

    def spawn_food(self):
        x = random.randrange(20, self.width - 20, 20)
        y = random.randrange(20, self.height - 20, 20)
        return [x, y]

    def run(self):
        print(f"Welcome, {self.username}! Current Level: {self.level}")
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game(self.user_id, self.score, self.level)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                        if self.paused:
                            save_game(self.user_id, self.score, self.level)
                    if not self.paused:
                        if event.key == pygame.K_UP and self.direction != 'DOWN':
                            self.direction = 'UP'
                        elif event.key == pygame.K_DOWN and self.direction != 'UP':
                            self.direction = 'DOWN'
                        elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                            self.direction = 'LEFT'
                        elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                            self.direction = 'RIGHT'

            if not self.paused:
                if self.direction == 'UP':
                    self.snake_pos[1] -= 20
                elif self.direction == 'DOWN':
                    self.snake_pos[1] += 20
                elif self.direction == 'LEFT':
                    self.snake_pos[0] -= 20
                elif self.direction == 'RIGHT':
                    self.snake_pos[0] += 20

                self.snake_body.insert(0, list(self.snake_pos))
                if self.snake_pos == self.food_pos:
                    self.score += 1
                    self.food_spawned = False
                    if self.score % 5 == 0:
                        self.level += 1
                        self.level_settings()
                else:
                    self.snake_body.pop()

                if not self.food_spawned:
                    self.food_pos = self.spawn_food()
                    self.food_spawned = True

                if (self.snake_pos[0] < 0 or self.snake_pos[0] >= self.width or
                    self.snake_pos[1] < 0 or self.snake_pos[1] >= self.height or
                    self.snake_pos in self.snake_body[1:]):
                    self.game_over = True

                for wall in self.walls:
                    wall_rect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
                    snake_rect = pygame.Rect(self.snake_pos[0], self.snake_pos[1], 20, 20)
                    if snake_rect.colliderect(wall_rect):
                        self.game_over = True

                self.display.fill((0, 0, 0))
                for pos in self.snake_body:
                    pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(pos[0], pos[1], 20, 20))
                pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], 20, 20))
                for wall in self.walls:
                    pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(wall[0], wall[1], wall[2], wall[3]))
                font = pygame.font.SysFont(None, 36)
                score_text = font.render(f'Score: {self.score} Level: {self.level}', True, (255, 255, 255))
                self.display.blit(score_text, (10, 10))
                if self.paused:
                    pause_text = font.render('Paused', True, (255, 255, 255))
                    self.display.blit(pause_text, (self.width // 2 - 50, self.height // 2))
                pygame.display.update()
                self.clock.tick(self.speed)

        save_game(self.user_id, self.score, self.level)
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render(f'Game Over! Score: {self.score}', True, (255, 255, 255))
        self.display.blit(game_over_text, (self.width // 2 - 150, self.height // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()

def main():
    create_tables()
    username = input("Enter your username: ")
    user_id = get_user(username)
    if user_id:
        game = SnakeGame(username, user_id)
        game.run()
    else:
        print("Failed to start game.")

if __name__ == "__main__":
    main()