import pygame
import random
import math

from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800, 600))


# Music load
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title
pygame.display.set_caption('Space Invaders')

# Photos
icon = pygame.image.load('idea.png')
pygame.display.set_icon(icon)

# bullet photo
bulletImg = pygame.image.load('bullet.png')

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score_val = font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(score_val, (textX, textY))



#Player 1
playerImg = pygame.image.load('idea.png')
playerX = 370
playerY = 480

# Enemy 1
num_of_enemy = 10

enemyImg = []
enemyX = []
enemyY = []

enemyX_change = []
enemyY_change = []

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(0,100))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# enemyImg = pygame.image.load('monster.png')
# enemyX = random.randint(0, 800)
# enemyY = random.randint(0,100)
#
# enemyX_change = 0.3
# enemyY_change = 40

# BUllet co-ordinates
bulletX = -1
bulletY = playerY
bulletX_change = 0
bulletY_change = 0.3
bullet_state = 'ready'

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2)+math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True

pressed_up = False
pressed_down = False
pressed_left = False
pressed_right = False
fired = False

while running:
    screen.fill((0, 0, 0))

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    # Check whether key is pressed depending on right or left
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                #playerX -= 1
                pressed_left = False
                print('Keystroke left is released')

            if event.key == pygame.K_RIGHT:
                #playerY -= 1
                pressed_right = False
                print('Keystroke right is released')

            if event.key == pygame.K_UP:
                #playerX -= 1
                pressed_up = False
                print('Keystroke up  is released')

            if event.key == pygame.K_DOWN:
                #playerY -= 1
                pressed_down = False
                print('Keystroke down is released')

            if event.key == pygame.K_SPACE:
                print('space key release')
                bullet_state = 'fire'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('Left key')
                #playerX -= 1
                pressed_left = True

            if event.key == pygame.K_RIGHT:
                print('Right key')
                #playerX += 1
                pressed_right = True

            if event.key == pygame.K_UP:
                print('Up  key')
                #
                pressed_up = True

            if event.key == pygame.K_DOWN:
                print('Down key')
                #playerY += 1
                pressed_down = True

            if event.key == pygame.K_SPACE:
                print('space key')
                #playerY += 1
                #bulletX = playerX
                bullet_state = 'fire'
                #fire_bullet(bulletX, bulletY)
                #fired = True

    # SPaceship movement
    if pressed_up:
        playerY -= 0.1
    if pressed_down:
        playerY += 0.1
    if pressed_left:
        playerX -= 0.1
    if pressed_right:
        playerX += 0.1

    if playerX <= 0:
        playerX = 0
    elif playerX >= 773:
        playerX = 773

    if bullet_state == 'fire':
        if bulletX < 0:
            bulletX = playerX
        bullet_sound = mixer.Sound('laser.wav')
        bullet_sound.play()

        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = playerY
        bulletX = -1
        print('i am ready')

    for i in range(num_of_enemy):
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 0.3
            enemyY[i] = enemyY[i] + enemyY_change[i]
        elif enemyX[i] >= 773:
            enemyX[i] = 773
            enemyX_change[i] = -0.3
            enemyY[i] = enemyY[i] + enemyY_change[i]
        elif enemyY[i] > 750:
            enemyY[i] = 0

        enemyX[i] = enemyX[i] + enemyX_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision and bullet_state == 'fire':
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play(-1)
            bulletY = playerX
            bullet_state = 'ready'
            score += 1
            print(score)

            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(0, 400)

        enemy(enemyX[i], enemyY[i], i)

    show_score(textX, textY)
    player(playerX, playerY)

    pygame.display.update()
