import random
from database.RuleTable import all_rule_tables, get_rule_table_by_id
from database.character_database import load_character_database

class AIGameSet:
    def __init__(self, character_manager):
        self.character_manager = character_manager
        self.rule_tables = self.load_rule_tables()
        self.character_db = load_character_database()
        self.initialize_script()

    def load_rule_tables(self):
        # 動態讀取並返回所有規則表
        return all_rule_tables

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

        # 步驟 9: 為角色分配身分能力
        self.assign_role_abilities()

    def select_main_rule_table(self):
        # 隨機選擇一個規則表
        rule_table_id = random.choice(list(self.rule_tables.keys()))
        return get_rule_table_by_id(rule_table_id)

    def select_characters(self, min_characters, max_characters):
        # 隨機選擇角色數量並從角色資料庫中選擇角色
        num_characters = random.randint(min_characters, max_characters)
        return random.sample(self.character_db, num_characters)

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
        for role, count in self.secret_main_rule.roles.items():
            for _ in range(count):
                if self.characters:
                    character = random.choice(self.characters)
                    identities[character] = role
                    self.characters.remove(character)

        for sub_rule in self.secret_sub_rules:
            for role, count in sub_rule.roles.items():
                for _ in range(count):
                    if self.characters:
                        character = random.choice(self.characters)
                        identities[character] = role
                        self.characters.remove(character)
        return identities

    def assign_event_criminals(self):
        criminals = list(self.characters)
        random.shuffle(criminals)
        assigned_criminals = {}
        for day, event in self.scheduled_events.items():
            if criminals:
                criminal = criminals.pop()
                assigned_criminals[day] = criminal
        return assigned_criminals

    def assign_role_abilities(self):
        for character, role_name in self.identities.items():
            role = next((role for role in self.main_rule_table.roles if role.name == role_name), None)
            if role:
                character.role_abilities = role.abilities
            for sub_rule in self.secret_sub_rules:
                sub_role = next((role for role in sub_rule.roles if role.name == role_name), None)
                if sub_role:
                    character.role_abilities.extend(sub_role.abilities)

    def get_public_info(self):
        return {
            "main_rule_table": self.main_rule_table.name,
            "total_days": self.total_days,
            "total_cycles": self.total_cycles,
            "characters": [character.name for character in self.characters],
            "scheduled_events": {day: event.name for day, event in self.scheduled_events.items()}
        }

    def get_secret_info(self):
        secret_info = {
            "main_rule": self.secret_main_rule.name,
            "sub_rules": [rule.name for rule in self.secret_sub_rules],
            "identities": {character.name: role for character, role in self.identities.items()},
            "event_criminals": {day: criminal.name for day, criminal in self.event_criminals.items()}
        }
        return secret_info