import pygame
from random import randint
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, image_path, loc = None, velocity = 0):
        super().__init__()

        self.type = type
        self.image_path = image_path
        self.source_image = pygame.transform.flip(pygame.image.load(image_path).convert_alpha(), True , False)
        self.velocity = velocity

        self.frames = [
            pygame.transform.scale(self.source_image.subsurface((0, 0, 64, 64)), (96, 96)),
            pygame.transform.scale(self.source_image.subsurface((64, 0, 64, 64)), (96, 96)),
            pygame.transform.scale(self.source_image.subsurface((0, 64, 64, 64)), (96, 96)),
            pygame.transform.scale(self.source_image.subsurface((64, 64, 64, 64)), (96, 96))]
        
        self.masks = []
        for f in self.frames:
            self.masks.append(pygame.mask.from_surface(f))

        self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        self.mask = self.masks[int(self.animation_index)]

        if type == 'air':
            if not loc: loc = (randint(900, 1100), randint(200, 270))
            self.rect = self.image.get_rect(midbottom = loc)
        else:
            if not loc: loc = (randint(900, 1100), GROUND_Y+35)
            self.rect = self.image.get_rect(midbottom = loc)

    def animate(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        self.mask = self.masks[int(self.animation_index)] 

    def update(self):
        self.animate()
        self.rect.x += self.velocity
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()