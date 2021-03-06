# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *
from sys import exit

import random

SCREEN_HIGHT = 800
SCREEN_WIDTH = 600

pygame.init()
# 初始化pygame,为使用硬件做准备

screen = pygame.display.set_mode((SCREEN_HIGHT, SCREEN_WIDTH), 0, 32)

pygame.display.set_caption('COOSK')

filename = 'Humming Urban Stereo - Scully Doesn_&#039;t Know.mp3'
pygame.mixer.music.load(filename)
pygame.mixer.music.play(loops=0, start=0.0)

mouse_image_filename = 'mouse.png'
mouse_cursor = pygame.image.load(mouse_image_filename).convert()

class Player(pygame.sprite.Sprite):
    """Sprite 用来扩展的，可以包含想要在屏幕上呈现的对象一个或多个图形表示"""
    def __init__(self):
        super(Player, self).__init__()
        '''self.surf = pygame.Surface((75, 25))'''
        self.image = pygame.image.load('飞碟.png').convert()
        self.cooldown = 15
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        # Surface和 Rects是 PyGame 中的基本构件
        # 将 Surface 看作一张白纸，你可以在上面随意绘画
        # fill 设定Surface的颜色，使其和屏幕分离
        # Rects 是 Surface 中矩形区域的表示
        # 调用convert()创建副本，这样可以更快地将它画在屏幕上（将图像数据都转化为Surface对象）
        # set_colorkey用于设置图片的颜色
        # RLEACCEL 有助于 PyGame 在非加速显示器上更快地渲染

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        elif pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
            # 限定player在屏幕中

    def shoot(self):
        bullet = Bullet(self.rect.midtop)
        Bullet.append(bullet)
        pass

class Enemy(pygame.sprite.Sprite):
    """docstring for Enemy"""
    def __init__(self, image=None):
        super(Enemy, self).__init__()
        '''self.surf = pygame.Surface((20, 10))'''
        self.image = image or Enemy._default_image
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(820, random.randint(0, 600)))
        self.speed = random.randint(1, 2)
        # 敌人从屏幕右边（820）的随机位置（0-600）上出现

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            # 检测敌人右侧是否通过了屏幕左边边界
            # 当敌人通过屏幕的边界后，调用 Sprite 的内建方法kill()，从 sprite 组中删除它们

class Cloud(pygame.sprite.Sprite):
    """docstring for Cloud"""
    def __init__(self):
        super(Cloud, self).__init__()
        self.image = pygame.image.load('白云.png').convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center = (random.randint(820, 900), random.randint(0, 600)))
        self.speed = 0

    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    """docstring for Bullet"""
    def __init__(self, init_pos, image = None):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image or Bullet._default_image
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.midtop = init_pos
        self.speed = 10

    def update(self):
        self.rect.centerx += self.speed

player = Player()
# 初始化Player

background = pygame.Surface(screen.get_size())
background.fill((135,206,250))

Bullet._default_image = pygame.image.load('geometrybullet.png').convert()
Enemy._default_image = pygame.image.load('炮弹.png').convert()

ADDENEMY= pygame.USEREVENT + 1
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
Bullet.containers = all_sprites, bullets
# Groups 是 Sprite 的集合, 用来包含游戏中的所有 Sprites
# 将 Player 添加到里面，因为它是我们目前唯一的 Sprite
# 为敌人创建一个 group 。 当我们调用 Sprite 的 kill() 方法时，sprite 将会从其所在的全部 group 中删除。

ADDCLOUD = pygame.USEREVENT + 2
clouds = pygame.sprite.Group()

flag = 0
bullets = []

pygame.time.set_timer(ADDCLOUD, 1000)
pygame.time.set_timer(ADDENEMY, 750)
# 每隔 750 毫秒触发一次 ADDENEMY 事件

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
        # 检测 KEYDOWN 事件: KEYDOWN 是 pygame.locals 中定义的常量

            if event.key == K_ESCAPE:
                running = False
                # 如果按下 Esc 那么主循环终止

            if event.key == K_SPACE:
                if flag == 1:
                    player.shoot()

        elif event.type == QUIT:
            running = False
            # 检测 QUIT : 如果 QUIT, 终止主循环
            # QUIT 用户按下关闭按钮

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            # 监听 ADDENEMY 事件
            # 创建一个 Enemy类的实例,将实例添加到 enemies 这个 Sprite Group(检测冲突) 和 all_sprites Group（这样它会和其他对象一起渲染）

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    for bullet in bullets:
        if bullet.rect.colliderect(Enemy):
            bullet.kill()
            Enemy.kill()
            SCORE += 50


    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    x, y = pygame.mouse.get_pos()
    x-= mouse_cursor.get_width() / 2
    y-= mouse_cursor.get_height() / 2

    screen.blit(mouse_cursor, (x, y))

    screen.blit(background, (0, 0))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        # 渲染

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        # spritecollideany() 检测 Sprite 对象是否和 Sprite Group 中的其他 Sprites 冲突

    pygame.display.flip()
    # 刷新