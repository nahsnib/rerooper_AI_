import random
from database.RuleTable import RuleTable
from database.Basecharacter import load_Basecharacters
from common.character import Character, CharacterManager
from common.area_and_date import TimeManager
from game import Game

class AIGameSet:
    def __init__(self):
        # 步驟 1: 隨機選擇主要規則表
        self.rule_table = RuleTable.get_rule_table_by_id(random.randint(1,1))
        print("選擇的規則表: ", self.rule_table.name) 
        # 步驟 2: 選擇角色
        self.character_db = load_Basecharacters() 
        self.character_manager = CharacterManager(self.character_db)  # 讓 Manager 管理角色
        self.character_manager.initialize_characters()  # 讓 Manager 選角色

        print("選擇的角色: ", [character.name for character in self.character_manager.characters])

        self.total_cycles = 4  # 初始化輪迴數
        self.total_days = 4  # 初始化總日期數

        self.main_rule = []  # 秘密主規則
        self.sub_rules = []  # 秘密副規則
        self.scheduled_events = {}
        self.roles = {}  # 秘密角色身分
        self.event_criminals = {}  # 秘密事件犯人


        
        self.initialize_script()  # 初始化劇本

    def initialize_script(self):

        # 步驟 3: 決定總日期數
        self.total_days = random.randint(4, 7)

        # 步驟 4: 決定事件及其發生日期
        self.scheduled_events = self.select_events(self.total_days)

        # 步驟 5: 決定輪迴數
        self.total_cycles = random.randint(4, 7)

        # 步驟 6: 選定主規則和副規則
        self.main_rule = random.choice(self.rule_table.main_rules)
        self.sub_rules = random.sample(self.rule_table.sub_rules, 2)
        print("選擇的主要規則: ", self.main_rule.name)
        print("選擇的副規則: ", [rule.name for rule in self.sub_rules])

        # 步驟 7: 秘密分配角色身分
        self.roles = self.assign_roles()

        # 步驟 8: 設定事件的犯人             
        self.event_criminals = self.assign_event_criminals()

    def assign_roles(self):
        """ 根據已選定的 main_rule 和 sub_rules，為角色分配適當的身分 """

        # 1️⃣ **收集需要分配的角色身分**
        role_requirements = self.main_rule.roles.copy()  # 先複製主規則的角色需求
        for rule in self.sub_rules:
            for role, count in rule.roles.items():
                role_requirements[role] = role_requirements.get(role, 0) + count  # 合併副規則的需求

        print("\n需要分配的身分：", role_requirements)  # 調試用，確認需求正確

        # 2️⃣ **準備角色分配**
        available_characters = self.character_manager.characters[:]  # 可選角色列表（複製避免修改原本的 `self.characters`）
        assigned_roles = {}  # 存放角色分配結果 (角色ID -> 身分名稱)
        
        # 角色類型與對應物件（確保從列表轉成字典）
        all_roles = {role.name: role for role in self.rule_table.roles}

        # 3️⃣ **開始分配角色身分**
        for role_name, count in role_requirements.items():
            if role_name not in all_roles:
                print(f"⚠ 找不到角色身分: {role_name}，請檢查 `self.rule_table.roles` 是否正確！")
                continue  # 若角色名稱不存在於規則表，則跳過

            for _ in range(count):
                if not available_characters:
                    print(f"⚠ 無法分配 {role_name}，角色數量不足！")
                    break

                chosen_character = random.choice(available_characters)  # 隨機選擇一名角色
                available_characters.remove(chosen_character)  # 從可用角色列表中移除
                
                # 設定角色的身份、能力、特性
                chosen_character.role_name = role_name
                chosen_character.traits = all_roles[role_name].traits  # 角色的特性
                chosen_character.role_abilities = all_roles[role_name].abilities  # 角色的能力
                
                assigned_roles[chosen_character.Ch_id] = role_name  # 記錄角色ID與分配的身份

        # 4️⃣ **回傳角色分配結果**
            return assigned_roles

    def select_events(self, max_events):
        if not self.rule_table.events:
            raise ValueError("The main rule table has no events to select from.")

        # 至少要有一起事件
        num_events = random.randint(1, max_events) if max_events > 1 else 1
        num_events = max(num_events, 1)  # 保證至少選 1 個事件

        event_days = random.sample(range(1, self.total_days + 1), num_events)

        if len(self.rule_table.events) >= num_events:
            events = random.sample(self.rule_table.events, k=num_events)
        else:
            events = random.choices(self.rule_table.events, k=num_events)

        scheduled_events = {}
        for day, event in zip(event_days, events):
            event.date = day  # 設定事件發生日期
            scheduled_events[day] = event
        return scheduled_events

  
    def assign_event_criminals(self):
        num_events = len(self.scheduled_events)
        num_characters = len(self.character_manager.characters)
        print(f"\n🔍 事件數量：{num_events}，角色數量：{num_characters}")

        criminals = random.sample(self.character_manager.characters, k=num_events)  # 隨機選擇不同的角色作為每個事件的犯人

        for (day, event), criminal in zip(self.scheduled_events.items(), criminals):
            event.criminal_name = criminal.name  # 直接更新事件的 criminal_name

            # 🔍 Debug 訊息
            print(f"✅ 事件 '{event.name}'（第 {day} 天）犯人設置為：{criminal.name}")


    def get_public_info(self):
        return {
            "rule_table": self.rule_table.name,
            "total_days": self.total_days,
            "total_cycles": self.total_cycles,
            "characters": [character.name for character in self.character_manager.characters],
            "scheduled_events": {day: event.name for day, event in self.scheduled_events.items()}
        }

    def get_secret_info(self):
        secret_info = {
            "main_rule": self.main_rule.name,
            "sub_rules": [rule.name for rule in self.sub_rules],
            "roles": {
                next((char.name for char in self.character_manager.characters if char.id == Ch_id), f"未知角色 {Ch_id}"): role_name
                for Ch_id, role_name in self.roles.items()
            },
            "event_criminals": {day: criminal.name for day, criminal in self.event_criminals.items()}
        }
        return secret_info