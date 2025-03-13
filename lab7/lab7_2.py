import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

MUSIC_FOLDER = "/home/llinn/Desktop/VSC/test/school/lab7/sound"  
music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(('.mp3', '.wav'))]

if not music_files:
    print("No music files found in the folder!")
    pygame.quit()
    exit()

current_song_index = 0
is_playing = False

def play_song(index):
    global is_playing
    song_path = os.path.join(MUSIC_FOLDER, music_files[index])
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    is_playing = True

play_song(current_song_index)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_playing:
                    pygame.mixer.music.pause()
                    is_playing = False
                else:
                    pygame.mixer.music.unpause()
                    is_playing = True
            elif event.key == pygame.K_LEFT:
                current_song_index = (current_song_index - 1) % len(music_files)
                play_song(current_song_index)
            elif event.key == pygame.K_RIGHT:
                current_song_index = (current_song_index + 1) % len(music_files)
                play_song(current_song_index)

    screen.fill(BLACK)

    current_song = music_files[current_song_index]
    text = font.render(f"Playing: {current_song}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()