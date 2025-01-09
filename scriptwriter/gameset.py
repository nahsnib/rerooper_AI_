# scriptwriter/gameset.py

import random
from database.character_database import load_character_database
from database.RuleTable import display_all_rule_tables, get_rule_table_by_id

class ScriptEditor:
    def __init__(self):
        self.rules = []
        self.secret_rules = []
        self.characters = []
        self.rounds = 0
        self.days_per_round = 0
        self.events = []
        self.current_rule_table = None  # 當前選擇的規則表

    def choose_rule_table(self):
        # 顯示所有規則表
        display_all_rule_tables()
        choice = int(input("選擇規則表索引: "))
        self.current_rule_table = get_rule_table_by_id(choice)
        if self.current_rule_table:
            print(f"選擇的規則表: {self.current_rule_table.name}")
        else:
            print("無效的規則表索引")

    def construct_scenario(self):
        # 選擇規則表
        self.choose_rule_table()

        # 劇本家從公開規則表中選擇一張
        self.rules = self.current_rule_table.main_rules
        
        # 劇本家秘密選擇數條規則
        self.secret_rules = self.current_rule_table.sub_rules
        
        # 從角色庫中選擇角色
        self.characters = self.select_characters()
        
        # 依據規則賦予角色身分
        self.assign_roles()
        
        # 決定輪迾次數
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

# 遊戲初始化
script_editor = ScriptEditor()
script_editor.construct_scenario()
