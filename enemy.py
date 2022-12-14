import pygame
from random import randint
from config import *
from effects import make_dreamy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, image_path, loc = None, velocity = 0):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

        self.type = type
        self.image_path = image_path
        self.source_image = pygame.transform.flip(pygame.image.load(image_path).convert_alpha(), True , False)
        self.velocity = velocity
        self.loc = loc

        self.frames = [
            pygame.transform.scale(self.source_image.subsurface((0, 0, 96, 96)), (96, 96)),
            pygame.transform.scale(self.source_image.subsurface((96, 0, 96, 96)), (96, 96)),
            pygame.transform.scale(self.source_image.subsurface((0, 96, 96, 96)), (96, 96)),
            pygame.transform.scale(self.source_image.subsurface((96, 96, 96, 96)), (96, 96))]
        
        self.masks = []
        for f in self.frames:
            self.masks.append(pygame.mask.from_surface(f))

        self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        self.mask = self.masks[int(self.animation_index)]

        if type == 'air':
            if not loc: self.loc = (randint(900, 1100), randint(220, 290))
            self.rect = self.image.get_rect(midbottom = self.loc)
        else:
            if not loc: self.loc = (randint(900, 1100), GROUND_Y+15)
            self.rect = self.image.get_rect(midbottom = self.loc)

    def animate(self, mouse_pos):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]
        self.mask = self.masks[int(self.animation_index)] 

        if mouse_pos and self.rect.collidepoint(mouse_pos):
            self.image = make_dreamy(self.image, 'purple', 0, 4)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(midbottom = (self.loc[0], self.loc[1]+8))

    def update(self, mouse_pos = None):
        self.rect.x += self.velocity
        self.animate(mouse_pos)
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()