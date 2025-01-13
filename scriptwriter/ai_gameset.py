import random
from database.RuleTable import RuleTable, get_rule_table_by_id
from database.character_database import CharacterDatabase

class AIGameSet:
    def __init__(self, character_manager):
        self.character_manager = character_manager
        self.rule_tables = self.load_rule_tables()
        self.character_db = CharacterDatabase()
        self.initialize_script()

    def load_rule_tables(self):
        return {
            1: get_rule_table_by_id(1),
            2: get_rule_table_by_id(2),
            3: get_rule_table_by_id(3),
            4: get_rule_table_by_id(4)
        }

    def initialize_script(self):
        # 步驟 1: 選擇主要規則表
        self.main_rule_table = self.select_main_rule_table()
        
        # 步驟 2: 選擇角色
        self.characters = self.select_characters(7, 12)
        
        # 步驟 3: 決定總日期數
        self.total_days = self.select_total_days(4, 7)
        
        # 步驟 4: 決定事件及其發生日期
        self.scheduled_events = self.select_events()
        
        # 步驟 5: 決定輪迴數
        self.total_cycles = self.select_total_cycles(4, 7)
        
        # 步驟 6: 選定主規則和副規則
        self.secret_main_rule = self.select_main_rule()
        self.secret_sub_rules = self.select_sub_rules(2)
        
        # 步驟 7: 秘密分配角色身分
        self.identities = self.assign_identities()
        
        # 步驟 8: 設定事件的犯人
        self.event_criminals = self.assign_event_criminals()

    def select_main_rule_table(self):
        rule_table_id = random.choice(list(self.rule_tables.keys()))
        return self.rule_tables[rule_table_id]

    def select_characters(self, min_characters, max_characters):
        num_characters = random.randint(min_characters, max_characters)
        return self.character_db.select_characters(num_characters)

    def select_total_days(self, min_days, max_days):
        return random.randint(min_days, max_days)

    def select_total_cycles(self, min_cycles, max_cycles):
        return random.randint(min_cycles, max_cycles)

    def select_events(self):
        events = random.sample(self.main_rule_table.events, k=self.total_days)
        scheduled_events = {}
        available_days = list(range(1, self.total_days + 1))
        random.shuffle
