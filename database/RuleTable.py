import random

class RuleTable:
    def __init__(self, id=0, name="不應該出現這串字", main_rules=None, sub_rules=None, events=None, roles=None, special_rules=None):
        self.id = id  # 新增的編號屬性
        self.name = name
        self.main_rules = main_rules  # 主規則列表
        self.sub_rules = sub_rules   # 副規則列表
        self.events =  events      # 事件列表
        self.roles = roles       # 身分列表
        self.special_rules = special_rules  # 特殊規則列表

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
                print(f"   ({ability.active}): {ability.description}")
        
        print("特殊規則:")
        for index, rule in enumerate(self.special_rules, start=1):
            print(f"{index}. {rule}")

    def get_rule_table_by_id(rule_table_id):
        return next((char for char in load_rule_table() if char.id == rule_table_id), None)

class Event:
    def __init__(self, id, name, effect):
        self.id = id  # 事件 ID
        self.name = name  # 事件名稱
        self.effect = effect  # 事件效果函數
        self.criminal_name = None  # 事件犯人（由遊戲決定）
        self.happened = False  # 事件是否發生
        self.date = 0  # 事件發生日期
    
    def trigger(self, game, script_writer):
        """ 觸發事件 """
        if self.criminal_name:
            culprit = game.character_manager.get_character_by_name(self.criminal_name)
        else:
            culprit = None
        
        self.effect(culprit, game, script_writer)
        self.happened = True
    def __str__(self):
        return self.name  # 返回事件名稱

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

class Role_Ability:
    def __init__(self, id, name, active, description, effect, requires_target=False):
        self.id = id  # 能力的唯一編號
        self.name = name  # 能力名稱
        self.active = active  # 能力類型 (主動 或 被動)
        self.description = description  # 能力描述
        self.effect = effect  # 能力效果函數
        self.requires_target = requires_target  # 是否需要選擇目標


def load_rule_table():
# 創建規則表
    return [
        RuleTable(
            id=1,
            name=  "Basic Tragedy X",
            main_rules=[
                Rule(1, "殺人計畫", "關鍵人物*1、殺手*1、黑幕*1。", roles={"關鍵人物": 1, "殺手": 1, "黑幕": 1}),
                Rule(2, "被封印之物", "黑幕*1、邪教徒*1。輪迴結束時，如果神社陰謀>1，腳本家勝利", roles={"黑幕": 1, "邪教徒": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利")),
                Rule(3, "和我簽下契約吧！", "關鍵人物*1。輪迴結束時，若關鍵人物陰謀>1，腳本家勝利。關鍵人物必須為少女", roles={"關鍵人物": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利")),
                Rule(4, "未來改變作戰", "邪教徒*1，時間旅行者*1。蝴蝶效應事件發生後，該輪迴結束時腳本家勝利。", roles={"邪教徒": 1, "時間旅行者": 1}),
                Rule(5, "巨型定時炸彈", "魔女*1。輪迴結束時，若魔女的初期所在區域陰謀>1，腳本家勝利。", roles={"魔女": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利"))
            ],
            sub_rules=[
                Rule(6, "友情小圈圈", "朋友*2，誤導者*1", roles={"朋友": 2, "誤導者": 1}),
                Rule(7, "戀愛的模樣", "戀人*1，情人*1", roles={"病嬌": 1, "戀人": 1}),
                Rule(8, "殺人魔潛伏", "朋友*1，殺人魔*1", roles={"朋友": 1, "殺人魔": 1}),
                Rule(9, "人心惶惶", "每輪迴一次，腳本家可以在能力階段使任意地區+1陰謀。", roles={}, special_effect=lambda game_state: game_state.add_conspiracy_points_to_any_area()),
                Rule(10, "惡性譫妄病毒", "誤導者*1。本遊戲中，普通人不安>2時，變成殺人魔。", roles={"誤導者": 1}, special_effect=lambda game_state: game_state.transform_normal_to_murderer()),
                Rule(11, "因果之線", "輪迴重啟後，前一輪迴友好>0的角色+2不安。", roles={}, special_effect=lambda game_state: game_state.add_anxiety_to_characters_with_friendship_above(0, 2))
            ],
            events= [
                Event(1, "殺人事件", lambda culprit, game, script_writer: [
                    target.handle_death("事件 - 殺人事件", game)
                    for target in [script_writer.choose_character_in_area(culprit.location, exclude=[culprit])]
                ]),
                
                Event(2, "流言蜚語", lambda culprit, game, script_writer: [
                    targets[0].add_anxiety(2), targets[1].add_conspiracy_points(1)
                    for targets in [script_writer.choose_two_characters()]
                ]),
                
                Event(3, "自殺", lambda culprit, game, script_writer: culprit.handle_death("事件 - 自殺", game)),
                
                Event(4, "醫院事件", lambda culprit, game, script_writer: [
                    character.handle_death("事件 - 醫院事件", game) if game.area_manager.get_area("醫院").conspiracy_points > 0 else None
                    for character in game.area_manager.get_area("醫院").characters
                ] + [
                    script_writer.win_cycle() if game.area_manager.get_area("醫院").conspiracy_points > 1 else None
                ]),
                
                Event(5, "遠距殺人", lambda culprit, game, script_writer: [
                    target.handle_death("事件 - 遠距殺人", game)
                    for target in [script_writer.choose_character_with_condition(lambda char: char.conspiracy_points > 1)]
                ]),
                
                Event(6, "失蹤", lambda culprit, game, script_writer: [
                    culprit.move_to(new_area), new_area.add_conspiracy_points(1)
                    for new_area in [script_writer.choose_area_except(culprit.location)]
                ]),
                
                Event(7, "流傳", lambda culprit, game, script_writer: [
                    target1.add_friendliness(-2), target2.add_friendliness(2)
                    for target1, target2 in [script_writer.choose_two_characters()]
                ]),
                
                Event(8, "蝴蝶效應", lambda culprit, game, script_writer: [
                    setattr(target, stat, getattr(target, stat) + 1)
                    for target in [script_writer.choose_character_in_area(culprit.location)]
                    for stat in [script_writer.choose_stat(["anxiety", "friendliness", "conspiracy_points"])]
                ]),
                
                Event(9, "褻瀆", lambda culprit, game, script_writer: game.area_manager.get_area("神社").add_conspiracy_points(2))
            ],

            roles=[
                Role(1, "關鍵人物",traits=["友好無視"], abilities=[
        Role_Ability(id=101, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        Role_Ability(id=102, name="友好增加", active= True, description="自己增加 1 點友好", effect=lambda character: character.change_friendship(1), requires_target=False),
            ]),
                Role(2, "殺手",traits=["友好無視"], abilities=[
        Role_Ability(id=201, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(3, "黑幕",traits=["友好無視"], abilities=[
        Role_Ability(id=301, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(4, "邪教徒",traits=["友好無視"], abilities=[
        Role_Ability(id=401, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(5, "魔女",traits=["友好無視"], abilities=[
        Role_Ability(id=501, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(6, "時間旅行者",traits=["友好無視"], abilities=[
        Role_Ability(id=601, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(7, "朋友",traits=["友好無視"], abilities=[
        Role_Ability(id=701, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(8, "誤導者",traits=["友好無視"], abilities=[
        Role_Ability(id=801, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(9, "病嬌",traits=["友好無視"], abilities=[
        Role_Ability(id=901, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(10, "戀人",traits=["友好無視"], abilities=[
        Role_Ability(id=1001, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(11, "殺人魔",traits=["友好無視"], abilities=[
        Role_Ability(id=1101, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(12, "因子",traits=["友好無視"], abilities=[
        Role_Ability(id=1201, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ])
            ],
            special_rules=[],
        )
    ]

basic_tragedy_x = RuleTable.get_rule_table_by_id(1)
basic_tragedy_y = RuleTable.get_rule_table_by_id(1)
basic_tragedy_z = RuleTable.get_rule_table_by_id(1)
basic_tragedy_w = RuleTable.get_rule_table_by_id(1)

basic_tragedy_y.id = 2
basic_tragedy_z.id = 3
basic_tragedy_w.id = 4


basic_tragedy_y.display_rules()