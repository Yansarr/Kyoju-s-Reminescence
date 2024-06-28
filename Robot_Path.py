from os import listdir
from os.path import isfile, join
import pygame as pg
import math
import pygame.sprite

from Player import Player
from Robot import Robot



def update_robot_position(robot, player):

    if player.GRAVITY > 0:
        if player.direction == "right":
            # robot.rect.x = player.rect.x - 32
            # robot.rect.y = player.rect.y - 32
            robot.dest_X = player.rect.x - 32
            robot.dest_Y = player.rect.y - 32
        else:
            # robot.rect.x = player.rect.x + 44
            # robot.rect.y = player.rect.y - 32
            robot.dest_X = player.rect.x + 44
            robot.dest_Y = player.rect.y - 32
    else:
        if player.direction == "left":
            # robot.rect.x = player.rect.x + 56
            # robot.rect.y = player.rect.y + 56
            robot.dest_X = player.rect.x + 56
            robot.dest_Y = player.rect.y + 56
        else:
            # robot.rect.x = player.rect.x - 32
            # robot.rect.y = player.rect.y + 56
            robot.dest_X = player.rect.x - 32
            robot.dest_Y = player.rect.y + 56

    robot.player_distance_X = abs(robot.dest_X) - abs(robot.rect.x)
    robot.player_distance_Y = abs(robot.dest_Y) - abs(robot.rect.y)

    update_robot_speed(robot)

    # Coordonnées en X


def update_robot_speed(robot):

    # racine carrée de la distance
    if robot.player_distance_X != 0:
        if robot.rect.x == robot.dest_X:
            robot.x_vel = 0
        elif robot.rect.x < robot.dest_X:
            robot.x_vel = math.sqrt(abs(robot.player_distance_X))
        elif robot.rect.x > robot.dest_X:
            robot.x_vel = math.sqrt(abs(robot.player_distance_X)) * -1
    else:
        robot.x_vel = 0

    if robot.player_distance_Y != 0:
        if robot.rect.y == robot.dest_Y:
            robot.y_vel = 0
        elif robot.rect.y < robot.dest_Y:
            robot.y_vel = math.sqrt(abs(robot.player_distance_Y))
        elif robot.rect.y > robot.dest_Y:
            robot.y_vel = math.sqrt(abs(robot.player_distance_Y)) * -1
    else:
        robot.y_vel = 0
