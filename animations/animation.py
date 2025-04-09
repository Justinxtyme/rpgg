import pygame
class Animation:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, frame_count):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frames = []
        self.current_frame = 0
        self.frame_count = frame_count

        # Slice the sprite sheet into individual frames
        for i in range(frame_count):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = self.sprite_sheet.subsurface(rect)
            self.frames.append(frame)

    def get_current_frame(self):
        # Return the current frame of the animation
        return self.frames[int(self.current_frame)]

    def update(self, dt, animation_speed):
        # Update the animation frame index
        self.current_frame += animation_speed * dt
        if self.current_frame >= self.frame_count:
            self.current_frame = 0  # Loop back to the first frame