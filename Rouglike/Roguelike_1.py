# -*- coding: UTF-8 -*-

import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
# 房间最大的数量

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

FOV_ALGO = 0 # 默认FOV算法
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10
# 视野

'''
playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2
# 设定角色位置在屏幕中心
# 备用1
'''

libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
# 设定字体
# 字体来源于 arial12x12.png 的位图字体

libtcod.console_init_root( SCREEN_WIDTH, SCREEN_HEIGHT, 'COOSK',False)
# 初始化窗口，最后一个参数告诉它是否应该是全屏。


libtcod.sys_set_fps(LIMIT_FPS)
# 限制游戏的速度 (帧每秒或FPS)

con = libtcod.console_new( SCREEN_WIDTH, SCREEN_WIDTH)
# 创建一个新的屏幕外控制台
# 重要！！！！！

libtcod.console_blit( con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
# blit 允许您将源控制台的矩形区域移动到目标控制台上的特定位置
# console_blit （ src ， xSrc ， ySrc ， xSrc ， hSrc ， dst ， xDst ， yDst ， foregroundAlpha = 1.0 ， backgroundAlpha = 1.0 ）
# src 源代码控制台，必须在另一个 blitting 上
# xSrc，ySrc，WSRC，HSRC 源控制台的矩形区 如果wSrc和/或hSrc == 0，则使用源控制台宽度/高度
# DST 目标控制台
# xDst，yDst 目标控制台中源区域左上角的位置
# foregroundAlpha，backgroundAlpha 控制台的Alpha透明度
# 1.0 =>源控制台是不透明的

class Tile: # 设定能否通过的区域
    """docstring for Tile"""
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        self.explored = False
        # 战争之雾 a.k.a Fog of War
        # 表示探索过的地区将会以阴影颜色显示

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Object:
    """这是一个通用的对象：玩家，怪物，物品，楼梯......  """
    def __init__(self, x, y, char, color ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        if not map[self.x + dx][self.y + dy].blocked:# 如果移动超出地图自动退出
            self.x += dx
            self.y += dy
        pass

    def draw(self):
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_default_foreground(con, self.color )
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
        pass

class Rect:
    """docstring for Rect"""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    # 创建矩形房间的框架

    def center(self):
        center_x = (self.x1 + self.x2)/2
        center_y = (self.y1 + self.y2)/2
        return (center_x, center_y)
    # 创建一个返回 room 中心坐标的方法

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
    # 分割 room 之间的距离使之不重叠

def create_room(room):
    global map

    for x in range( room.x1, room.x2 + 1):
        for y in range( room.y1, room.y2 + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False
            # 左上角x1,y1 右下角x2,y2
            pass
        pass
    # room.x2/y2 + 1 使彼此不相邻的 room 总有一道墙隔开
    pass

def make_map():
    global map, player

    map = [[ Tile(True)
            for y in range(MAP_HEIGHT) ]
                for x in range(MAP_WIDTH) ]
    # 当 tile(false) 时 不会显示房间

    '''
    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[50][22].blocked = True
    map[50][22].block_sight = True
    # 建立区域
    # 备用
    '''
    '''
    room1 = Rect(20, 15, 10, 15)
    room2 = Rect(50, 15, 10, 15)
    create_room(room1)
    create_room(room2)
    # 创造两个房间
    # 备用
    '''

    '''
    player.x = 25
    player.y = 23
    # 让玩家出现在第一个房间的中央
    # 备用
    '''

    '''
    create_h_tunnel(25, 55, 23)
    # 创建水平隧道的位置
    # 备用
    '''

    rooms = []
    num_rooms = 0

    for r in range(MAX_ROOMS):
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        # room 随机的宽度与长度

        x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
        # 在地图范围内随机 room 的位置
        # random_get_int 返回两个数字之间的随机整数
        # (0, 0) 默认

        new_room = Rect(x, y, w, h)

        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        # 创建另一个 room 看他是否相交这个 room

        if not failed:
        # 如果没有相交，则这个 room 是有效的
            create_room(new_room)

            (new_x, new_y) = new_room.center()

            if  num_rooms == 0:
                player.x = new_x
                player.y = new_y
                # 当玩家第一次所在的位置时，这将是第一个 room

            else:
                # 当所有的 room 在第一个 room 的后面
                # 用隧道 tunnel 连接这些以前/之后(previons room?)的 room

                (prev_x, prev_y) = rooms[num_rooms - 1].center()
                # 协调这些 room 的中心坐标

                if libtcod.random_get_int(0, 0, 1) == 1:
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                    # 绘制连接这些 room 的隧道
                    # 首先水平移动，然后垂直移动

                else:
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
                    # 首先垂直移动，然后水平移动
                pass

            rooms.append(new_room)
            num_rooms +=1

        pass

def create_h_tunnel(x1, x2, y):# 水平隧道
    global map

    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
        pass

    for x in range(x1, x2 + 1):
        pass
    pass
    # 创建一个从一个room 到另一个room 的隧道

def create_v_tunnel(y1, y2, x):# 垂直隧道
    global map

    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
        pass
    pass

def render_all(): # 渲染
    global fov_map, color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_recompute

    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
        pass
    # 改变渲染代码来实际重新计算FOV，并显示结果！
    # 只需要重新计算FOV，并在recompute_fov为True的情况下渲染地图（然后我们将其重置为False）

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            visible = libtcod.map_is_in_fov(fov_map, x, y)
            wall = map[x][y].block_sight
            if not visible:
                # if it's not visible right now, the player can only see it if it's explored
                if map[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background( con, x, y, color_dark_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background( con, x, y, color_dark_ground, libtcod.BKGND_SET)
            else:
                if wall:
                    libtcod.console_set_char_background(con, x, y, color_light_wall, libtcod.BKGND_SET )
                else:
                    libtcod.console_set_char_background(con, x, y, color_light_ground, libtcod.BKGND_SET )
                # since it's visible, explore it
                # 既然它是可见的，那么就可以探索它

                map[x][y].explored = True

    for object in objects:
        object.draw()
        pass
    pass

    libtcod.console_blit( con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    pass

def handle_keys():#控制键位与角色行走
    '''global playerx,playery # 备用'''
    global fov_recompute

    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt + Enter: toggle fullscreen
        # 切换键

        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        # 全屏

    elif key.vk == libtcod.KEY_ESCAPE:
        return True
        # 按下 ESC 则 exit game

    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)
        fov_recompute = True
        # fov_recompute 只要玩家移动或 tile 改变，FOV只需要重新计算。
        # 为了建模，我们将在主循环之前定义一个全局变量fov_recompute = True。
        # 然后，在handle_keys函数中，每当玩家移动，我们将其设置为True


    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)
        fov_recompute = True


    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)
        fov_recompute = True


    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)
        fov_recompute = True

    '''
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        playery -= 1

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        playery += 1

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        playerx -= 1

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        playerx += 1

    # 该代码存在缺陷，当角色改变方向时，总会像原来的方向再前进一格，才改变方向。
    # 备用
    '''

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
# 角色

npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
# 用于测试 黄色的@代表一个非玩家的角色(NPC)

objects = [npc, player]

make_map()

fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
# libtcod FOV模块需要知道哪些 title 可见
# 所以,我们创建一个libtcod可以理解的地图（fov_map）
# 并使用 tile 自己的 block_sight 和 blocked 属性中的适当值来填充它们
# 实际上，只有 block_sight 会被使用; blocked 的值与FOV完全无关！(汗(lll￢ω￢))
# 它只对寻路模块(pathfinding module)有用，但是无论如何不会提供这个值。
# 另外，libtcod要求的值与我们定义的值相反，所以我们用not操作符来切换它们。

for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
        pass
    pass

fov_recompute = True

while not libtcod.console_is_window_closed():

    '''
    libtcod.console_set_default_foreground( 0, libtcod.white) 
    # 背景颜色白色

    libtcod.console_put_char( 0, playerx, playery, '@', libtcod.BKGND_NONE)
    # 打印一个字符到坐标（playerx,playery）. 0 表示再次指定控制台。

    libtcod.console_flush()
    # 刷新

    libtcod.console_put_char( 0, playerx, playery, ' ', libtcod.BKGND_NONE)
    # ‘ ’要空格

    # 备用1
    '''
    render_all()
    # 调用 render_all() 函数

    libtcod.console_flush()
    # 刷新

    for object in objects:
        object.clear()

    exit = handle_keys()
    if exit:
        break


