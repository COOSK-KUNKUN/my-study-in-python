# -*- coding: UTF-8 -*-

import libtcodpy as libtcod
import math
import textwrap
import shelve

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 55

LIMIT_FPS = 100

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
# 房间最大的数量

'''
color_dark_wall = libtcod.Color(0, 0, 100) # 视野外的墙壁颜色
color_light_wall = libtcod.Color(130, 110, 50) #视野内的墙壁颜色
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)
'''

color_dark_wall = libtcod.Color(130, 110, 50) * libtcod.dark_grey * 0.4
color_dark_wall2 = libtcod.light_orange * libtcod.dark_grey * 0.2
color_dark_wall3 = libtcod.chartreuse * libtcod.dark_grey * 0.5
color_light_wall = libtcod.Color(130, 110, 50)
color_light_wall2 = libtcod.light_orange * 0.3
color_light_wall3 = libtcod.light_chartreuse * 0.3

color_dark_ground = libtcod.Color(200, 180, 50) * libtcod.dark_grey * 0.5
color_dark_ground2 = libtcod.orange * 0.2
color_dark_ground3 = libtcod.chartreuse * 0.4
color_light_ground = libtcod.Color(200, 180, 50)
color_light_ground2 = libtcod.orange * 0.9
color_light_ground3 = libtcod.chartreuse * 0.9

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

HEAL_AMOUNT = 40

LIGHTNING_DAMAGE = 40 # 闪电法术伤害数值
LIGHTNING_RANGE = 5

CONFUSE_RANGE = 8     # 迷惑法术
CONFUSE_NUM_TURNS = 10

FIREBALL_RADIUS = 3   # 火球法术伤害数值
FIREBALL_DAMAGE = 25

LEVEL_SCREEN_WIDTH = 40
LEVEL_UP_BASE = 200
LEVEL_UP_FACTOR = 150
# 经验值

CHARACTER_SCREEN_WIDTH = 30
GRENADE_DAMAGE = 200

class Tile:
    # 设定能否通过的区域
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False
        # 战争之雾 a.k.a Fog of War （其实就是视野啦）
        # 表示探索过的地区将会以阴影颜色显示

        # 默认情况下，如果 tiel 被挡住，也会阻止视线
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Rect:
    # 用于生成整个地牢的构建模块
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    # 创建矩形房间的框架
    # 左上角（x1，y1）和右下角（x2，y2）

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
    # 创建一个返回 room 中心坐标的方法

    def intersect(self, other):
        #如果此矩形与另一个矩形相交，则返回true
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
    # 分割 room 之间的距离使之不重叠

class Object:
    """这是一个通用的对象：玩家，怪物，物品，楼梯......  """
    def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, fighter=None, ai=None, item=None, equipment=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.always_visible = always_visible # 允许一些对象始终可见
        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

            #这里是个必备 Item 组件，以便 Equipment 组件正常工作
            self.item = Item()
            self.item.owner = self

    def move(self, dx, dy):
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        # 算出从此对象（怪物）到目标（玩家）的距离
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #将其标准化为长度1（保留方向），然后将其四舍五入并转换为整数，以便将运动限制为地图网格
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        # 返回到另一个对象的距离
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        # 返回坐标的距离
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def send_to_back(self):
        # 首先绘制此对象，如果它们位于同一个图块中，则所有其他对象都显示在其上方。
        global objects
        objects.remove(self)
        objects.insert(0, self)

    def draw(self):
        #仅显示 玩家 是否可见; 或者它被设置为“始终可见”并且在经过探索的 tile 上
        if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or
                (self.always_visible and map[self.x][self.y].explored)):
            #设置颜色，然后在其位置绘制表示此对象的字符
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        # 擦除表示此对象的字符
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

class Fighter:
    """与战斗有关的属性和方法（怪物， 玩家， NPC）"""
    def __init__(self, hp, defense, power, xp, death_function=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.death_function = death_function

    @property # 简单地在装备物品时将 bonus value 添加到统计数据（例如，攻击力）
    def power(self):  # 返回装备物品的 power 数值
        bonus = sum(equipment.power_bonus for equipment in get_all_equipped(self.owner))
        return self.base_power + bonus

    @property
    def defense(self):  #返回装备物品的 defense 数值
        bonus = sum(equipment.defense_bonus for equipment in get_all_equipped(self.owner))
        return self.base_defense + bonus

    @property
    def max_hp(self):  #返回装备物品的 base_max_hp 数值
        bonus = sum(equipment.max_hp_bonus for equipment in get_all_equipped(self.owner))
        return self.base_max_hp + bonus
    # 用  @property 替代 get 和 set

    def attack(self, target):
        # 一个简单的计算攻击伤害公式
        damage = self.power - target.fighter.defense

        if damage > 0:
            # 使目标受到伤害的信息以消息 message  的方式打印出来
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
            target.fighter.take_damage(damage)
        else:
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

    def take_damage(self, damage):
        # 伤害以及损伤
        if damage > 0:
            self.hp -= damage

            # 检查目标是否死亡。如果是，调用死亡函数。
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner)

                if self.owner != player:  # 每次杀死怪物后给玩家加经验
                    player.fighter.xp += self.xp

    def heal(self, amount):
        #按给定的数值治愈，且不超过其最大值
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class BasicMonster:
    """基本怪物AI"""
    def take_turn(self):
        # 给予怪物基本的 FOV 和其在玩家 FOV 里的活动
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(player) >= 2: # 如果怪物距离玩家 >=2,就移动向玩家
                monster.move_towards(player.x, player.y)

            elif player.fighter.hp > 0:
                monster.fighter.attack(player)
                # 如果怪物距离玩家小于2,就攻击玩家，并判断玩家是否存活

class ConfusedMonster:
    """由闪电卷轴造成的混乱咒语 并让怪物恐惧(随机移动)"""
    def __init__(self, old_ai, num_turns=CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns
        # old_ai 用于临时混淆的怪物（在一段时间后恢复到之前的AI）

    def take_turn(self):
        if self.num_turns > 0:  # 仍然困惑......
            # 随机移动（随机X和Y位移在-1和1之间）
            self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1

        else:  # 恢复以前的AI（这个将被删除，因为它不再被引用）
            self.owner.ai = self.old_ai
            message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)

class Item:
    """可以拾取和使用的物品"""
    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        if len(inventory) >= 26: # 通过按下从A到Z的键来选择项目，并且只有26个字母
            message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
        else:
            inventory.append(self.owner)
            objects.remove(self.owner)
            message('You picked up a ' + self.owner.name + '!', libtcod.green)

            # 特殊情况：如果相应的设备插槽未使用，则自动装备
            equipment = self.owner.equipment
            if equipment and get_equipped_in_slot(equipment.slot) is None:
                equipment.equip()

    def drop(self):
        # 如果对象具有 Equipment 组件，则在删除之前将其取消
        if self.owner.equipment:
            self.owner.equipment.dequip()

        objects.append(self.owner)
        inventory.remove(self.owner)
        self.owner.x = player.x
        self.owner.y = player.y
        message('You dropped a ' + self.owner.name + '.', libtcod.yellow)
        # 添加到地图并从 player 的 inventory 中删除。 另外，将它放在玩家的坐标下

    def use(self):
        # 如果对象具有 Equipment 这个组件，则“use”动作是装备或者丢弃
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        # 如果已定义，则调用“use_function”
        if self.use_function is None:
            message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self.owner)
                # 使用后销毁, 除非被玩家取消
class Equipment:
    # 这是表示装备武器的方法
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus

        self.slot = slot
        self.is_equipped = False

    def toggle_equip(self):  # 装备与丢弃
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def equip(self):
        #装备武器时的信息
        # 如果插槽已经被使用，请首先解除其中的任何内容
        old_equipment = get_equipped_in_slot(self.slot)
        if old_equipment is not None:
            old_equipment.dequip()
        # 防止同一个插槽中有两个项目，取消旧项目以为新项目腾出空间。

        #装备对象并显示有关它的消息
        self.is_equipped = True
        message('Equipped ' + self.owner.name + ' on ' + self.slot + '.', libtcod.light_green)

    def dequip(self):
        # 丢弃装备的信息
        if not self.is_equipped: return
        self.is_equipped = False
        message('Dequipped ' + self.owner.name + ' from ' + self.slot + '.', libtcod.light_yellow)

def get_equipped_in_slot(slot):  # 将设备返回到插槽中，如果设备为空，则返回None
    for obj in inventory:
        if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
            return obj.equipment
    return None

def get_all_equipped(obj):  # 返回配备项目列表
    if obj == player:
        equipped_list = []
        for item in inventory:
            if item.equipment and item.equipment.is_equipped:
                equipped_list.append(item.equipment)
                # 如果他们的插槽可用，则自动装备拾取的物品

        return equipped_list
    else:
        return []

def is_blocked(x, y):
    # 测试 map 中的 tile 是否堵塞
    if map[x][y].blocked:
        return True

    # 检查任何堵塞的 objects
    for object in objects:
        if object.blocks and object.x == x and object.y == y:
            return True

    return False

def create_room(room):
    global map

    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False
    # room.x2/y2 + 1 使 room 彼此不相邻且总有一道墙隔开

def create_h_tunnel(x1, x2, y):
    global map
    # 水平隧道。 在x1> x2的情况下使用min（）和max（）
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    global map
    # 垂直隧道
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def make_map():
    global map, objects, stairs

    objects = [player]

    map = [[ Tile(True)
             for y in range(MAP_HEIGHT) ]
           for x in range(MAP_WIDTH) ]
    # 当 tile(false) 时 不会显示 room

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
                # 创建一个 room 看他是否重叠或相交其他 room

        if not failed:
            # 如果没有重叠或相交，则这个 room 是有效的
            create_room(new_room)

            (new_x, new_y) = new_room.center()
            # 新房间的中心坐标，以后会有用

            if num_rooms == 0:

                player.x = new_x
                player.y = new_y
                # 当玩家第一次所在的位置时，这将是第一个 room
            else:
                # 在第一个房间后的所有房间
                # 用隧道将它连接到先前的房间

                (prev_x, prev_y) = rooms[num_rooms-1].center()
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

            # 添加一些内容到这个房间，如怪物
            place_objects(new_room)

            rooms.append(new_room)
            num_rooms += 1
            # 将新房间添加到列表中

    stairs = Object(new_x, new_y, 's', 'stairs', libtcod.white, always_visible=True)
    objects.append(stairs)
    stairs.send_to_back()  # 所以它被绘制在怪物下面
    # 在房间的中心创建向下的楼梯

def random_choice_index(chances):  #从 chances 列表中选择一个选项，返回其索引
    #骰子将落在1和1之间的数字之间
    dice = libtcod.random_get_int(0, 1, sum(chances))
    # sum(chances) 接受一个数字列表并返回它们的总和

    #  遍历所有 chances ，保持其 sum
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        #看看骰子是否落在与此选择相对应的部分
        if dice <= running_sum:
            return choice
        choice += 1

def random_choice(chances_dict):
    #从 chances_dict 中选择一个选项，并返回其关键词
    chances = chances_dict.values()
    strings = chances_dict.keys()

    return strings[random_choice_index(chances)]

def from_dungeon_level(table):
    #返回一个等级的值。该函数指定每个级别后出现的值，默认值为0.
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value
    return 0

def place_objects(room):
    #这是决定每个怪物或物品出现的机会方法。

    #每个房间最多的怪物数量
    max_monsters = from_dungeon_level([[2, 1], [3, 4], [5, 6]])

    #每个怪物出现的概率以及等级
    monster_chances = {}
    monster_chances['orc'] = 80  # 80%
    monster_chances['troll'] = from_dungeon_level([[15, 3], [30, 5], [60, 7]])

    #每间 room 的最大物品数量
    max_items = from_dungeon_level([[1, 1], [2, 4]])

    #每个物品出现的概率(默认情况下，它们在第一层的时候只有0%的机会，然后上升)
    item_chances = {}
    item_chances['heal'] = 35  #35%
    item_chances['lightning'] = from_dungeon_level([[25, 4]])
    item_chances['fireball'] =  from_dungeon_level([[25, 6]])
    item_chances['confuse'] =   from_dungeon_level([[10, 2]])
    item_chances['sword'] =     from_dungeon_level([[5, 4]])
    item_chances['shield'] =    from_dungeon_level([[15, 8]])
    item_chances['holy hand grenade'] =  from_dungeon_level([[25, 6]])

    # 选择随机数量的怪物
    num_monsters = libtcod.random_get_int(0, 0, max_monsters)

    for i in range(num_monsters):
        # 为这个怪物选择随机点
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        # 只有在 tile 未被阻挡时才放置它
        if not is_blocked(x, y):
            choice = random_choice(monster_chances)
            if choice == 'orc':
                # 创建兽人
                fighter_component = Fighter(hp=20, defense=0, power=4, xp=35, death_function=monster_death)
                ai_component = BasicMonster()

                monster = Object(x, y, 'o', 'orc', libtcod.desaturated_green,
                                 blocks=True, fighter=fighter_component, ai=ai_component)

            elif choice == 'troll':
                # 创建巨魔
                fighter_component = Fighter(hp=30, defense=2, power=8, xp=100, death_function=monster_death)
                ai_component = BasicMonster()

                monster = Object(x, y, 'T', 'troll', libtcod.darker_green,
                                 blocks=True, fighter=fighter_component, ai=ai_component)

            objects.append(monster)

    # 选择随机数量的项目
    num_items = libtcod.random_get_int(0, 0, max_items)

    for i in range(num_items):
        # 为这个项目选择随机点
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        # 只有在 tile 未被阻挡时才放置它
        if not is_blocked(x, y):
            choice = random_choice(item_chances)
            if choice == 'heal':
                #c 创建治疗药水
                item_component = Item(use_function=cast_heal)
                item = Object(x, y, '!', 'healing potion', libtcod.violet, item=item_component)

            elif choice == 'lightning':
                # 创建一个闪电卷轴
                item_component = Item(use_function=cast_lightning)
                item = Object(x, y, '#', 'scroll of lightning bolt', libtcod.light_yellow, item=item_component)

            elif choice == 'fireball':
                # 创建一个火球卷轴
                item_component = Item(use_function=cast_fireball)
                item = Object(x, y, '#', 'scroll of fireball', libtcod.light_yellow, item=item_component)

            elif choice == 'confuse':
                # 创建一个混乱卷轴
                item_component = Item(use_function=cast_confuse)
                item = Object(x, y, '#', 'scroll of confusion', libtcod.light_yellow, item=item_component)

            elif choice == 'sword':
                # 创建一把剑
                equipment_component = Equipment(slot='right hand', power_bonus=3)
                item = Object(x, y, '/', 'sword', libtcod.sky, equipment=equipment_component)

            elif choice == 'shield':
                # 创建一个盾牌
                equipment_component = Equipment(slot='left hand', defense_bonus=1)
                item = Object(x, y, '[', 'shield', libtcod.darker_orange, equipment=equipment_component)

            elif choice == 'holy hand grenade':
                #创建神圣手雷
                item_component = Item(use_function=cast_grenade)
                item = Object(x, y, 'O', 'Holy Hand Grenade', libtcod.darkest_grey, item=item_component)

            objects.append(item)
            item.send_to_back()  # items 显示在其他对象下方
            item.always_visible = True  #  如果在探索区域内，即使在FOV之外也可以看到物品


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # 渲染状态栏（血量， 经验等 ），但首先计算状态栏的宽度
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    # 渲染后台

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
    # 现在将条形图呈现在顶部


    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
                                 name + ': ' + str(value) + '/' + str(maximum))
    # 一些带有值的居中文本

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

def render_all(): # 绘制列表中的所有对象
    global fov_map, color_dark_wall, color_dark_wall2,  color_light_wall
    global color_dark_ground, color_light_ground, color_light_wall2, color_dark_ground2
    global color_light_ground2
    global fov_recompute

    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
    # 改变渲染代码来实际重新计算FOV，并显示结果！
    # 只需要重新计算FOV，并在recompute_fov为True的情况下渲染地图（然后我们将其重置为False）

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight
                if not visible:
                    # 如果它现在不可见，那么玩家只能在探索的时候才可见 （视野）
                    if map[x][y].explored:
                        if wall and dungeon_level % 2 == 0:
                            libtcod.console_set_char_background(
                            con, x, y, color_dark_wall, libtcod.BKGND_SET)
                        elif wall and dungeon_level % 3 == 0:
                            libtcod.console_set_char_background(
                            con, x, y, color_dark_wall3, libtcod.BKGND_SET)
                        elif wall:
                            libtcod.console_set_char_background(
                            con, x, y, color_dark_wall2, libtcod.BKGND_SET)
                        elif dungeon_level % 2 == 0:
                            libtcod.console_set_char_background(
                            con, x, y, color_dark_ground, libtcod.BKGND_SET)
                        elif dungeon_level % 3 == 0:
                            libtcod.console_set_char_background(
                            con, x, y, color_dark_ground3, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(
                            con, x, y, color_dark_ground2, libtcod.BKGND_SET)
                else:
                    # 它是可见的
                    if wall and dungeon_level % 2 == 0:
                        libtcod.console_set_char_background(
                        con, x, y, color_light_wall, libtcod.BKGND_SET )
                    elif wall and dungeon_level % 3 == 0:
                        libtcod.console_set_char_background(
                        con, x, y, color_light_wall3, libtcod.BKGND_SET )
                    elif wall:
                        libtcod.console_set_char_background(
                        con, x, y, color_light_wall2, libtcod.BKGND_SET )
                    elif dungeon_level % 2 == 0:
                        libtcod.console_set_char_background(
                        con, x, y, color_light_ground, libtcod.BKGND_SET )
                    elif dungeon_level % 3 == 0:
                        libtcod.console_set_char_background(
                        con, x, y, color_light_ground3, libtcod.BKGND_SET )
                    else:
                        libtcod.console_set_char_background(
                        con, x, y, color_light_ground2, libtcod.BKGND_SET )
                        # 既然它是可见的，那么就可以探索它
                    map[x][y].explored = True

    for object in objects:
        if object != player:
            object.draw()
    player.draw()
    # 防止怪物尸体与角色重叠，造成无法渲染
    # 绘制列表中的所有对象，但除了 player 外。 它总是出现在所有其他对象上！ 所以它稍后绘制。

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
    # 将“面板”的内容提交到根控制台

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    # 渲染GUI面板

    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT,line)
        y += 1
    # 将状态栏渲染出来
    # 打印游戏消息，一次一行

    # 显示玩家的统计数据
    render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    render_bar(1, 2, BAR_WIDTH, 'XP', player.fighter.xp, LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR,
               libtcod.darker_green, libtcod.darker_gray)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level ' + str(dungeon_level))

    # 显示鼠标下的对象名称
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())

    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

def message(new_msg, color = libtcod.white):
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]
        # 如果消息超出消息的最大高度，就删除第一行以腾出空间给新的一个

        game_msgs.append((line, color))
        # 将新行添加为元组，文本和颜色

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
        # 如果发现目标攻击并移动

def menu(header, options, width):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    #计算标题的总高度（且自动换行后）和每选项一行的总高度
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height
 
    #创建表示菜单窗口的控制台
    window = libtcod.console_new(width, height)
 
    # 打印 header, 自动换行
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
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

    # 等待玩家做出选择，游戏才能继续
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:  #(special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen)

    index = key.c - ord('a')
    if index >= 0 and index < len(options): return index
    return None
    # 通过减去字母 a 的 ASCLL 码
    # 得到的关键代码从0到25对应的字母 A 到 z
    # 任何超出该范围意味着它不是一个有效的值

def inventory_menu(header):
    # 显示库存
    # 将 menu 中每个项目的 item 显示为选项

    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in inventory:
            text = item.name
            # 显示装备信息
            if item.equipment and item.equipment.is_equipped:
                text = text + ' (on ' + item.equipment.slot + ')'
            options.append(text)

    index = menu(header, options, INVENTORY_WIDTH)


    if index is None or len(inventory) == 0: return None
    return inventory[index].item
    # 如果选择了某个 item，请将其退回

def msgbox(text, width=50):
    menu(text, [], width)  #使用 menu（）作为一种“消息框”

def story():
    global race
    if race == 'Human':
        msgbox('You are a young adventurer who has entered THE UNDERDEEP\n\n'+
               'This cave has had many '+
               'horrible stories told about it around the campfires at night,'+
               ' but also stories of the amulet of the King, which '+
               'could give great power to the wearer.'+
               '\n\nYou, being a brave explorer, grab your trusty dagger '+
               'and descend into the cave to find out what is really' +
                ' hiding in the dark shadows of the deep.\n\n'+
               'Use your wits to gather items to explore the depths of the '+
               'cave.  Be warned, though, that many perils await you.')
                # 你是个年轻的冒险家正在进入这些洞穴，有个可怕的故事夜晚在的营火中讲述了，关于王的护身符的故事
                # 它可以给佩戴者很大的力量。你，勇敢的探险家，拿着你那可靠的匕首然后下山到山洞里去看看到底是什么
                # 藏在深邃的黑暗中。“用你的智慧收集物品来探索洞穴。不过，请注意，许多危险都在等着你。

    elif race == 'Elf':
        msgbox('An elf is a mythical creature that appears to be human in nature '+
               'but has magical powers and does not age (or at least ages very slowly)\n\n'+
               'The elves are seen as a luminous group of people who are known to have fair '+
               'complexions far more perfect than even the most beautiful human features.'+
               'They are sometimes known as the white people.\n\n' +
               'You pick up your trusty dagger '+
               'vowing to recover the amulet of the King\n' +
               '...and return your people to their former glory.')
                # 精灵是一种神话中的生物，似乎是人类的天性，但具有神奇的力量，并且不会衰老（或者至少非常缓慢地衰老）
                # 精灵被视为一群“光明”的人，他们的公平肤色远比最美丽的人类特征更完美。他们有时被称为“白人”。
                # 你拿起一把匕首，发誓要找回王的护身符，让你们的人民回到从前的荣耀中。

    elif race == 'Dwarf':
        msgbox('The UNDERDEEP, once home to the dwarvish people '+
               'has fallen under the spell of Malfuriul the Vast One\n\n'+
               'You pick up the dagger of your grandfather, Norat Longbeard '+
               ',and vow to reclaim the amulet of the flying circus to '+
               'cleanse the evil from your ancestral home.')
                # 曾经是矮人的国家是非常弱小的。它被已被大法师玛法里奥的咒语所迷惑。
                # 你拿起你祖父的匕首，诺拉特朗比尔德，并发誓要夺回王的护身符，并你的国中除掉邪恶。


def handle_keys(): # 控制键位与角色行走
    global key, race

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt + Enter: 全屏

        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  # 按下 ESC 则 exit game

    if game_state == 'playing':
        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            player_move_or_attack(0, -1)
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            player_move_or_attack(0, 1)
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            player_move_or_attack(-1, 0)
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            player_move_or_attack(1, 0)
        elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
            player_move_or_attack(-1, -1)
        elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
            player_move_or_attack(1, -1)
        elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
            player_move_or_attack(-1, 1)
        elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
            player_move_or_attack(1, 1)
        elif key.vk == libtcod.KEY_KP5:
            pass  # 等待
        else:
            #test for other keys
            key_char = chr(key.c)

            if key_char == 'g':
                # 拿起一件物品
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
                # 丢弃
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()

            if key_char == 'c':
                # 显示角色信息
                level_up_xp = LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR
                msgbox('Character Information\n\nLevel: ' + str(player.level) + '\nExperience: ' + str(player.fighter.xp) +
                       '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(player.fighter.max_hp) +
                       '\nAttack: ' + str(player.fighter.power) + '\nDefense: ' + str(player.fighter.defense), CHARACTER_SCREEN_WIDTH)

            if key_char == 's':
                # 下楼梯
                if stairs.x == player.x and stairs.y == player.y:
                    next_level()

            if key_char == 'q':
                story()
                # 各个种族的描述

            return 'didnt-take-turn'

def check_level_up(): # 检查玩家的经验是否足以升级
    level_up_xp = LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR
    if player.fighter.xp >= level_up_xp:
        player.level += 1
        player.fighter.xp -= level_up_xp
        message('Your battle skills grow stronger! You reached level ' + str(player.level) + '!', libtcod.yellow)

        choice = None
        while choice == None:  # 继续询问，直到做出选择
            choice = menu('Level up! Choose a stat to raise:\n',
                          ['Constitution (+20 HP, from ' + str(player.fighter.max_hp) + ')',
                           'Strength (+1 attack, from ' + str(player.fighter.power) + ')',
                           'Agility (+1 defense, from ' + str(player.fighter.defense) + ')'], LEVEL_SCREEN_WIDTH)

        if choice == 0:
            player.fighter.base_max_hp += 20
            player.fighter.hp += 20
        elif choice == 1:
            player.fighter.base_power += 1
        elif choice == 2:
            player.fighter.base_defense += 1

def player_death(player):
    # game over
    global game_state
    message('You died!', libtcod.red)
    game_state = 'dead'

    # 增加效果，将玩家变成尸体
    player.char = '%'
    player.color = libtcod.dark_red
1
def monster_death(monster):
    # 将怪物变成尸体，但它的尸体不能造成道路堵塞（block）
    # 变成尸体时不能移动,关闭ai
    message('The ' + monster.name + ' is dead! You gain ' + str(monster.fighter.xp) + ' experience points.', libtcod.orange)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()

def target_tile(max_range=None):
    # 增加鼠标与界面的互动
    # 返回在玩家的FOV中左键点击的 tile 的位置的值（可选地在一个范围内），或者如果右键单击，则返回（None，None）。
    global key, mouse
    while True: # 渲染屏幕。这将显示鼠标下对象的名称。
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        render_all()

        (x, y) = (mouse.cx, mouse.cy)

        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return (None, None) 
            # 定义右键单击和Escape键作为取消键

        if (mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, x, y) and
                (max_range is None or player.distance(x, y) <= max_range)):
            return (x, y)
            # 如果玩家在FOV中单击，则显示目标信息，如果指定了范围，则检测是否在该范围内

def target_monster(max_range=None):
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  # 取消
            return None

        #返回第一个单击的怪物的信息
        for obj in objects:
            if obj.x == x and obj.y == y and obj.fighter and obj != player:
                return obj

def closest_monster(max_range):
    # 找到最近的敌人，达到最大范围，并且在玩家的FOV里
    closest_enemy = None
    closest_dist = max_range + 1  #以（略大于）最大范围开始

    for object in objects:
        if object.fighter and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
            #计算此对象与player之间的距离
            dist = player.distance_to(object)
            if dist < closest_dist:
                closest_enemy = object
                closest_dist = dist
    return closest_enemy

def cast_grenade():
    global player
    # 向玩家询问目标，以便向其投掷，其实方法与火球术类似。
    message('Left-click a target tile for the Holy Hand Grenade, or right-click to cancel.', libtcod.light_cyan)
    (x, y) = target_tile()
    if x is None: return 'cancelled'
    message('The Holy Hand Grenade demolishes everything!'+ str(FIREBALL_RADIUS) + ' tiles!', libtcod.orange)

    for obj in objects:  # 损坏范围内的所有物品，包括玩家
        if obj != player:
            if obj.distance(x, y) <= FIREBALL_RADIUS and obj.fighter:
                message('The ' + obj.name + ' vaporizes for ' + str(GRENADE_DAMAGE) + ' hit points.', libtcod.orange)
                obj.fighter.take_damage(GRENADE_DAMAGE)


def cast_heal():
    if player.fighter.hp == player.fighter.max_hp:
        message('You are already at full health.', libtcod.red)
        return 'cancelled'

    message('Your wounds start to feel better!', libtcod.light_violet)
    player.fighter.heal(HEAL_AMOUNT)

def cast_lightning():
    # 找到最近的敌人（在最大范围内）并对其造成伤害
    monster = closest_monster(LIGHTNING_RANGE)
    if monster is None:  # 如果在最大范围内没有发现敌人
        message('No enemy is close enough to strike.', libtcod.red)
        return 'cancelled'

    message('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is '
            + str(LIGHTNING_DAMAGE) + ' hit points.', libtcod.light_blue)
    monster.fighter.take_damage(LIGHTNING_DAMAGE)

def cast_fireball():
    #要求玩家单击鼠标完成在目标牌上投掷火球的动作
    message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan)
    (x, y) = target_tile()
    if x is None: return 'cancelled'
    message('The fireball explodes, burning everything within ' + str(FIREBALL_RADIUS) + ' tiles!', libtcod.orange)

    for obj in objects:  # 损坏范围内的所有目标，包括玩家
        if obj.distance(x, y) <= FIREBALL_RADIUS and obj.fighter:
            message('The ' + obj.name + ' gets burned for ' + str(FIREBALL_DAMAGE) + ' hit points.', libtcod.orange)
            obj.fighter.take_damage(FIREBALL_DAMAGE)

def cast_confuse():
    # 询问玩家要让哪一个目标受到 confuse
    message('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)
    monster = target_monster(CONFUSE_RANGE)
    if monster is None: return 'cancelled'

    # 将怪物的AI换成“困惑”的AI; 经过一段时间后，它会恢复旧的AI
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster
    message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', libtcod.light_green)



def save_game():
    file = shelve.open('savegame', 'n')
    file['map'] = map
    file['objects'] = objects
    file['player_index'] = objects.index(player)
    file['stairs_index'] = objects.index(stairs)
    file['inventory'] = inventory
    file['game_msgs'] = game_msgs
    file['game_state'] = game_state
    file['dungeon_level'] = dungeon_level
    file['race'] = race
    file.close()

def load_game():
    global map, objects, player, stairs, inventory, game_msgs, game_state, dungeon_level, race

    file = shelve.open('savegame', 'r')
    map = file['map']
    objects = file['objects']
    player = objects[file['player_index']]
    stairs = objects[file['stairs_index']]
    inventory = file['inventory']
    game_msgs = file['game_msgs']
    game_state = file['game_state']
    dungeon_level = file['dungeon_level']
    race = file['race']
    file.close()

    initialize_fov()

def new_game():
    global player, inventory, game_msgs, game_state, dungeon_level

    if race == 'Human':
        fighter_component = Fighter(hp=1000, defense=1, power=3, xp=0, death_function=player_death)
    elif race == 'Dwarf':
        fighter_component = Fighter(hp=1200, defense=1, power=2, xp=0, death_function=player_death)
    elif race == 'Elf':
        fighter_component = Fighter(hp=1000, defense=2, power=2, xp=0, death_function=player_death)

    # 创建代表玩家的对象
    # fighter_component = Fighter(hp=100, defense=3, power=3, xp=0, death_function=player_death)
    player = Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component)

    player.level = 1

    # 生成地图
    dungeon_level = 1
    make_map()
    initialize_fov()

    game_state = 'playing'
    inventory = []

    game_msgs = []
    # 创建游戏消息列表及其颜色，开始为空

    message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)

    # 初始装备：匕首
    equipment_component = Equipment(slot='right hand', power_bonus=2)
    obj = Object(0, 0, '-', 'dagger', libtcod.sky, equipment=equipment_component)
    inventory.append(obj)
    equipment_component.equip()
    obj.always_visible = True

def next_level():
    global dungeon_level
    message('You take a moment to rest, and recover your strength.', libtcod.light_violet)
    player.fighter.heal(player.fighter.max_hp / 2)  # 恢复50%的血量

    dungeon_level += 1
    message('After a rare moment of peace, you descend deeper into the heart of the dungeon...', libtcod.red)
    make_map()
    initialize_fov()

def initialize_fov():
    global fov_recompute, fov_map
    fov_recompute = True

    # 根据生成的地图创建 FOV
    fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

    libtcod.console_clear(con)  #未探测区域开始黑色（这是默认的背景颜色）

def play_game():
    global key, mouse

    player_action = None

    mouse = libtcod.Mouse()
    key = libtcod.Key()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        render_all()

        libtcod.console_flush()

        check_level_up()

        # 在移动之前擦除旧位置的所有对象
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

def main_menu():
    img = libtcod.image_load('menu_background1.png')

    while not libtcod.console_is_window_closed():
        # 以分辨率的两倍显示背景图像
        libtcod.image_blit_2x(img, 0, 0, 0)

        # 显示游戏的标题，以及一些积分！
        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER,
                                 'TOMBS OF THE ANCIENT KINGS')
        libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER, 'By COOSK-KUNKUN')

        # 显示选项并等待玩家的选择
        choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  #new game
            # new_game()
            # play_game()
            race_menu()
        if choice == 1:  #load last game
            try:
                load_game()
            except:
                msgbox('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:  #quit
            break

def race_menu():
    global race
    race_choice = None
    # 角色种族选择的菜单
    img = libtcod.image_load('menu_background1.png')
    libtcod.image_blit_2x(img, 0, 0, 0)
    msgbox("What is your want to be?\n" +
               "Press ENTER to Continue")
    libtcod.console_wait_for_keypress(True)
    libtcod.image_blit_2x(img, 0, 0, 0)
    while race_choice == None: # 一直询问直到做出选择
            race_choice = menu('Choose Your Race:\n',
                          ['Human hp=1000, defense=1, power=3,',
                           'Elf   hp=1200, defense=1, power=2',
                           'Dwarf hp=1000, defense=2, power=2',], LEVEL_SCREEN_WIDTH)
    if race_choice == 0:
        race = 'Human'
    elif race_choice == 1:
        race = 'Elf'
    elif race_choice == 2:
        race = 'Dwarf'
    new_game()
    play_game()

libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
# 设定字体
# 字体来源于 arial12x12.png 的位图字体

libtcod.console_init_root( SCREEN_WIDTH, SCREEN_HEIGHT, 'COOSK',False)
# 初始化窗口，最后一个参数告诉它是否应该是全屏。

libtcod.sys_set_fps(LIMIT_FPS)
# 限制游戏的速度 (帧每秒或FPS)

con = libtcod.console_new( SCREEN_WIDTH, SCREEN_WIDTH)
# 创建一个新的屏幕外控制台, 重要！！！！！dice = libtcod.random_get_int

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