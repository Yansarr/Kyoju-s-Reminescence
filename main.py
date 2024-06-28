import pygame as pg
from os.path import join, isfile
import math
import pygame.event
import pytmx
from Tile import Tile
from Sgroup import Sgroup

pg.init()
pg.display.set_caption("Beep Boop")
WIDTH, HEIGHT = 1024, 768
window = pg.display.set_mode((WIDTH, HEIGHT))

from Player import Player
from Player import load_sprite_sheets
from Player import get_sound
from Robot import Robot
from Robot import load_robot_sprite_sheets
from Block import Block
from Robot_Path import *
from button import Button


def get_background(name):
    image = pg.image.load(join("assets", "IHM", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw(window, player, offset_x, offset_y, robot):
    player.draw(window, offset_x, offset_y)
    robot.draw(window, offset_x, offset_y)
    pygame.display.update()


def handle_collide_upgrade(player, robot, objects):
    collect_sound = get_sound("Collect_Sound.mp3", 0.05)
    for obj in objects:
        if pg.sprite.collide_mask(player, obj):
            if obj.rect.x < 1700:
                if robot.nombrePowerUp < 1:
                    collect_sound.play()
                    robot.set_nombre_powerUp(1)
            elif 1700 < obj.rect.x < 2700:
                if robot.nombrePowerUp < 2:
                    collect_sound.play()
                    robot.set_nombre_powerUp(2)
            elif obj.rect.x > 4000:
                if robot.nombrePowerUp < 3:
                    collect_sound.play()
                    robot.set_nombre_powerUp(3)

            else:
                pass
                # Ici il faut coder l'étape 4
                # print("Trophée hit")
                #
                # background_end, bg_image_end = get_background("VictoryPage.png")
                # for tile in background_end:
                #     window.blit(bg_image_end, tile)
                #
                # pygame.display.update()





def handle_collide_checkpoint(player, objects):
    for obj in objects:
        if pg.sprite.collide_mask(player, obj):
            player.set_respawn_point((obj.rect.x + obj.rect.width // 2), (obj.rect.y + obj.rect.height // 2))


def handle_collide_damage(player, objects):
    for obj in objects:
        if pg.sprite.collide_mask(player, obj):
            player.make_hit()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pg.sprite.collide_mask(player, obj):
            if dy > 0:
                if player.GRAVITY > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                else:
                    player.rect.bottom = obj.rect.top
                    player.hit_head()

            if dy < 0:
                if player.GRAVITY > 0:
                    player.rect.top = obj.rect.bottom
                    player.hit_head()
                else:
                    player.rect.top = obj.rect.bottom
                    player.landed()

        collided_objects.append(obj)

    return collided_objects


# On cherche a verfier la collision horizontale
# Le modele du joueur est deplacer par anicipation pour voir si le joueur toucherait un objet en avancant
# Si cest le cas on garde l'objet en memoire
# Puis on remet le joueur a sa position d'origine
def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pg.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, robot, objects, danger_objects, checkpoint_objects, upgrade_objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -10)
    collide_right = collide(player, objects, +10)

    if keys[pg.K_RIGHT] & keys[pg.K_LEFT]:
        player.x_vel = 0
    else:
        if keys[pg.K_LEFT] and not collide_left:
            player.move_left(5)

        if keys[pg.K_RIGHT] and not collide_right:
            player.move_right(5)

    handle_collide_upgrade(player, robot, upgrade_objects)
    handle_collide_checkpoint(player, checkpoint_objects)
    handle_collide_damage(player, danger_objects)
    handle_vertical_collision(player, objects, player.y_vel)


def main(window):
    clock = pg.time.Clock()
    etape = 0
    background, bg_image = get_background("Background_accueil.png")
    background_how, bg_image_how = get_background("howToPlayPage.png")
    background_cred, bg_image_cred = get_background("CreditsPage.png")

    # Création de la musique
    game_music = pygame.mixer.music.load(join("assets", "Music", "Menu_Theme.mp3"))
    pygame.mixer.music.play(-1)
    robot = Robot(50, 100, 50, 50)
    player = Player(100, 800, 50, 50)
    offset_x = 0
    offset_y = 0

    button_sound = get_sound("Button_Sound.mp3", 0.05)

    collect_1_done = False
    collect_2_done = False
    collect_3_done = False

    scroll_area_width = 0

    tmx_data = pytmx.load_pygame("assets/MapTiled/map.tmx")

    sprite_group = Sgroup()
    respawns = tmx_data.get_layer_by_name("respawns")
    collision_layer = tmx_data.get_layer_by_name('collisions')
    danger_collision_layer = tmx_data.get_layer_by_name('dangerCollisions')
    upgrade_layer = tmx_data.get_layer_by_name("upgrades")
    print(upgrade_layer)

    decor_list = []
    danger_list = []
    checkpoint_list = []
    upgrade_list = []
    speed_list = []

    for obj in respawns:
        print(obj.name)
        print(obj.id)
        if obj.id < 33 or obj.id > 380:
            respawn_bloc = Block(obj.x, obj.y, obj.width, obj.height)
            checkpoint_list.append(respawn_bloc)

    for obj in upgrade_layer:
        if obj.type == "Hitbox":
            print(obj.x)
            block_upgrade = Block(obj.x, obj.y, obj.width, obj.height)
            upgrade_list.append(block_upgrade)

    for obj in collision_layer:
        # if obj.name in ("rectangle1", "rectangle2", "rectangle3", "rectangle4"):
        test = obj
        block_test = Block(test.x, test.y, test.width, test.height)
        decor_list.append(block_test)

    for obj in danger_collision_layer:
        danger = obj
        block_danger = Block(danger.x, danger.y, danger.width, danger.height)
        danger_list.append(block_danger)

    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * 32 - offset_x, y * 32 - offset_y)
                Tile(pos, surf, sprite_group)

    for obj in tmx_data.objects:
        if obj.image:
            Tile((obj.x - offset_x, obj.y - offset_y), obj.image, sprite_group)


    run = True
    while run:
        clock.tick(60)


        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and player.jump_count < 1:
                    player.jump()
                if robot.nombrePowerUp >= 1:
                    if event.key == pg.K_a:
                        if player.GRAVITY > 0:
                            if player.GRAVITY == 5 or player.GRAVITY == 1:
                                player.GRAVITY = 12
                            elif player.GRAVITY == 12:
                                player.GRAVITY = 5
                        else:
                            if player.GRAVITY == -5 or player.GRAVITY == -1:
                                player.GRAVITY = -12
                            elif player.GRAVITY == -12:
                                player.GRAVITY = -5
                if robot.nombrePowerUp >= 2:
                    if event.key == pg.K_z:
                        if player.GRAVITY > 0:
                            if player.GRAVITY == 1:
                                player.GRAVITY = 5
                            elif player.GRAVITY == 5 or player.GRAVITY == 12:
                                player.GRAVITY = 1
                        else:
                            if player.GRAVITY == -1:
                                player.GRAVITY = -5
                            elif player.GRAVITY == -5 or player.GRAVITY == -12:
                                player.GRAVITY = -1
                if robot.nombrePowerUp >= 3:
                    if event.key == pg.K_e:
                        if player.gravity_reverse_count == 0:  # mettre == pour avoir droit qu'à 1 reverse gravity
                            player.gravity_reverse_count += 1
                            player.GRAVITY *= -1
                            if player.GRAVITY < 0:
                                player.PLAYER = "JeremyReverse"
                                player.SPRITES = load_sprite_sheets("MainCharacters", player.PLAYER, 32, 32, True)
                                robot.ROBOT = "KyojuReverse"
                                robot.SPRITE = load_robot_sprite_sheets("MainCharacters", robot.ROBOT, 32, 32)
                            else:
                                player.PLAYER = "Jeremy"
                                player.SPRITES = load_sprite_sheets("MainCharacters", player.PLAYER, 32, 32, True)
                                robot.ROBOT = "Kyoju"
                                robot.SPRITE = load_robot_sprite_sheets("MainCharacters", robot.ROBOT, 32, 32)

        if etape == 0:

            for tile in background:
                window.blit(bg_image, tile)

            mx, my = pygame.mouse.get_pos()
            if 570 > mx > 450 and 510 > my > 450:
                start_img = pygame.image.load('assets/IHM/boutons/Play_hover.png').convert_alpha()
            else:
                start_img = pygame.image.load('assets/IHM/boutons/Play.png').convert_alpha()
            start_button = Button(450, 450, start_img, 0.8)
            if start_button.draw(window):
                button_sound.play()
                etape = 1
                pygame.mixer.music.stop()
                game_music = pygame.mixer.music.load(join("assets", "Music", "Game_Theme.mp3"))
                pygame.mixer.music.play(-1)

            if 607 > mx > 407 and 565 > my > 525:
                rules_img = pygame.image.load('assets/IHM/boutons/howToPlay_hover.png').convert_alpha()
            else:
                rules_img = pygame.image.load('assets/IHM/boutons/howToPlay.png').convert_alpha()
            rules_button = Button(407, 525, rules_img, 0.8)
            if rules_button.draw(window):
                button_sound.play()
                etape = 2

            if 250 > mx > 50 and 740 > my > 700:
                credits_img = pygame.image.load('assets/IHM/boutons/Credits_hover.png').convert_alpha()
            else:
                credits_img = pygame.image.load('assets/IHM/boutons/Credits.png').convert_alpha()
            credits_button = Button(50, 700, credits_img, 0.8)
            if credits_button.draw(window):
                button_sound.play()
                etape = 3

            if 1000 > mx > 800 and 740 > my > 700:
                quit_img = pygame.image.load('assets/IHM/boutons/Quit_hover.png').convert_alpha()
            else:
                quit_img = pygame.image.load('assets/IHM/boutons/Quit.png').convert_alpha()
            quit_button = Button(800, 700, quit_img, 0.8)
            if quit_button.draw(window):
                button_sound.play()
                pygame.quit()
                run = False

            pygame.display.update()

        if etape == 1:




            player.loop(60)
            update_robot_position(robot, player)
            robot.loop(player)
            handle_move(player, robot, decor_list, danger_list, checkpoint_list, upgrade_list)

            draw(window, player, offset_x, offset_y, robot)
            sprite_group.drawGroup(window, offset_x, offset_y)

            if (player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0:
                offset_x += WIDTH - 2 * scroll_area_width
            elif (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0:
                offset_x -= WIDTH - 2 * scroll_area_width

            if (player.rect.bottom - offset_y >= HEIGHT - scroll_area_width) and player.y_vel > 0:
                offset_y += HEIGHT - 2 * scroll_area_width
            elif (player.rect.top - offset_y <= scroll_area_width) and player.y_vel < 0:
                offset_y -= HEIGHT - 2 * scroll_area_width

        if etape == 2:
            for tile in background_how:
                window.blit(bg_image_how, tile)

            mx, my = pygame.mouse.get_pos()
            if 600 > mx > 400 and 740 > my > 700:
                return_img = pygame.image.load('assets/IHM/boutons/return_hover.png').convert_alpha()
            else:
                return_img = pygame.image.load('assets/IHM/boutons/return.png').convert_alpha()
            return_button = Button(400, 700, return_img, 0.8)
            if return_button.draw(window):
                button_sound.play()
                etape = 0

            pygame.display.update()

        if etape == 3:
            for tile in background_cred:
                window.blit(bg_image_cred, tile)

            mx, my = pygame.mouse.get_pos()
            if 600 > mx > 400 and 740 > my > 700:
                return_img = pygame.image.load('assets/IHM/boutons/return_hover.png').convert_alpha()
            else:
                return_img = pygame.image.load('assets/IHM/boutons/return.png').convert_alpha()
            return_button = Button(400, 700, return_img, 0.8)
            if return_button.draw(window):
                button_sound.play()
                etape = 0

            pygame.display.update()

    pg.quit()
    quit()


if __name__ == "__main__":
    main(window)
