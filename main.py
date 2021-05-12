##############################################
# main.py
#
# author : Shrivani S
# date : May 12,2021
#
#
##############################################

import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# creating screen(width,height)
screen = pygame.display.set_mode((600, 500))

# creating background image
# background = pygame.image.load("back.png")
# mixer.music.load('filename')
# mixer.music.play(-1)  -1 is for continous background music
# icons are available at flaticon.com

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space.png")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load("space-invaders.png")
playerX = 270
playerY = 400
playerX_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0, 536))
    enemyy.append(random.randint(30, 50))
    enemyx_change.append(0.2)
    enemyy_change.append(40)

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 400
bulletx_change = 0
bullety_change = 1.0
bullet_state = "ready"

# score
# other fonts are available on www.dafont.com
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 36)

textx = 10
texty = 10

# game over text
over_text = pygame.font.Font('freesansbold.ttf', 74)


def show_score(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_msg = over_text.render("GAME OVER!!", True, (255, 0, 0))
    screen.blit(over_msg, (50, 200))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 5))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow((enemyx - bulletx), 2)) + (math.pow((enemyy - bullety), 2)))
    if distance < 30:
        return True
    else:
        return False


# game loop

running = True
while running:
    # rgb
    screen.fill((20, 110, 20))
    # screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed then check wheather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # gets current x cordinate of spaceship
                    bulletx = playerX
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            playerX_change = 0

    playerX += playerX_change

    # setting object  boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 536:
        playerX = 536

    # movement of enemy
    for i in range(num_of_enemy):

        if enemyy[i] > 360:
            for j in range(num_of_enemy):
                enemyy[j] = 2000

            game_over()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.3
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 536:
            enemyx_change[i] = -0.3
            enemyy[i] += enemyy_change[i]

        # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 400
            bullet_state = "ready"
            score_val += 10

            enemyx[i] = random.randint(0, 536)
            enemyy[i] = random.randint(30, 50)

        enemy(enemyx[i], enemyy[i], i)

    # movement of bullet
    if bullety <= 0:  # multiple bullet
        bullety = 400
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerX, playerY)
    show_score(textx, texty)
    pygame.display.update()
