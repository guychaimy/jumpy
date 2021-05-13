# Pygame template - skelton for a new pygame project
import pygame
import random
from settings import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

all_sprits = pygame.sprite.Group()

# Game loop
running = True
while running:
    # Keep the running at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False



    # update
    all_sprits.update()
    # Drae / render
    screen.fill(BLACK)
    all_sprits.draw(screen)

    # *After* drawing everything, flip the display
    pygame.display.flip()
