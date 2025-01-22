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

        # 確保規則表中包含事件
        if not self.main_rule_table.events:
            raise ValueError("The main rule table has no events to select from.")

        # 步驟 2: 選擇角色
        self.characters = self.select_characters(7, 12)

        # 確保角色數量在 7 到 12 之間
        if len(self.characters) < 7 or len(self.characters) > 12:
            raise ValueError("Number of characters selected is outside the allowed range (7-12).")

        # 步驟 3: 決定總日期數
        self.total_days = self.select_total_days(4, 7)

        # 確保事件數量不超過角色數量
        max_events = min(len(self.characters), self.total_days)

        # 步驟 4: 決定事件及其發生日期
        self.scheduled_events = self.select_events(max_events)

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

    def select_events(self, max_events):
        if not self.main_rule_table.events:
            raise ValueError("The main rule table has no events to select from.")

        # 隨機選擇一些天作為犯案日並安排事件
        num_events = random.randint(1, max_events)  # 隨機選擇事件數量
        event_days = random.sample(range(1, self.total_days + 1), num_events)  # 隨機選擇事件發生的天數

        # 在事件數量不足時允許重複選擇事件
        if len(self.main_rule_table.events) >= num_events:
            events = random.sample(self.main_rule_table.events, k=num_events)  # 隨機選擇事件
        else:
            events = random.choices(self.main_rule_table.events, k=num_events)  # 允許重複選擇事件

        scheduled_events = {}
        for day, event in zip(event_days, events):
            scheduled_events[day] = event
        return scheduled_events

    def select_main_rule(self):
        return random.choice(self.main_rule_table.main_rules)

    def select_sub_rules(self, num_sub_rules):
        return random.sample(self.main_rule_table.sub_rules, k=num_sub_rules)

    def assign_identities(self):
        identities = {character: "普通人" for character in self.characters}
        
        # 確保 self.secret_main_rule.roles 和 sub_rule.roles 返回角色名稱
        characters_copy = self.characters.copy()
        for role_name, count in self.secret_main_rule.roles.items():
            role = next((r for r in self.main_rule_table.roles if r.name == role_name), None)
            if role:
                for _ in range(count):
                    if characters_copy:
                        character = random.choice(characters_copy)
                        identities[character] = role.name
                        character.role_name = role.name  # 更新角色的身分名稱
                        character.traits = role.traits  # 更新角色的特性
                        character.role_abilities = role.abilities  # 更新角色的身份能力
                        characters_copy.remove(character)

        for sub_rule in self.secret_sub_rules:
            for role_name, count in sub_rule.roles.items():
                role = next((r for r in self.main_rule_table.roles if r.name == role_name), None)
                if role:
                    for _ in range(count):
                        if characters_copy:
                            character = random.choice(characters_copy)
                            identities[character] = role.name
                            character.role_name = role.name  # 更新角色的身分名稱
                            character.traits = role.traits  # 更新角色的特性
                            character.role_abilities = role.abilities  # 更新角色的身份能力
                            characters_copy.remove(character)
        return identities

    def assign_event_criminals(self):
        num_events = len(self.scheduled_events)
        num_characters = len(self.characters)

        if num_events > num_characters:
            raise ValueError("Number of events exceeds number of characters available to assign as criminals.")

        criminals = random.sample(self.characters, k=num_events)  # 隨機選擇不同的角色作為每個事件的犯人
        assigned_criminals = {}
        for day, criminal in zip(self.scheduled_events.keys(), criminals):
            assigned_criminals[day] = criminal
        return assigned_criminals

    def assign_role_abilities(self):
        for character, role_name in self.identities.items():
            role = next((role for role in self.main_rule_table.roles if role.name == role_name), None)
            if role:
                character.role_abilities = role.abilities
            for sub_rule in self.secret_sub_rules:
                sub_role = next((role for role in self.main_rule_table.roles if role.name == role_name), None)
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