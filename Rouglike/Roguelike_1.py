# -*- coding: UTF-8 -*-

import libtcodpy as libtcod
import math
import textwrap

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
# 房间最大的数量

color_dark_wall = libtcod.Color(0, 0, 100) # 视野外的墙壁颜色
color_light_wall = libtcod.Color(130, 110, 50) #视野内的墙壁颜色
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

MAX_ROOM_MONSTERS = 3
# 最大怪物量为3

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
# 状态栏的大小于坐标

MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

MAX_ROOM_ITEMS = 2

INVENTORY_WIDTH = 50

HEAL_AMOUNT = 4

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

panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

class Tile:
    """设定能否通过的区域"""
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        self.explored = False
        # 战争之雾 a.k.a Fog of War
        # 表示探索过的地区将会以阴影颜色显示

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Object:
    """这是一个通用的对象：玩家，怪物，物品，楼梯......  """
    def __init__(self, x, y, char,  name , color, blocks = False, fighter = None, ai = None, item = None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks

        self.fighter = fighter
        if self.fighter:
            # 让战斗系统‘知道’谁拥有它
            self.fighter.owner = self
            pass

        self.ai = ai
        if self.ai:
            # 让AI系统‘知道’谁拥有它
            self.ai.owner = self
            pass

        self.item = item
        if self.item:
            self.item.owner = self
            pass

    def move(self, dx, dy):
        '''if not map[self.x + dx][self.y + dy].blocked:# 如果移动超出地图自动退出 备用'''
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
        pass

    def draw(self):
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_default_foreground(con, self.color )
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
            # 设置颜色，然后在其位置绘制表示此对象的字符

    def clear(self):
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
        pass

    def move_towards(self, target_x, target_y):
        # 算出从此对象（怪物）到目标（玩家）的距离
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2) # dx的2次方，dy的2次方

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)
        pass

    def distance_to(self, other):
        # 返回到另一个对象的距离
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def send_to_back(self):
        global object
        objects.remove(self)
        objects.insert(0, self)
        pass
    # 返回怪物尸体的值

class Rect:
    """docstring for Rect"""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    # 创建矩形房间的框架
    # 左上角（x1，y1）和右下角（x2，y2）

    def center(self):
        center_x = (self.x1 + self.x2)/2
        center_y = (self.y1 + self.y2)/2
        return (center_x, center_y)
    # 创建一个返回 room 中心坐标的方法

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
    # 分割 room 之间的距离使之不重叠

class Fighter:
    """与战斗有关的属性和方法（怪物， 玩家， NPC）"""
    def __init__(self, hp, defense, power, death_function = None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage):
        # 伤害以及损伤
        if damage > 0:
            self.hp -= damage

        if self.hp <= 0:
        # 检查目标是否死亡。如果是，调用死亡函数。
            function = self.death_function
            if function is not None:
                function(self.owner)

    def attack(self, target):
        # 一个简单的计算攻击伤害公式
        damage = self.power - target.fighter.defense

        if damage > 0:
            # 使目标受到伤害的信息以消息 message  的方式打印出来
            '''
            print self.owner.name.capitalize() + ' attack ' + target.name + 'for ' + str(damage) + 'hit points.'
            target.fighter.take_damage(damage)
        else:
            print self.owner.name.capitalize() + ' attack ' + target.name + 'but it has no effect!'
            '''
            message(self.owner.name.capitalize() + ' attack ' + target.name + ' for ' + str(damage) + 'hit points')
            target.fighter.take_damage(damage)
        else:
            message(self.owner.name.capitalize() + ' attack ' + target.name + ' but it has no effect!')

    def cast_heal():
        if player.fighter.hp == player.fighter.max_hp:
            message("You are already at full health", libtcod.red)
            return 'cancelled'

        message('Your wounds start to feel better!', libtcod.light_violet)
        player.fighter.heal(HEAL_AMOUNT)


class BasicMonster:
    """基本怪物AI"""
    def take_turn(self):
        # 一个基本的怪物‘视觉’,在玩家的FOV内,如果你能看到它，它也可以看到你
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            pass

            if monster.distance_to(player) >= 2:# 如果怪物距离玩家 >=2,就移动向玩家
                monster.move_towards(player.x, player.y)
                pass

            elif player.fighter.hp > 0:
            # 如果怪物距离玩家小于2,就攻击玩家，并判断玩家是否存活
                monster.fighter.attack(player)
                print 'The attack of the ' + monster.name + 'bounces off your shiny metal armor'

class Item:
    """可以拾取和使用的物品"""
    def __init__(self, use_function=None):
        self.use_function = use_function


    def pick_up(self):
        if len(inventory) >= 26: # 通过按下从A到Z的键来选择项目，并且只有26个字母
            message("Your inventory is full, cannot pick up" + self.owner.name + ".", libtcod.red )
            pass
        else:
            inventory.append(self.owner)
            objects.remove(self.owner)
            message("You picked up a" + self.owner.name + '!', libtcod.green)

    def use(slef):
        if self.use_function is None:
            message('The' + self.owner.name + 'cannot be used')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self.owner)
                # 使用后销毁, 除非因某种原因被取消
                pass
        pass
def create_room(room):
    global map

    for x in range( room.x1, room.x2 + 1):
        for y in range( room.y1, room.y2 + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False
            # 左上角x1,y1 右下角x2,y2
            pass
        pass
    # room.x2/y2 + 1 使 room 彼此不相邻且总有一道墙隔开
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
        # 且随机的位置不超过地图的边界
        # random_get_int 返回两个数字之间的随机整数
        # (0, 0) 默认

        new_room = Rect(x, y, w, h)

        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        # 创建另一个 room 看他是否重叠或相交这个 room

        if not failed:
        # 如果没有重叠或相交，则这个 room 是有效的
            create_room(new_room)

            (new_x, new_y) = new_room.center()

            if  num_rooms == 0:
                player.x = new_x
                player.y = new_y
                # 当玩家第一次所在的位置时，这将是第一个 room

            else:
                # 在第一个房间后的所有房间
                # 用隧道将它连接到先前的房间

                (prev_x, prev_y) = rooms[num_rooms - 1].center()
                # 新 room 的中心坐标

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

            place_objects(new_room)

            rooms.append(new_room)
            num_rooms +=1

def create_h_tunnel(x1, x2, y):# 水平隧道
    global map

    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
        pass

    for x in range(x1, x2 + 1):
        pass
    pass
    # 返回两个参数的最小值或最大值
    # 如果x1 <x2，x1将是两者的最小值，x2是最大值
    # 创建一个从一个room 到另一个room 的隧道

def create_v_tunnel(y1, y2, x):# 垂直隧道
    global map

    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
        pass
    pass

def place_objects(room):
    # 怪物与物品的随机位置

    num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

    for i in range(num_monsters):
        # 随机怪物的出生点
        x = libtcod.random_get_int(0, room.x1, room.x2)
        y = libtcod.random_get_int(0, room.y1, room.y2)

        if not is_blocked(x, y):
            # 如果没有被阻塞
            if libtcod.random_get_int(0, 0, 100) < 80:
                # 80%的几率生成一个兽人

                fighter_component = Fighter(hp = 10, defense = 0, power = 3, death_function = monster_death)
                # 设置生命，防御力，力量

                ai_component = BasicMonster()

                monster = Object(x, y, 'o', 'orc', libtcod.desaturated_green, blocks = True,fighter = fighter_component, ai = ai_component)
            else:
                # 否则生成一个巨魔
                fighter_component = Fighter(hp = 16, defense = 1, power = 4, death_function = monster_death)
                ai_component = BasicMonster()

                monster = Object(x, y, 'T', 'troll', libtcod.darker_green, blocks = True, fighter = fighter_component, ai = ai_component)

            objects.append(monster)
            pass

    num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)

    for i in range(num_items):
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        if not is_blocked(x, y):
            item_component = Item(use_function=cast_heal)
            item = Object(x, y, '!', 'healing potion', libtcod.violet, item = item_component)
            # 创建一个治疗药水

            objects.append(item)
            item.send_to_back()
            # item 出现在其他对象的下面
        pass

def is_blocked(x, y):
    # 测试 map 中的 tile 是否堵塞
    if map[x][y].blocked:
        return True

    for object in objects:
        # 检查任何堵塞的 objects
        if object.blocks and object.x == x and object.y == y:
            return True
    return False

def render_all(): # 绘制列表中的所有对象
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
        if object != player:
            object.draw()
    player.draw()
    # 防止怪物尸体与角色重叠，造成无法渲染

    libtcod.console_blit( con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(0, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
        'HP:' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp))
    # 在屏幕左下角显示玩家的血量

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    # 准备呈现GUI状态栏

    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
    # 将状态栏渲染出来

    render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
    # 显示玩家的统计

    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)
    # 将“面板”的内容提交到根控制台

    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
    # sys_check_for_event函数返回键盘和鼠标活动的信息

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE,  libtcod.LEFT, get_names_under_mouse())

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # 渲染状态栏（血量， 经验等 ），但首先计算状态栏的宽度

    bar_width = int (float (value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    # 渲染后台

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
        pass
    # 将状态栏呈现在顶上

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER, name + ':' + str(value) + '/' + str(maximum))
    pass

def message(new_msg, color = libtcod.white):
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]
        # 如果消息超出消息的最大高度，就删除第一行以腾出空间给新的一个

        game_msgs.append((line, color))
        # 将新行添加为元组，文本和颜色

def get_names_under_mouse():
    global mouse

    (x, y) = (mouse.cx, mouse.cy)
    # 返回一个字符串，其中包含鼠标下所有对象的名称
    # 访问鼠标结构的cx和cy字段,它们是鼠标结束的图块（或单元格）的坐标。

    names = [obj.name for obj in objects
        if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]
    # 收集满足几个条件的对象名称列表
    # 它们在鼠标下面和玩家的FOV内（they're under the mouse, and inside the player's FOV. ）

    names = ', '.join(names) # 在 name 中，用逗号分隔
    return names.capitalize()

def player_move_or_attack(dx, dy):
    global fov_recompute

    x = player.x + dx
    y = player.y + dy
    # 协调 player 边移动边攻击

    target = None
    for object in objects:
        if object.fighter and object.x == x and object.y == y:
            target = object
            break
    # 尝试去寻找被攻击的目标

    if target is not None:
        player.fighter.attack(target)
        print 'The' + target.name + 'laughs at puny efforts to attack him!'
    else:
        player.move(dx, dy)
        fov_recompute = True
        pass
    # 如果发现目标攻击并移动

def player_death(player):
    # game over
    global game_state
    print 'You died!'
    game_state = 'dead'

    # 增加效果，将玩家变成尸体
    player.char = '%'
    player.color = libtcod.dark_red
    pass

def monster_death(monster):
    # 将怪物变成尸体，但它的尸体不能造成道路堵塞（block）
    # 变成尸体时不能移动,关闭ai
    print monster.name.capitalize() + 'is dead!'
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remians of ' + monster.name
    monster.send_to_back()


def handle_keys():#控制键位与角色行走
    '''global playerx,playery # 备用'''
    '''global fov_recompute'''
    global key

    '''
    key = libtcod.console_wait_for_keypress(True)
    '''

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt + Enter: toggle fullscreen
        # 切换键

        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        # 全屏

    elif key.vk == libtcod.KEY_ESCAPE:
        return True
        # 按下 ESC 则 exit game

    if game_state == 'playing':
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            player_move_or_attack(0, -1)
            fov_recompute = True
            # fov_recompute 只要玩家移动或 tile 改变，FOV只需要重新计算。
            # 为了建模，我们将在主循环之前定义一个全局变量fov_recompute = True。
            # 然后，在handle_keys函数中，每当玩家移动，我们将其设置为True


        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            player_move_or_attack(0, 1)
            fov_recompute = True


        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            player_move_or_attack(-1, 0)
            fov_recompute = True


        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            player_move_or_attack(1, 0)
            fov_recompute = True

        else:

            key_char = chr(key.c)

            if key_char == 'g':
                for object in objects:
                    if object.x == player.x and object.y == player.y and object.Item:
                        object.item.pick_up()
                        break

            if key_char == 'i':
                # 显示库存
                inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
                pass

            return 'didnt-take-turn'

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


'''
player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
# 角色
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
# 用于测试 黄色的@代表一个非玩家的角色(NPC)
objects = [npc, player]
备用
'''

def menu(header, options, width):
    if len(options) > 26:raise ValueError('Cannot have a menu with more than 26 options.')

    header_heght = libtcod.console_get_height_rect(con, 0, 0, widh, SCREEN_HEIGHT, header)
    height = len(options) + header_heght
    # 计算页眉 (自动换行后) 和每选项一行的总高度

    window = libtcod.console_new(width, height)
    # 创建表示菜单窗口的控制台

    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
    # 打印 header, 自动换行

    y = header_heght
    letter_index = ord('a')
    for option_text in options:
        text = '('+ chr(letter_index) +')' + option_text
        y += 1
        letter_index += 1
        pass
    # 打印所有项目
    # 原理 ： 打印一个循环，第一个选项的 Y 坐标位于页眉的正下方;我们打印该选项的文本, 并增加它。
    # 然后从字母 A 开始, 每次递增, 以在选项的文本旁边显示它。函数返回字母 A 的 ASCII 码;
    # 然后, 可以用来增加它来获取其余字母的代码。

    x = SCREEN_WIDTH/2 - width/2
    y = SCREEN_HEIGHT/2 - height/2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    # 1.0 ， 0.7 它们分别定义了前景(文本)和背景的透明度

    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
    # 等待玩家做出选择，游戏才能继续

def inventory_menu(header):
    # 显示库存
    # 将 menu 中每个项目的 item 显示为选项

    if len(inventory) == 0:
        options = ['Inventory is empty']
    else:
        options = [item.name for item in inventory]

    index = menu(header, options, INVENTORY_WIDTH)


fighter_component = Fighter (hp = 100, defense = 3, power = 5, death_function = player_death)

player = Object(0, 0, '@', 'player', libtcod.white, blocks = True, fighter = fighter_component)

objects = [player]

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

game_state = 'playing'

player_action = None

game_msgs = []
# 创建游戏消息列表及其颜色，开始为空

inventory = []

message('Welcome stranger! Prepare to perish in the Tombs of Ancient Kings.', libtcod.red)

mouse = libtcod.Mouse()
key = libtcod.Key()
# 鼠标界面

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
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key,mouse)
    render_all()
    # 调用 render_all() 函数

    libtcod.console_flush()
    # 刷新

    for object in objects:
        object.clear()

    player_action = handle_keys()
    if player_action == 'exit':
        break

    if game_state == 'playing' and player_action != 'didnt-take-turn':
        for object in objects:
            if object.ai:
                object.ai.take_turn()
