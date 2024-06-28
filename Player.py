from os import listdir
from os.path import isfile, join
import pygame as pg
import math
import pygame.sprite

def get_sound(name, volume):
    # sound = pg.mixer.music.load(join("assets", "Music", name))
    sound = pygame.mixer.Sound(join("assets", "Music", name))
    sound.set_volume(volume)
    return sound

def flip(sprites):
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
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
            sprites.append(pg.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = flip(sprites)
            all_sprites[image.replace(".png", "") + "_left"] = sprites
        else:
            all_sprites[image.replace(".png", "")] = sprites
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 5
    PLAYER = "Jeremy"
    SPRITES = load_sprite_sheets("MainCharacters", PLAYER, 32, 32, True)
    ANIMATION_DELAY = 8

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_countdown = 0
        self.sprite = None
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.respawn_point_x = 100
        self.respawn_point_y = 800
        self.gravity_reverse_count = 0
        self.onGround = None

    def jump(self):
        if self.onGround:
            if abs(self.GRAVITY) == 5:
                self.y_vel = -self.GRAVITY * 2
            elif abs(self.GRAVITY) == 12:
                self.y_vel = -self.GRAVITY * 0.65
            elif abs(self.GRAVITY) == 1:
                self.y_vel = -self.GRAVITY * 11
            self.animation_count = 0
            self.jump_count += 1
            if self.jump_count == 1:
                self.fall_countdown = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def tp(self, x, y):
        self.rect = pg.Rect(x, y, 50, 50)

    def make_hit(self):
        if self.hit == False:
            death_sound = get_sound("Death_Sound.mp3", 0.05)
            death_sound.play()
        self.hit = True


    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def respawn(self, x, y):
        self.tp(x, y)
        self.hit_count = 0

    def loop(self, fps):

        if -1.5 > self.y_vel > 1.5:
            self.y_vel = 0

        self.y_vel += min(1, (self.fall_countdown / fps) * self.GRAVITY)
        if self.GRAVITY < 0:
            self.y_vel = max(-31, self.y_vel)
        else:
            self.y_vel = min(31, self.y_vel)

        self.move(self.x_vel, self.y_vel)
        self.fall_countdown += 1
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 0.6:
            self.hit = False
            self.hit_count = 0
            self.respawn(self.respawn_point_x, self.respawn_point_y)

        self.update_sprite()

    def update_sprite(self):
        keys = pygame.key.get_pressed()
        sprite_sheet = "idle"

        if keys[pg.K_RIGHT] or keys[pg.K_LEFT]:
            sprite_sheet = "run"
        if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
            sprite_sheet = "idle"

        elif self.hit:
            sprite_sheet = "death"

        # Animation SAUT
        elif self.GRAVITY > 0:
            if self.y_vel < 0:
                self.onGround = False
                if self.jump_count == 1:
                    sprite_sheet = "jump"
            elif self.y_vel > self.GRAVITY * 2:
                sprite_sheet = "fall"
                self.onGround = False
        else:
            if self.y_vel > 0:
                self.onGround = False
                if self.jump_count == 1:
                    sprite_sheet = "jump"
            elif self.y_vel < self.GRAVITY * 2:
                sprite_sheet = "fall"

        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

        # Animation SAUT


        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

    def landed(self):
        self.fall_countdown = 0
        self.y_vel = 0
        self.jump_count = 0
        self.gravity_reverse_count = 0
        self.onGround = True

    def hit_head(self):
        self.y_vel *= -1

    def set_respawn_point(self, x, y):
        self.respawn_point_x = x
        self.respawn_point_y = y
