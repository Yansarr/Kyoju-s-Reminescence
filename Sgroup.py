
import pygame as pg

class Sgroup (pg.sprite.Group):

    def __init__(self):
        super().__init__()

    def drawGroup(self, surface, offset_x, offset_y):
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for sprite in self.sprites():
            old_rect = self.spritedict[sprite]
            new_rect = surface_blit(sprite.image, (sprite.rect.x - offset_x, sprite.rect.y - offset_y))
            if old_rect:
                if new_rect.colliderect(old_rect):
                    dirty_append(new_rect.union(old_rect))
                else:
                    dirty_append(new_rect)
                    dirty_append(old_rect)
            else:
                dirty_append(new_rect)
            self.spritedict[sprite] = new_rect
        return dirty
