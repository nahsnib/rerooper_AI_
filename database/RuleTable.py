# database/RuleTable.py

class RuleTable:
    def __init__(self, name):
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
        print("主規則:")
        for index, rule in enumerate(self.main_rules, start=1):
            print(f"{index}. {rule.name}: {rule.description}")
        
        print("副規則:")
        for index, rule in enumerate(self.sub_rules, start=1):
            print(f"{index}. {rule.name}: {rule.description}")
        
        print("事件:")
        for index, event in enumerate(self.events, start=1):
            print(f"{index}. {event.name}: {event.effect}")
        
        print("身分:")
        for index, role in enumerate(self.roles, start=1):
            print(f"{index}. {role.name}")
            for idx, ability in enumerate(role.abilities, start=1):
                print(f"  {idx}. {ability.name} ({ability.type}): {ability.description}")
        
        print("特殊規則:")
        for index, rule in enumerate(self.special_rules, start=1):
            print(f"{index}. {rule}")


class Event:
    def __init__(self, name, effect):
        self.name = name  # 事件名稱
        self.effect = effect  # 事件效果函數


class Role:
    def __init__(self, name, traits=None, abilities=None):
        self.name = name  # 身分名稱
        self.traits = traits if traits is not None else []  # 特性列表
        self.abilities = abilities if abilities is not None else []  # 能力列表

    def add_trait(self, trait):
        self.traits.append(trait)

    def add_ability(self, ability):
        self.abilities.append(ability)


class Rule:
    def __init__(self, name, description, special_conditions=None, roles=None):
        self.name = name  # 規則名稱
        self.description = description  # 規則描述
        self.special_conditions = special_conditions if special_conditions is not None else []  # 特殊條件列表
        self.roles = roles if roles is not None else []  # 涉及的身分列表

    def add_special_condition(self, condition):
        self.special_conditions.append(condition)

    def add_role(self, role):
        self.roles.append(role)


class Ability:
    def __init__(self, name, type, description, effect):
        self.name = name  # 能力名稱
        self.type = type  # 能力類型 (主動 或 被動)
        self.description = description  # 能力描述
        self.effect = effect  # 能力效果函數


# 定義主要規則表 Basic Tragedy X
basic_tragedy_x = RuleTable("Basic Tragedy X")

# 範例事件
event1 = Event("殺人事件", lambda culprit, area: [
    character.die() for character in area.characters if character != culprit
])
event2 = Event("流言蜚語", lambda culprit, area, script_writer: [
    targets[0].add_anxiety(2) and targets[1].add_conspiracy_points(1)
    for targets in [script_writer.choose_two_characters()]
])
event3 = Event("自殺", lambda culprit: culprit.die())
event4 = Event("醫院事件", lambda area, script_writer: [
    character.die() if area.conspiracy_points > 0 else None
    for character in area.characters
] + [
    script_writer.win_cycle() if area.conspiracy_points > 1 else None
])
event5 = Event("遠距殺人", lambda script_writer: [
    target.die()
    for target in [script_writer.choose_character_with_condition(lambda char: char.conspiracy_points > 1)]
])
event6 = Event("失蹤", lambda culprit, area, script_writer: [
    culprit.move_to(new_area) and new_area.add_conspiracy_points(1)
    for new_area in [script_writer.choose_area_except(area)]
])
event7 = Event("流傳", lambda culprit, script_writer: [
    target1.add_friendliness(-2) and target2.add_friendliness(2)
    for target1, target2 in [script_writer.choose_two_characters()]
])
event8 = Event("蝴蝶效應", lambda culprit, area, script_writer: [
    setattr(target, stat, getattr(target, stat) + 1)
    for target in [script_writer.choose_character_in_area(area)]
    for stat in [script_writer.choose_stat(["anxiety", "friendliness", "conspiracy_points"])]
])
event9 = Event("褻瀆", lambda shrine: shrine.add_conspiracy_points(2))

basic_tragedy_x.add_event(event1)
basic_tragedy_x.add_event(event2)
basic_tragedy_x.add_event(event3)
basic_tragedy_x.add_event(event4)
basic_tragedy_x.add_event(event5)
basic_tragedy_x.add_event(event6)
basic_tragedy_x.add_event(event7)
basic_tragedy_x.add_event(event8)
basic_tragedy_x.add_event(event9)

# 建立範例身分與能力
key_figure = Role("關鍵人物")
key_figure.add_ability(Ability(
    "犧牲的代價", "被動", "此角色死亡時，輪迴直接結束，腳本家勝利",
    lambda character, game: game.script_writer.win_cycle() if character.is_dead else None
))

murderer = Role("殺手")
murderer.add_trait("友好無視")
murderer.add_ability(Ability(
    "夜晚殺戮", "被動", "夜晚階段時，若與其他角色獨處，則殺害之",
    lambda character, game: (
        target.die() if (target := character.current_area.get_random_character_except(character)) and character.current_area.is_night else None
    )
))
murderer.add_ability(Ability(
    "陰謀操控", "被動", "夜晚階段時，陰謀>3，腳本家勝利，輪迴結束",
    lambda character, game: (
        game.script_writer.win_cycle() if character.conspiracy_points > 3 else None
    )
))

mastermind = Role("黑幕")
mastermind.add_trait("友好無視")
mastermind.add_ability(Ability(
    "陰謀操控", "主動", "同地區其他角色或地區+1陰謀",
    lambda character, script_writer: (
        target.add_conspiracy_points(1) if isinstance(target := script_writer.choose_target_or_area(character.current_area), Character) else target.add_conspiracy_points(1)
    )
))

cultist = Role("邪教徒")
cultist.add_trait("友好無效")
cultist.add_ability(Ability(
    "陰謀取消", "被動", "行動結算階段，取消此地區偵探設置的陰謀禁止卡片",
    lambda area, is_scriptwriter_view: (
        area.remove_conspiracy_ban(), 
        print(f"陰謀禁止卡片在地區 {area.name} 被取消") if is_scriptwriter_view else None
    )
))

witch = Role("魔女")
witch.add_trait("友好無效")

time_traveler = Role("時間旅行者")
time_traveler.add_trait("無法被殺害")
time_traveler.add_ability(Ability(
    "友好檢查", "被動", "最後一天夜晚階段，若友好值<2，腳本家勝利，輪迴結束",
    lambda character, game_state, is_scriptwriter_view: (
        game_state.end_loop("腳本家勝利")
        if game_state.current_day == game_state.final_day and character.friendship < 2 else None,
        print(f"{character.name} 的友好值不足，腳本家勝利") if is_scriptwriter_view else None
    )
))

# 添加次要角色
friend = Role("朋友")
friend.add_ability(Ability(
    "犧牲的代價", "被動", "輪迴結束死亡時，腳本家勝利並公開身分",
    lambda character, game: game.script_writer.win_cycle() if character.is_dead else None
))

misleader = Role("誤導者")
misleader.add_ability(Ability(
    "不安增加", "主動", "能力階段對同地區角色+1不安",
    lambda target, is_scriptwriter_view: (
        target.add_anxiety(1),
        print(f"{target.name} +1 不安") if is_scriptwriter_view else None
    )
))

lover = Role("戀人")
lover.add_ability(Ability(
    "不安增加", "被動", "死亡時使情人+6不安",
    lambda partner, is_scriptwriter_view: (
        partner.add_anxiety(6),
        print(f"情人增加 6 不安") if is_scriptwriter_view else None
    )
))

loved_one = Role("情人")
loved_one.add_ability(Ability(
    "不安增加", "被動", "死亡時使戀人+6不安",
    lambda partner, is_scriptwriter_view: (
        partner.add_anxiety(6),
        print(f"戀人增加 6 不安") if is_scriptwriter_view else None
    )
))
loved_one.add_ability(Ability(
    "腳本家勝利", "被動", "夜晚階段若不安>3且陰謀值>0，腳本家勝利，輪迴結束",
    lambda character, game_state, is_scriptwriter_view: (
        game_state.end_loop("腳本家勝利")
        if character.anxiety > 3 and character.conspiracy > 0 else None,
        print(f"因為 {character.name} 的條件滿足，腳本家勝利") if is_scriptwriter_view else None
    )
))

# 添加規則表到遊戲系統
rule_tables = {
    1: basic_tragedy_x
}

def display_all_rule_tables():
    for idx, rule_table in rule_tables.items():
        print(f"{idx}. {rule_table.name}")

def get_rule_table_by_id(rule_table_id):
    return rule_tables.get(rule_table_id, None)

# 新增主要規則
additional_main_rules = [
    Rule("未來改變作戰", "邪教徒*1，時間旅行者*1。蝴蝶效應事件發生後，該輪迴結束時腳本家勝利。"),
    Rule("巨型定時炸彈", "魔女*1。輪迴結束時，若魔女的初期所在區域陰謀>1，腳本家勝利。")
]

# 新增副規則
additional_sub_rules = [
    Rule("友情小圈圈", "朋友*2，誤導者*1"),
    Rule("戀愛的模樣", "戀人*1，情人*1"),
    Rule("殺人魔潛伏", "朋友*1，殺人魔*1"),
    Rule("人心惶惶", "每輪迴一次，腳本家可以在能力階段使任意地區+1陰謀。"),
    Rule("惡性譫妄病毒", "誤導者*1。本遊戲中，普通人不安>2時，變成殺人魔。"),
    Rule("因果之線", "輪迴重啟後，前一輪迴友好>0的角色+2不安。"),
    Rule("不定因子", "因子*1")
]

# 將這些規則添加到基礎悲劇 X 中
for rule in additional_main_rules:
    basic_tragedy_x.add_main_rule(rule)

for rule in additional_sub_rules:
    basic_tragedy_x.add_sub_rule(rule)
