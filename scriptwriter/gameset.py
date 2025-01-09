import random
from database.character_database import load_character_database

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

class ScriptEditor:
    def __init__(self):
        self.rules = []
        self.secret_rules = []
        self.characters = []
        self.rounds = 0
        self.days_per_round = 0
        self.events = []
        self.rule_tables = []  # 所有規則表
        self.current_rule_table = None  # 當前選擇的規則表

    def add_rule_table(self, rule_table):
        self.rule_tables.append(rule_table)

    def choose_rule_table(self, index):
        if 0 <= index < len(self.rule_tables):
            self.current_rule_table = self.rule_tables[index]
            print(f"選擇的規則表: {self.current_rule_table.name}")
        else:
            print("無效的規則表索引")

    def display_rule_tables(self):
        for index, rule_table in enumerate(self.rule_tables, start=1):
            print(f"{index}. {rule_table.name}")

    def construct_scenario(self):
        # 選擇規則表
        self.display_rule_tables()
        choice = int(input("選擇規則表索引: ")) - 1
        self.choose_rule_table(choice)

        # 劇本家從公開規則表中選擇一張
        self.rules = self.current_rule_table.main_rules
        
        # 劇本家秘密選擇數條規則
        self.secret_rules = self.current_rule_table.sub_rules
        
        # 從角色庫中選擇角色
        self.characters = self.select_characters()
        
        # 依據規則賦予角色身分
        self.assign_roles()
        
        # 決定輪迴次數
        self.rounds = self.choose_rounds()
        
        # 決定每輪回合數
        self.days_per_round = self.choose_days_per_round()
        
        # 決定哪些日子會發生事件
        self.events = self.schedule_events()
        
        # 決定事件犯人
        self.assign_event_criminals()

    def choose_public_rule(self):
        # 示例：選擇公開規則
        return ["公開規則1", "公開規則2"]

    def choose_secret_rules(self):
        # 示例：選擇秘密規則
        return ["秘密規則1", "秘密規則2"]

    def select_characters(self):
        # 示例：選擇角色
        character_list = load_character_database()
        return random.sample(character_list, 5)  # 隨機選擇五個角色

    def assign_roles(self):
        # 示例：賦予角色身分
        for character in self.characters:
            character.secret_identity = random.choice(["角色A", "角色B", "角色C"])

    def choose_rounds(self):
        # 示例：決定輪迴次數
        return random.randint(2, 5)

    def choose_days_per_round(self):
        # 示例：決定每輪回合數
        return random.randint(3, 7)

    def schedule_events(self):
        # 示例：決定哪些日子會發生事件
        return ["事件1", "事件2", "事件3"]

    def assign_event_criminals(self):
        # 示例：決定事件犯人
        for event in self.events:
            event_criminal = random.choice(self.characters).name
            print(f"為事件 {event} 分配犯人 {event_criminal}")


# 添加規則到規則表
rule_table.add_main_rule(ancient_myth)
rule_table.add_sub_rule(causal_line)
rule_table.add_event(event1)
rule_table.add_role(key_figure)
rule_table.add_role(mastermind)
rule_table.add_role(murderer)

# 遊戲初始化
script_editor = ScriptEditor()
script_editor.add_rule_table(rule_table)
script_editor.construct_scenario()
