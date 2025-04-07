import math
from Character-System import Character
# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player = Character(0, 0)
player_sprite = 

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    #uncomment for sprite
    #screen.blit(player_sprite, player.position)
    pygame.draw.circle(screen, "red", player_pos, 40)
    keys = pygame.key.get_pressed()
    x_move = (keys[pygame.K_d] - keys[pygame.K_a])  # Right (1) / Left (-1)
    y_move = (keys[pygame.K_s] - keys[pygame.K_w])  # Down (1) / Up (-1)

    player.move(x_move, y_move, 300, dt)
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
