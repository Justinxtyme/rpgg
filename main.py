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
Gandalf = Character(0, 0)
gandalf_sprite = pygame.image.load("~/home/slapper/project/gitrg/gadalf.png").convert_alpha()
# Scale sprite based on screen size
def scale_sprite(sprite, screen_width, screen_height, scale_factor=0.1):
    scaled_width = int(screen_width * scale_factor)  # Scale by fraction of screen width
    scaled_height = int(screen_height * scale_factor)  # Scale by fraction of screen height
    return pygame.transform.scale(sprite, (scaled_width, scaled_height))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
        # Scale sprite dynamically
    scaled_sprite = scale_sprite(gandalf_sprite, screen.get_width(), screen.get_height())
    #uncomment for sprite
    screen.blit(scaled_sprite, (int(gandalf.position.x), int(gandalf.position.y)))
    
    # uncomment ball for testing purposes
    #pygame.draw.circle(screen, "red", player_pos, 40)
    keys = pygame.key.get_pressed()
    x_move = (keys[pygame.K_d] - keys[pygame.K_a])  # Right (1) / Left (-1)
    y_move = (keys[pygame.K_s] - keys[pygame.K_w])  # Down (1) / Up (-1)

    gandalf.move(x_move, y_move, 300, dt)
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
