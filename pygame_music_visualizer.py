import pygame
import pyaudio
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CHUNK_SIZE = 1024

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Music Visualizer")
clock = pygame.time.Clock()

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

# Main game loop
running = True
frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Read audio data from microphone
    data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)

    # Draw the waveform
    waveform_height = HEIGHT // 4
    for i, sample in enumerate(data):
        x = int(i / CHUNK_SIZE * WIDTH)
        y_pos = int(HEIGHT * 3/4 + sample * waveform_height / 2**15)
        pygame.draw.line(screen, BLUE, (x, HEIGHT * 3/4), (x, y_pos), 1)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

    frame += 1

# Close the stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()

# Quit Pygame
pygame.quit()

