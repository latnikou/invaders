# импортируем библиотеки
import pygame
import random
import math
from pygame import mixer

pygame.init() #включаем пайгейм

screen = pygame.display.set_mode((800, 600)) # параметры окна

background = pygame.image.load('background.png') # фоновый рисунок

mixer.music.load('background.wav') # фоновая музыка
mixer.music.set_volume(0.1)
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders") # название окна
icon = pygame.image.load('ufo.png') # значок
pygame.display.set_icon(icon)

# переменные игрока
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# переменные врага
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# создание нескольких противников
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# создание пули и переменные
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# надписи "очки" и "игра окончена"
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf', 64)

# функция для прорисовки надписи "игра окончена"
def game_over_text():
    over_text = font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# функция для прорисовки очков
def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# функция для прорисовки врага
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# функция для прорисовки игрока
def player(x, y):
    screen.blit(playerImg, (x, y))

# функция для выстрела и прорисовки пули
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# функция для проверки столкновений
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 28:
        return True
    else:
        return False

# игровой цикл
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # обработчик событий + работа с клавиатурой
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # границы для игрока
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # движение врагов + границы
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # столкновения
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # стрельба
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
