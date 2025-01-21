import random

class RuleTable:
    def __init__(self, id, name):
        self.id = id  # 新增的編號屬性
        self.name = name
        self.main_rules = []  # 主規則列表
        self.sub_rules = []   # 副規則列表
        self.events = []      # 事件列表
        self.roles = []       # 身分列表
        self.special_rules = []  # 特殊規則列表

    def add_main_rule(self, rule):
        self.main_rules.append(rule)

    def add_sub_rule(self, rule):
        self.sub_rules.append(rule)

    def add_event(self, event):
        self.events.append(event)

    def add_role(self, role):
        self.roles.append(role)

    def add_special_rule(self, rule):
        self.special_rules.append(rule)
    
    def display_rules(self):
        print(f"規則表編號: {self.id}")
        print(f"名稱: {self.name}")
        print("主規則:")
        for index, rule in enumerate(self.main_rules, start=1):
            print(f"{index}. {rule.name}: {rule.description}")
        
        print("副規則:")
        for index, rule in enumerate(self.sub_rules, start=1):
            print(f"{index}. {rule.name}: {rule.description}")
        
        print("事件:")
        for index, event in enumerate(self.events, start=1):
            print(f"{index}. {event.name}")
        
        print("身分:")
        for index, role in enumerate(self.roles, start=1):
            print(f"{index}. {role.name}")
            for idx, ability in enumerate(role.abilities, start=1):
                print(f"  {idx}. {ability.name} ({ability.type}): {ability.description}")
        
        print("特殊規則:")
        for index, rule in enumerate(self.special_rules, start=1):
            print(f"{index}. {rule}")

class Event:
    def __init__(self, id, name, effect):
        self.id = id  # 新增的編號屬性
        self.name = name  # 事件名稱
        self.effect = effect  # 事件效果函數

class Role:
    def __init__(self, id, name, traits=None, abilities=None):
        self.id = id  # 新增的編號屬性
        self.name = name  # 身分名稱
        self.traits = traits if traits is not None else []  # 特性列表
        self.abilities = abilities if abilities is not None else []  # 能力列表

    def add_trait(self, trait):
        self.traits.append(trait)

    def add_ability(self, ability):
        self.abilities.append(ability)

class Rule:
    def __init__(self, id, name, description, roles, special_effect=None):
        self.id = id  # 新增的編號屬性
        self.name = name  # 規則名稱
        self.description = description  # 規則描述
        self.roles = roles  # 涉及的身分列表
        self.special_effect = special_effect  # 特殊效果函數

    def add_role(self, role):
        self.roles.append(role)

    def set_special_effect(self, effect):
        self.special_effect = effect

    def apply_special_effect(self, game):
        if self.special_effect:
            return self.special_effect(game)
        return False

class Ability:
    def __init__(self, name, type, description, effect):
        self.name = name  # 能力名稱
        self.type = type  # 能力類型 (主動 或 被動)
        self.description = description  # 能力描述
        self.effect = effect  # 能力效果函數

# 定義主要規則表 Basic Tragedy X
basic_tragedy_x = RuleTable(1, "Basic Tragedy X")

# 建立範例身分與能力
key_figure = Role(1, "關鍵人物")
key_figure.add_ability(Ability(
    "犧牲的代價", "被動", "此角色死亡時，輪迴直接結束，腳本家勝利",
    lambda character, game: game.script_writer.win_cycle() if character.is_dead else None
))

murderer = Role(2, "殺手")
murderer.add_trait("友好無視")
murderer.add_ability(Ability(
    "夜晚殺戮", "被動", "夜晚階段時，若與其他角色獨處，則殺害之",
    lambda character, game: (
        target.handle_death("事件 - 夜晚殺戮", game) if (target := character.current_area.get_random_character_except(character)) and character.current_area.is_night else None
    )
))
murderer.add_ability(Ability(
    "預謀殺害", "被動", "夜晚階段時，陰謀>3，腳本家勝利，輪迴結束",
    lambda character, game: (
        game.script_writer.win_cycle() if character.conspiracy > 3 else None
    )
))

mastermind = Role(3, "黑幕")
mastermind.add_trait("友好無視")
mastermind.add_ability(Ability(
    "陰謀操控", "主動", "同地區其他角色或地區+1陰謀",
    lambda character, script_writer: (
        target.add_conspiracy(1) if isinstance(target := script_writer.choose_target_or_area(character.current_area)) else target.add_conspiracy(1)
    )
))

cultist = Role(4, "邪教徒")
cultist.add_trait("友好無效")
cultist.add_ability(Ability(
    "無法遏止", "被動", "行動結算階段，取消此地區偵探設置的陰謀禁止卡片",
    lambda area, is_scriptwriter_view: (
        area.remove_conspiracy_ban()
    )
))

witch = Role(5, "魔女")
witch.add_trait("友好無效")

time_traveler = Role(6, "時間旅行者")
time_traveler.add_trait("無法被殺害")
time_traveler.add_ability(Ability(
    "拯救失敗", "被動", "最後一天夜晚階段，若友好值<2，腳本家勝利，輪迴結束",
    lambda character, game_state, is_scriptwriter_view: (
        game_state.end_loop("腳本家勝利")
        if game_state.current_day == game_state.final_day and character.friendship < 2 else None
    )
))

# 添加次要角色
friend = Role(7, "朋友")
friend.add_ability(Ability(
    "友誼破碎", "被動", "輪迴結束死亡時，腳本家勝利並公開身分",
    lambda character, game: game.script_writer.win_cycle() if character.is_dead else None
))

misleader = Role(8, "誤導者")
misleader.add_ability(Ability(
    "不安增加", "主動", "能力階段對同地區角色+1不安",
    lambda target, is_scriptwriter_view: (
        target.add_anxiety(1)
    )
))

lover = Role(9, "戀人")
lover.add_ability(Ability(
    "生離死別", "被動", "死亡時使情人+6不安",
    lambda partner, is_scriptwriter_view: (
        partner.add_anxiety(6)
    )
))

loved_one = Role(10, "情人")
loved_one.add_ability(Ability(
    "生離死別", "被動", "死亡時使戀人+6不安",
    lambda partner, is_scriptwriter_view: (
        partner.add_anxiety(6)
    )
))
loved_one.add_ability(Ability(
    "為愛痴狂", "被動", "夜晚階段若不安>3且陰謀值>0，腳本家勝利，輪迴結束",
    lambda character, game_state, is_scriptwriter_view: (
        game_state.end_loop("腳本家勝利")
        if character.anxiety > 3 and character.conspiracy > 0 else None       
    )
))
murderer_role = Role(11, "殺人魔")
murderer_role.add_ability(Ability(
    "夜晚殺戮", "被動", "夜晚階段時，若與其他角色獨處，則殺害之",
    lambda character, game: (
        target.handle_death("身分能力 - 夜晚殺戮", game) if (target := character.current_area.get_random_character_except(character)) and character.current_area.is_night else None
    )
))

factor_role = Role(12, "因子")
factor_role.add_trait("友好無視")
factor_role.add_ability(Ability(
    "不安增加·仿", "主動", "如果地區「都市」的陰謀數>1才能發動。能力階段對同地區角色+1不安",
    lambda target, is_scriptwriter_view: (
        target.add_anxiety(1),
        
        )
))
factor_role.add_ability(Ability(
    "犧牲的代價·仿", "被動", "此角色死亡時，如果地區「學校」的陰謀數>1，輪迴直接結束，腳本家勝利",
    lambda character, game: game.script_writer.win_cycle() if character.is_dead else None
    
    
))

# 添加角色到 Basic Tragedy X
basic_tragedy_x.add_role(key_figure)
basic_tragedy_x.add_role(murderer)
basic_tragedy_x.add_role(mastermind)
basic_tragedy_x.add_role(cultist)
basic_tragedy_x.add_role(witch)
basic_tragedy_x.add_role(time_traveler)
basic_tragedy_x.add_role(friend)
basic_tragedy_x.add_role(misleader)
basic_tragedy_x.add_role(lover)
basic_tragedy_x.add_role(loved_one)
basic_tragedy_x.add_role(murderer_role)
basic_tragedy_x.add_role(factor_role)

# 新增主要規則
additional_main_rules = [
    Rule(1, "殺人計畫", "關鍵人物*1、殺手*1、黑幕*1。", roles={"關鍵人物": 1, "殺手": 1, "黑幕": 1}),
    Rule(2, "被封印之物", "黑幕*1、邪教徒*1。輪迴結束時，如果神社陰謀>1，腳本家勝利", roles={"黑幕": 1, "邪教徒": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利")),
    Rule(3, "和我簽下契約吧！", "關鍵人物*1。輪迴結束時，若關鍵人物陰謀>1，腳本家勝利。關鍵人物必須為少女", roles={"關鍵人物": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利")),
    Rule(4, "未來改變作戰", "邪教徒*1，時間旅行者*1。蝴蝶效應事件發生後，該輪迴結束時腳本家勝利。", roles={"邪教徒": 1, "時間旅行者": 1}),
    Rule(5, "巨型定時炸彈", "魔女*1。輪迴結束時，若魔女的初期所在區域陰謀>1，腳本家勝利。", roles={"魔女": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利"))
]

# 新增副規則
additional_sub_rules = [
    Rule(6, "友情小圈圈", "朋友*2，誤導者*1", roles={"朋友": 2, "誤導者": 1}),
    Rule(7, "戀愛的模樣", "戀人*1，情人*1", roles={"戀人": 1, "情人": 1}),
    Rule(8, "殺人魔潛伏", "朋友*1，殺人魔*1", roles={"朋友": 1, "殺人魔": 1}),
    Rule(9, "人心惶惶", "每輪迴一次，腳本家可以在能力階段使任意地區+1陰謀。", roles={}, special_effect=lambda game_state: game_state.add_conspiracy_points_to_any_area()),
    Rule(10, "惡性譫妄病毒", "誤導者*1。本遊戲中，普通人不安>2時，變成殺人魔。", roles={"誤導者": 1}, special_effect=lambda game_state: game_state.transform_normal_to_murderer()),
    Rule(11, "因果之線", "輪迴重啟後，前一輪迴友好>0的角色+2不安。", roles={}, special_effect=lambda game_state: game_state.add_anxiety_to_characters_with_friendship_above(0, 2))
]

# 將這些規則添加到 Basic Tragedy X 中
for rule in additional_main_rules:
    basic_tragedy_x.add_main_rule(rule)

for rule in additional_sub_rules:
    basic_tragedy_x.add_sub_rule(rule)

# 複製 Basic Tragedy X 規則表，並給予不同的名稱和編號以便測試
def copy_rule_table(source, target):
    target.main_rules = source.main_rules[:]
    target.sub_rules = source.sub_rules[:]
    target.events = source.events[:]
    target.roles = source.roles[:]
    target.special_rules = source.special_rules[:]

basic_tragedy_y = RuleTable(2, "Basic Tragedy Y")
basic_tragedy_z = RuleTable(3, "Basic Tragedy Z")
basic_tragedy_w = RuleTable(4, "Basic Tragedy W")

copy_rule_table(basic_tragedy_x, basic_tragedy_y)
copy_rule_table(basic_tragedy_x, basic_tragedy_z)
copy_rule_table(basic_tragedy_x, basic_tragedy_w)

# 添加規則表到遊戲系統
all_rule_tables = {
    basic_tragedy_x.id: basic_tragedy_x,
    basic_tragedy_y.id: basic_tragedy_y,
    basic_tragedy_z.id: basic_tragedy_z,
    basic_tragedy_w.id: basic_tragedy_w,
}

def display_all_rule_tables():
    for rule_table in all_rule_tables.values():
        print(f"{rule_table.id}. {rule_table.name}")

def get_rule_table_by_id(rule_table_id):
    return all_rule_tables.get(rule_table_id, None)