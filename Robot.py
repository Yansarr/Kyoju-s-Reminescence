from os import listdir
from os.path import isfile, join
import pygame as pg
import math
import pygame.sprite

def flip(sprites):
    return [pg.transform.flip(sprite, False, True) for sprite in sprites]

def load_robot_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pg.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pg.Surface((width, height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pg.transform.scale(surface,(48,48)))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = flip(sprites)
            all_sprites[image.replace(".png", "") + "_left"] = sprites
        else:
            all_sprites[image.replace(".png", "")] = sprites
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

class Robot(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    ROBOT = "Kyoju"
    SPRITE = load_robot_sprite_sheets("MainCharacters", ROBOT, 32, 32)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.direction = "left"
        self.sprite = None
        self.dest_X = 0
        self.dest_Y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.player_distance_X = 0
        self.player_distance_Y = 0
        self.nombrePowerUp = 0


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def loop(self, player):
        self.update_sprite(player)
        self.move(self.x_vel, self.y_vel)

    def set_nombre_powerUp(self, nombre):
        self.nombrePowerUp = nombre
    def update_sprite(self, player):

        sprite_sheet_name = ""

        if player.GRAVITY == 1 or player.GRAVITY == -1:  # Low gravity
            sprite_sheet_name = "Robot_LG"
        elif player.GRAVITY == 5 or player.GRAVITY == -5:  # Normal gravity
            sprite_sheet_name = "Robot_smile"
        elif player.GRAVITY == 12 or player.GRAVITY == -12:  # High gravity
            sprite_sheet_name = "Robot_HG"

        if self.nombrePowerUp == 0:
            sprite_sheet_name = "Robot_bug"
        elif self.nombrePowerUp == 1:
            sprite_sheet_name += ""
        elif self.nombrePowerUp == 2:  # à 1 on a pas besoin de rajouter
            sprite_sheet_name += "_bras"
        else:
            sprite_sheet_name += "_antenne"

        sprites = self.SPRITE[sprite_sheet_name]
        sprite_index = 0
        self.sprite = sprites[sprite_index]

        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

















