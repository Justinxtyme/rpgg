import pygame
from animations.animation import Animation
from char_system.char import Character  # Make sure your module name matches your file/folder structure

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Create your character instance (Gandalf) from your character module.
gandalf = Character(0, 0)  # Assuming the Character class sets up a position attribute (e.g., via a pygame.Vector2)

# Create animations.
# Replace "assets/idle_sprite_sheet.png" and "assets/walking_sprite_sheet.png" with your actual asset paths.
idle_animation = Animation("assets/mage_idle.png", 128, 128, 8)
walking_animation = Animation("assets/mage_walk.png", 128, 128, 6)

# Set the initial animation (idle) and animation speed
current_animation = idle_animation
animation_speed = 10  # This controls how fast the animation plays (frames per second equivalent)

running = True
dt = 0

while running:
    dt = clock.tick(60) / 1000  # Delta time for consistent timing

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states for movement (using WASD keys)
    keys = pygame.key.get_pressed()
    x_move = keys[pygame.K_d] - keys[pygame.K_a]  # Moves right (positive) or left (negative)
    y_move = keys[pygame.K_s] - keys[pygame.K_w]  # Moves down (positive) or up (negative)

    # Update Gandalf's position.
    # Assume that the move() method updates gandalf.position based on x_move, y_move, speed, and dt.
    gandalf.move(x_move, y_move, 300, dt)

    # Select the appropriate animation based on movement.
    if x_move != 0 or y_move != 0:
        current_animation = walking_animation
    else:
        current_animation = idle_animation

    # Update the animation (this cycles through frames based on dt and animation_speed)
    current_animation.update(dt, animation_speed)

    # Render: clear the screen first.
    screen.fill("purple")

    # Blit the current animation frame at the character's position.
    # Here we assume that gandalf.position is a vector (or has x and y attributes).
    current_frame = current_animation.get_current_frame()
    screen.blit(current_frame, (int(gandalf.position.x), int(gandalf.position.y)))
    
    # Update the display
    pygame.display.flip()

pygame.quit()
