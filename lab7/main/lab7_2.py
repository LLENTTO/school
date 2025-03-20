"""""
2. Create music player with keyboard controller. You have to be
 able to press keyboard: play, stop, next and previous as some keys. 
 Player has to react to the given command appropriately.
 
 """

import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player with Buttons")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)

MUSIC_FOLDER = "./sound"
music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(('.mp3', '.wav'))]

if not music_files:
    print("No music files found in the folder!")
    pygame.quit()
    exit()

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

def play_pause():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
    else:
        pygame.mixer.music.unpause()
        is_playing = True

def previous_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(music_files)
    play_song(current_song_index)

def next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(music_files)
    play_song(current_song_index)

def play_song(index):
    global is_playing
    song_path = os.path.join(MUSIC_FOLDER, music_files[index])
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    is_playing = True

current_song_index = 0
is_playing = False
play_song(current_song_index)

buttons = [
    Button(300, 400, 100, 50, "Play/Pause", GRAY, GREEN, play_pause),
    Button(200, 400, 80, 50, "Prev", GRAY, RED, previous_song),
    Button(420, 400, 80, 50, "Next", GRAY, RED, next_song)
]

clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    for button in buttons:
        button.check_hover(mouse_pos)

    screen.fill(BLACK)

    current_song = music_files[current_song_index]
    text = font.render(f"Playing: {current_song}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()