import random
import math
import pygame
from pygame import mixer

#  https://www.youtube.com/watch?v=FfWpgLFMI7w
# pygame
pygame.init()

#                               (width, height)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('BG.png')
# Title and Code
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('project.png')
pygame.display.set_icon(icon)

# Player
PlayerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480 #Depending on the selected screen size
playerX_Change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
noOfEnemeies = 6

for i in range(noOfEnemeies):
    enemyImg.append(pygame.image.load('mzon.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150)) #Depending on the selected screen size
    enemyX_Change.append(4)
    enemyY_Change.append(20)

# Bullet
#    Ready: can not see the bullet on the screen, Fire: The bullet moving on the screen
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 5
bulletState = "Ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 28)
textX = 10
textY = 10

font1 = pygame.font.Font('freesansbold.ttf', 70)

def displayScore(x, y):
    scoreV = font.render("Score: " + str(score) , True, (255, 255, 255))
    screen.blit(scoreV, (x, y))

def gameOver_Text():
    over_text = font1.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    screen.blit(PlayerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def Fire_bullet(x, y):
    global bulletState
    bulletState = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - enemyY, 2)) + (math.pow(bulletX - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # RGB = REd, Green, Blue
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # To verify that the keys pressed are left or right so that it moves based on what is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -5
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5
            if event.key == pygame.K_SPACE:
                if bulletState == "Ready": # To shoot one bullet at a time

                    bulletX = playerX
                    Fire_bullet(bulletX,bulletY)
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    # To verify that the player and enemies do not cross the page limits
    playerX += playerX_Change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736  # 800 - 64.is the image size

    # Enemy movement
    for i in range(noOfEnemeies):

        # End of the game
        if enemyY[i] > 440:
            for j in range(noOfEnemeies):
                enemyY[j] = 2000
            gameOver_Text()
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 0.9
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] = -0.9  # 800 - 64.is the image size
            enemyY[i] += enemyY_Change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletSound = mixer.Sound('explosion.wav')
            bulletSound.play()
            bulletY = 480
            bulletState = "Ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "Ready"

    if bulletState  == "Fire":
        Fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    displayScore(textX, textY)
    pygame.display.update()
