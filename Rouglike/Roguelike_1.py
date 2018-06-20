# -*- coding: UTF-8 -*-

import libtcodpy as libtcod
import math
import textwrap
import shelve

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 55

LIMIT_FPS = 100

MAP_WIDTH = 80
MAP_HEIGHT = 43

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

MAX_ROOM_MONSTERS = 3
# 最大怪物量为3

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
# 状态栏的大小与坐标

MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

MAX_ROOM_ITEMS = 2

INVENTORY_WIDTH = 50
HEAL_AMOUNT = 4
# 地图上的药水数量

LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 8
# 闪电法术伤害数值

CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8
# 迷惑法术

FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12
# 火球法术伤害数值

LEVEL_SCREEN_WIDTH = 40
LEVEL_UP_BASE = 200
LEVEL_UP_FACTOR = 150
# 经验值

CHARACTER_SCREEN_WIDTH = 30

class Tile:
    """设定能否通过的区域"""
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False
        # 战争之雾 a.k.a Fog of War （其实就是视野啦）
        # 表示探索过的地区将会以阴影颜色显示

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Object:
    """这是一个通用的对象：玩家，怪物，物品，楼梯......  """
    def __init__(self, x, y, char,  name , color, blocks = False, fighter = None, ai = None, item = None, always_visible = False):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.always_visible = always_visible # 允许一些对象始终可见

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

    def draw(self):
        if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or
            (self.always_visible and map[self.x][self.y].explored)):
            libtcod.console_set_default_foreground(con, self.color )
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
            # 设置颜色，然后在其位置绘制表示此对象的字符

    def clear(self):
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

    def move_towards(self, target_x, target_y):
        # 算出从此对象（怪物）到目标（玩家）的距离
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2) # dx的2次方，dy的2次方

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        # 返回到另一个对象的距离
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        return math.sqrt((x - self.x) **  2 + (y - self.y) ** 2)

    def send_to_back(self):
        global objects
        objects.remove(self)
        objects.insert(0, self)
        pass
    # 返回怪物尸体的值

class Rect:
    """用于生成整个地牢的构建模块"""
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
    def __init__(self, hp, defense, power, xp, death_function = None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp
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

            if self.owner != player:
                player.fighter.xp += self.xp
                # 每杀死怪物后加经验

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
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + 'hit points')
            target.fighter.take_damage(damage)
        else:
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp


class BasicMonster:
    """基本怪物AI"""
    def take_turn(self):
        # 给予怪物基本的 FOV 和在其与玩家 FOV 里的活动
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(player) >= 2:# 如果怪物距离玩家 >=2,就移动向玩家
                monster.move_towards(player.x, player.y)

            elif player.fighter.hp > 0:
            # 如果怪物距离玩家小于2,就攻击玩家，并判断玩家是否存活
                monster.fighter.attack(player)

class ConfusedMonster:
    """由闪电卷轴造成的混乱咒语 并让怪物恐惧(随机移动)"""
    def __init__(self, old_ai, num_turns = CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns
        # AI用于临时混淆的怪物（在一段时间后恢复到之前的AI）

    def take_turn(self):
        if self.num_turns >0: # still confused...
            self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
        # 随机移动（随机X和Y位移在-1和1之间）

        else:
            self.owner.ai = self.old_ai
            message('The' + self.owner.name + 'is no longer confused!', libtcod.red)

class Item:
    """可以拾取和使用的物品"""
    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        if len(inventory) >= 26: # 通过按下从A到Z的键来选择项目，并且只有26个字母
            message("Your inventory is full, cannot pick up" + self.owner.name + ".", libtcod.red )
        else:
            inventory.append(self.owner)
            objects.remove(self.owner)
            message("You picked up a" + self.owner.name + '!', libtcod.green)

    def use(self):
        if self.use_function is None:
            message('The' + self.owner.name + 'cannot be used')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self.owner)
                # 使用后销毁, 除非被玩家取消

    def drop(self):
        objects.append(self.owner)
        inventory.remove(self.owner)
        self.owner.x = player.x
        self.owner.y = player.y # 获取玩家坐标，使得掉落的物品在玩家的坐标下
        message('You dropped a' + self.owner.name + '.', libtcod.yellow)
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
    global map, objects, stairs
    objects = [player]

    map = [[ Tile(True)
            for y in range(MAP_HEIGHT) ]
                for x in range(MAP_WIDTH) ]
    # 当 tile(false) 时 不会显示房间

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
        # 创建另一个 room 看他是否重叠或相交其他 room

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

    stairs = Object(new_x, new_y, 's', 'stairs', libtcod.white)
    objects.append(stairs)
    stairs.send_to_back()
    # 在房间的中心创建向下的楼梯

def create_h_tunnel(x1, x2, y):# 水平隧道
    global map

    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
        pass
    pass

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

                fighter_component = Fighter(hp = 10, defense = 0, power = 3, xp = 35, death_function = monster_death)
                # 设置生命，防御力，力量

                ai_component = BasicMonster()

                monster = Object(x, y, 'o', 'orc', libtcod.desaturated_green, blocks = True,fighter = fighter_component, ai = ai_component)
            else:
                # 否则生成一个巨魔
                fighter_component = Fighter(hp = 16, defense = 1, power = 4, xp = 100, death_function = monster_death)
                ai_component = BasicMonster()

                monster = Object(x, y, 'T', 'troll', libtcod.darker_green, blocks = True, fighter = fighter_component, ai = ai_component)

            objects.append(monster)


    num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)

    for i in range(num_items):
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        if not is_blocked(x, y):
            dice = libtcod.random_get_int(0, 0, 100) # 在 治疗药水 与 闪电魔法卷轴 随机选择
            if dice < 70:
                item_component = Item(use_function = cast_heal)
                item = Object(x, y, '!', 'healing potion', libtcod.violet, item = item_component)
                # 创建一个治疗药水（70％机会）

            elif dice < 70 + 10:
                item_component = Item(use_function = cast_lightning)
                item = Object(x, y, '#', 'scroll of lightning bolt', libtcod.light_yellow, item = item_component)
                # 创建闪电卷轴（15％几率）

            elif dice < 70 + 10 + 10:
                item_component = Item(use_function = cast_fireball)

                item = Object(x, y, '#', 'scroll of fireball', libtcod.light_yellow, item = item_component)

            else:
                item_component = Item(use_function = cast_lightning)
                item = Object(x, y, '#', 'scroll of confusion', libtcod.light_yellow, item = item_component)
                # 创建一个迷惑法术（15％几率）

            objects.append(item)
            item.send_to_back()
            # item 出现在其他对象的下面

            item.always_visible = True
            # 即使不在探索范围里，FOV 仍可见



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
                # 如果它现在不可见，玩家只能在探索的时候才可见 （视野）
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

    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level' + str(dungeon_level))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE,  libtcod.LEFT, get_names_under_mouse())

    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)
    # 将“面板”的内容提交到根控制台

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # 渲染状态栏（血量， 经验等 ），但首先计算状态栏的宽度

    bar_width = int(float (value) / maximum * total_width)

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
    message(monster.name.capitalize() + ' is dead!', libtcod.orange)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = ' remians of ' + monster.name
    monster.send_to_back()

def handle_keys():#控制键位与角色行走
    '''global playerx,playery # 备用'''
    '''global fov_recompute'''
    global key;

    '''
    key = libtcod.console_wait_for_keypress(True)
    '''

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt + Enter: toggle fullscreen
        # 切换键

        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        # 全屏

    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'
        # 按下 ESC 则 exit game

    if game_state == 'playing':
        if key.vk == libtcod.KEY_UP:
            player_move_or_attack(0, -1)
            fov_recompute = True

        elif key.vk == libtcod.KEY_DOWN:
            player_move_or_attack(0, 1)
            fov_recompute = True

        elif key.vk == libtcod.KEY_LEFT:
            player_move_or_attack(-1, 0)
            fov_recompute = True

        elif key.vk == libtcod.KEY_RIGHT:
            player_move_or_attack(1, 0)
            fov_recompute = True

        else:
            key_char = chr(key.c)

            if key_char == 'g':
                for object in objects:
                    if object.x == player.x and object.y == player.y and object.item:
                        object.item.pick_up()
                        break

            if key_char == 'i':
                # 显示库存
                chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.use()

            if key_char == 'd':
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()

            if key_char == 's':
                if stairs.x == player.x and stairs.y == player.y:
                    next_level()

            if key_char == 'c': # 显示玩家属性
                level_up_xp = LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR
                msgbox('Character Information\n\n Level : ' + str(player.level) + '\n Experience : ' + str(player.fighter.xp) +
                    '\n Experience to level up : ' + str(level_up_xp) + '\n\n Maximum HP : ' + str(player.fighter.max_hp) +
                    '\n Attack : ' + str(player.fighter.power) + '\n Defense : ' + str(player.fighter.defense), CHARACTER_SCREEN_WIDTH)

            return 'didnt-take-turn'


def inventory_menu(header):
    # 显示库存
    # 将 menu 中每个项目的 item 显示为选项

    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory]

    index = menu(header, options, INVENTORY_WIDTH)

    if index is None or len(inventory) == 0:return None
    return inventory[index].item

def cast_heal():
    if player.fighter.hp == player.fighter.max_hp:
        message("You are already at full health", libtcod.red)
        return 'cancelled'

    message('Your wounds start to feel better!', libtcod.light_violet)
    player.fighter.heal(HEAL_AMOUNT)

def cast_lightning():
    monster = closest_monster(LIGHTNING_RANGE)
    if monster is None:
        message('No enemy is close enough to strike.', libtcod.red)
        return 'cancelled'
    # 找到最近的敌人（在最大范围内）并对其造成伤害

    message('A lighting bolt strikes the ' + ' with a loud thunder! The damage is ' + str(LIGHTNING_DAMAGE) + ' hit points.', libtcod.light_blue)
    monster.fighter.take_damage(LIGHTNING_DAMAGE)

def cast_fireball():
    message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan)
    (x, y) = target_tile()

    if x is None: return 'cancelled'
    message('The fireball explodes, burning everything within ' + str(FIREBALL_RADIUS) + ' tiles!', libtcod.orange)

    for obj in objects:  # 伤害射程内的所有物体
        if obj.distance(x, y) <= FIREBALL_RADIUS and obj.fighter:
            message('The ' + obj.name + ' gets burned for ' + str(FIREBALL_DAMAGE) + ' hit points.', libtcod.orange)
            obj.fighter.take_damage(FIREBALL_DAMAGE)
    # 投掷火球

def cast_confuse():
    message('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)
    monster = target_monster(CONFUSE_RANGE)
    if monster is None: return 'cancelled'

    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster
    message('The eyes of the ' + ' look vacant, as he starts to stumble around!', libtcod.light_green)
    # 将怪物的AI换成“困惑”的AI; 经过一段时间后，它会恢复旧的AI

def closest_monster(max_range): # 找到最近的敌人，达到最大范围，并且在玩家的FOV里
    closest_enemy = None
    closest_dist = max_range + 1
    # 开始时（稍大于）最大范围

    for object in objects:
        if object.fighter and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
            dist = player.distance_to(object)
            if dist < closest_dist: # it's closer, so remember it
                closest_enemy = object
                closest_dist = dist
            # 计算此对象与player之间的距离
    return closest_enemy


def target_tile(max_range = None):
    # 增加鼠标与界面的互动
    # 返回在玩家的FOV中左键点击的 tile 的位置的值（可选地在一个范围内），或者如果右键单击，则返回（None，None）。
    global key, mouse
    while True: # 渲染屏幕。这将显示鼠标下对象的名称。
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
        render_all()

        (x, y) = (mouse.cx, mouse.cy)

        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return(None, None)
            # 定义右键单击和Escape键作为取消键

        if (mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, x, y) and
            (max_range is None or player.distance(x, y) <= max_range)):
            return (x, y)


def target_monster(max_range = None):
    while True:
        (x, y) = target_tile(max_range)
        if x is None:
            return None

        for obj in objects:
            if obj.x == x and obj.y == y and obj.fighter and obj != player:
                return obj

def new_game():
    global player, inventory, game_msgs, game_state, dungeon_level

    fighter_component = Fighter(hp = 100, defense = 3, power = 5, xp = 0, death_function = player_death)

    player = Object(0, 0, '@', 'player', libtcod.white, blocks = True, fighter = fighter_component)

    player.level = 1

    game_msgs = []
    # 创建游戏消息列表及其颜色，开始为空

    inventory = []

    dungeon_level = 1
    make_map()
    initialize_fov()

    game_state = 'playing'

    message('Welcome stranger! Prepare to death in the Tombs of Ancient Kings.', libtcod.red)
    pass

def initialize_fov():
    global fov_recompute, fov_map
    fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    # libtcod FOV模块需要知道哪些 title 可见
    # 所以,我们创建一个libtcod可以理解的地图（fov_map）
    # 并使用 tile 自己的 block_sight 和 blocked 属性中的适当值来填充它们
    # 实际上，只有 block_sight 会被使用; blocked 的值与FOV完全无关！(汗(lll￢ω￢))
    # 它只对寻路模块(pathfinding module)有用，但是无论如何不会提供这个值。
    # 另外，libtcod要求的值与我们定义的值相反，所以我们用not操作符来切换它们。

    fov_recompute = True

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

    libtcod.console_clear(con)

def check_level_up():# 检查玩家的经验是否足以升级
    level_up_xp = LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR
    if player.fighter.xp >= level_up_xp:
        player.level += 1
        player.fighter.xp -= level_up_xp
        message('Your battle skills grow stronger! You reached level ' + str(player.level) + '!', libtcod.yellow)

        choice = None
        while choice == None:
            choice = menu('Level up! Choose a stat to raise:\n',
                ['Constitution (+ 20 HP, from' + str(player.fighter.max_hp) + ')',
                'Strength(+1 attack, from' + str(player.fighter.power) + ')',
                'Agility (+1 defense, from' + str(player.fighter.defense) + ')' ], LEVEL_SCREEN_WIDTH)

        if choice == 0:
            player.fighter.max_hp += 20
            player.fighter.hp += 20
        elif choice == 1:
            player.fighter.power += 1
        elif choice == 2:
            player.fighter.defense += 1

def next_level():
    global dungeon_level
    message('You take a moment to rest, and recover your strength', libtcod.light_violet)
    player.fighter.heal(player.fighter.max_hp / 2)

    dungeon_level += 1
    message('After a rare moment of peace, you descend deeper into the heart of the dungeon...', libtcod.red)
    make_map()
    initialize_fov()

def play_game():
    global key, mouse

    player_action = None

    mouse = libtcod.Mouse()
    key = libtcod.Key()
    # 鼠标界面

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key,mouse)
        render_all()
        # 调用 render_all() 函数

        libtcod.console_flush()
        # 刷新

        check_level_up()

        for object in objects:
            object.clear()

        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break

        if game_state == 'playing' and player_action != 'didnt-take-turn':
            for object in objects:
                if object.ai:
                    object.ai.take_turn()

def save_game():
    file = shelve.open('savegame', 'n')
    file['map'] = map
    file['objects'] = objects
    file['player_index'] = objects.index(player)
    file['inventory'] = inventory
    file['game_msgs'] = game_msgs
    file['game_state'] = game_state
    file['stairs_index'] = object.index(stairs)
    file['dungeon_level'] = dungeon_level
    file.close()

def load_game():
    global map, Object, player, inventory, game_msgs, game_state, dungeon_level

    file = shelve.open('savegame', 'r')
    map = file['map']
    objects = file['objects']
    player = objects[file['player_index']]
    inventory = file['inventory']
    game_msgs = file['game_msgs']
    game_state = file['game_state']
    starts = objects[file['starts_index']]
    dungeon_level = file['dungeon_level']
    file.close()

    initialize_fov()


def menu(header, options, width):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height
    # 计算页眉 (自动换行后) 和每选项一行的总高度

    window = libtcod.console_new(width, height)
    # 创建表示菜单窗口的控制台

    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
    # 打印 header, 自动换行

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '('+ chr(letter_index) +')' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text) # 显示库存里的项目
        y += 1
        letter_index += 1
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

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


    index = key.c - ord('a')
    if index >= 0 and index < len(options):return index
    return None
    # 通过减去字母 a 的 ASCLL 码
    # 得到的关键代码从0到25对应的字母 A 到 z
    # 任何超出该范围意味着它不是一个有效的值

def main_menu():
    img = libtcod.image_load('menu_background1.png')
    while not libtcod.console_is_window_closed():
        libtcod.image_blit_2x(img, 0, 0, 0)
        # 显示背景图像，为常规控制台分辨率的两倍

        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER, 'TOMBS OF THE ANCIENT KINGS')
        libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER, 'by COOSK-KUNKUN')

        choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)
        # 显示选项并等待玩家的选择
        if choice == 0:
            new_game()
            play_game()

        if choice == 1:
            try:
                load_game()
            except:
                msgbox('\n No saved game to load.\n', 24)
                continue
            play_game()

        elif choice == 2:
            break

def msgbox(text, width = 50):
    menu(text, [], width)
    # 使用 menu() 作为一种“消息框”



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

main_menu()