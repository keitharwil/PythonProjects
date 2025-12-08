# ========================
# File: spritesheet.py
# ========================

import pygame

class SpriteSheet:
    """
    Class used to retrieve images from a sprite sheet.
    """
    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load sprite sheet image: {filename}")
            raise SystemExit(e)

    def get_frame(self, x, y, width, height, scale=1):
        """
        Extracts a frame from the sheet.
        
        :param x: The x-coordinate (in pixels) of the frame's top-left corner on the sheet.
        :param y: The y-coordinate (in pixels) of the frame's top-left corner on the sheet.
        :param width: The width of a single frame.
        :param height: The height of a single frame.
        :param scale: A multiplier to resize the frame after extraction.
        :return: A new pygame.Surface containing the extracted frame, optionally scaled.
        """
        # Create a new, blank Surface with a transparent background
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Define the rectangular area to copy from the sheet
        rect = pygame.Rect(x, y, width, height)
        
        # Blit (copy) the area defined by 'rect' from the sheet onto the new image Surface
        image.blit(self.sheet, (0, 0), rect)
        
        # Scale the image if requested
        if scale != 1:
            image = pygame.transform.scale(image, (width * scale, height * scale))
            
        return image


class Player(pygame.sprite.Sprite):
    """
    Class to handle the player character's animation and movement.
    """
    def __init__(self, x, y, sheet_file, frame_w, frame_h, scale, row_index, num_frames, fps):
        super().__init__()
        
        # --- Constants ---
        self.SPRITE_WIDTH = frame_w
        self.SPRITE_HEIGHT = frame_h
        self.FRAME_RATE = fps

        # --- Load and Extract Frames ---
        self.sprite_sheet = SpriteSheet(sheet_file)
        self.frames = []
        
        # Extract the sequence of frames for the animation from the specified row
        start_y = row_index * self.SPRITE_HEIGHT 

        for frame_index in range(num_frames):
            start_x = frame_index * self.SPRITE_WIDTH
            frame = self.sprite_sheet.get_frame(
                start_x, start_y, 
                self.SPRITE_WIDTH, self.SPRITE_HEIGHT, 
                scale=scale
            )
            self.frames.append(frame)

        # --- Animation and Sprite Variables ---
        self.frame_index = 0
        self.image = self.frames[self.frame_index] # The currently displayed frame
        self.rect = self.image.get_rect(topleft=(x, y)) # The collision rectangle
        self.last_update = pygame.time.get_ticks()

    def update(self):
        """
        Handles the animation cycling based on time.
        """
        now = pygame.time.get_ticks()
        
        # Check if enough time has passed to switch to the next frame
        if now - self.last_update > (1000 / self.FRAME_RATE):
            self.last_update = now
            
            # Increment frame index and wrap around to 0 if we exceed the list size
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            
            # Example movement (optional)
            self.rect.x += 1 # Move the player 1 pixel to the right
            if self.rect.x > 800:
                self.rect.x = -100 # Reset if off-screen