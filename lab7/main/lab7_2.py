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

MUSIC_FOLDER = "/home/llinn/Desktop/VSC/test/school/lab7/sound"

music_files = [f for f in os.listdir(MUSIC_FOLDER.replace("\\", os.sep).replace("/", os.sep)) if f.endswith(('.mp3', '.wav'))]

if not music_files:
    print("No music files found in the folder!")
    pygame.quit()
    exit()

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

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play_pause()
            elif event.key == pygame.K_RIGHT:
                next_song()
            elif event.key == pygame.K_LEFT:
                previous_song()

    screen.fill(BLACK)

    current_song = music_files[current_song_index]
    text = font.render(f"Playing: {current_song}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()