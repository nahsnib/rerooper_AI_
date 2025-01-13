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
        # 假設這裡讀取並返回所有規則表
        return {
            1: RuleTable(1, "Basic Tragedy X"),
            2: RuleTable(2, "Basic Tragedy Y"),
            3: RuleTable(3, "Basic Tragedy Z"),
            4: RuleTable(4, "Basic Tragedy W")
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
        # 隨機選擇一個規則表
        rule_table_id = random.choice(list(self.rule_tables.keys()))
        return get_rule_table_by_id(rule_table_id)

    def select_characters(self, min_characters, max_characters):
        # 隨機選擇角色數量並從角色資料庫中選擇角色
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
        random.shuffle(available_days)
        for event in events:
            if available_days:
                day = available_days.pop()
                scheduled_events[day] = event
        return scheduled_events

    def select_main_rule(self):
        return random.choice(self.main_rule_table.main_rules)

    def select_sub_rules(self, num_sub_rules):
        return random.sample(self.main_rule_table.sub_rules, k=num_sub_rules)

    def assign_identities(self):
        identities = {character: "普通人" for character in self.characters}
        for role in self.secret_main_rule.roles:
            count = role.get("count", 1)
            for _ in range(count):
                character = random.choice(list(identities.keys()))
                identities[character] = role["name"]
                self.characters.remove(character)
        
        for sub_rule in self.secret_sub_rules:
            for role in sub_rule.roles:
                count = role.get("count", 1)
                for _ in range(count):
                    character = random.choice(list(identities.keys()))
                    identities[character] = role["name"]
                    self.characters.remove(character)
        return identities

    def assign_event_criminals(self):
        criminals = list(self.characters)
        random.shuffle(criminals)
        assigned_criminals = {}
        for day, event in self.scheduled_events.items():
            criminal = criminals.pop()
            assigned_criminals[day] = criminal
        return assigned_criminals

    def get_public_info(self):
        return {
            "main_rule_table": self.main_rule_table.name,
            "total_days": self.total_days,
            "total_cycles": self.total_cycles,
            "characters": [character.name for character in self.characters],
            "scheduled_events": {day: event.name for day, event in self.scheduled_events.items()}
        }

    def get_secret_info(self):
        return {
            "secret_main_rule": self.secret_main_rule.name,
            "secret_sub_rules": [rule.name for rule in self.secret_sub_rules],
            "identities": self.identities,
            "event_criminals": {day: criminal.name for day, criminal in self.event_criminals.items()}
        }
