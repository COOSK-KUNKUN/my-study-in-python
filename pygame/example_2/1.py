# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import*

bg1 = pygame.image.load('sushiplate.jpg')
bg2 = pygame.image.load('sushiplate.jpg')

pox_x1 = 0
pox_x2 = 640

pygame.init()

screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('滚动')

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                # 如果按下 Esc 那么主循环终止
        if event.type == QUIT:
            running == False

    screen.blit(bg1, (pox_x1, 0))
    screen.blit(bg2, (pox_x2, 0))

    pox_x1 -= 0.5
    pox_x2 -= 0.5

    if pox_x1 < -640:
        pox_x1 = 640
    elif pox_x2 < -640:
        pos_x2 = 640

    pygame.display.update()
