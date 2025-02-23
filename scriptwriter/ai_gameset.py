import random
from database.RuleTable import RuleTable, Role
from database.Basecharacter import load_Basecharacters
from common.character import CharacterManager
from common.area_and_date import AreaManager, TimeManager
import copy

class AIGameSet:
    def __init__(self):
        # 步驟 0: 建立地區和日期管理器、建立角色管理器、建立資料庫
        self.character_db = load_Basecharacters() 
        self.character_manager = CharacterManager(self.character_db)  # 讓 Manager 管理角色
        self.area_manager = AreaManager()  # 初始化地區管理器
        self.area_manager.initialize_areas()  # 初始化地區

        self.time_manager = TimeManager(1,1)  # 初始化日期管理器，預設總輪迴數和總日期數為 1

        # 步驟 1: 隨機選擇主要規則表
        self.selected_rule_table = RuleTable.get_rule_table_by_id(random.randint(1,3))
        #print("選擇的規則表: ", self.selected_rule_table.name) 

        # 步驟 2: 選擇一條主規則、二條副規則
        self.selected_main_rule = random.choice(self.selected_rule_table.main_rules)
        self.selected_sub_rules = random.sample(self.selected_rule_table.sub_rules, 2)
        #print("選擇的主要規則: ", self.selected_main_rule[0].name)
        #print("選擇的副規則: ", [rule.name for rule in self.selected_sub_rules])

        # 步驟 3: 選擇角色
        self.character_manager.initialize_characters()  # 讓 Manager 選角色
        #print("選擇的角色: ", [character.name for character in self.character_manager.characters])

        self.time_manager.total_cycles = random.randint(4, 7)  # 初始化總輪迴數
        self.time_manager.total_days = random.randint(10, 10)  # 初始化總日期數

        # 步驟 4: 秘密分配角色身分
        self.passive_abilities = {
            "on_death": [],
            "night_phase": [],
            "end_of_cycle": [],
            "start_of_cycle": [],
            "change_anxiety": [],
            "change_conspiracy": [],
            "area_conspiracy": [],
            "assign_criminal": [],
            "post_event": []
        }
        self.assign_roles()
        # 輸出被動能力列表
        #print("📜 被動能力列表：")
        for key, abilities in self.passive_abilities.items():
            print(f"  🔹 {key}: {[ability.name for ability in abilities]}")

        # 輸出所有角色的當前身分與能力
        #print("\n🎭 所有角色的身份與能力：")
        for character in self.character_manager.characters:
            #print(f"🔹 {character.name} (ID: {character.Ch_id}) - 身分: {character.role.name}")
            
            passive_names = [ability.name for ability in character.role.passive_RAs]
            active_names = [ability.name for ability in character.role.active_RAs]

            #print(f"    🛡 被動能力: {passive_names if passive_names else '無'}")
            #print(f"    ⚔ 主動能力: {active_names if active_names else '無'}")
            #print("-" * 40)
        # 步驟 5: 決定事件及其發生日期與犯人
        self.scheduled_events = self.select_events(self.time_manager.total_days)
        self.event_criminals = self.assign_event_criminals()

    def assign_roles(self):
        """根據已選定的 main_rule 和 sub_rules，為角色分配適當的身分"""

        # 1️⃣ **收集所有需要的角色**
        role_name_list =[]
        role_name_list.extend(self.selected_main_rule[0].assign_roles) # 主規則角色
        for rule_name in self.selected_sub_rules:
            role_name_list.extend(rule_name.assign_roles)  # 副規則角色
        
        # 2️⃣ **開始分配角色**
        available_characters = [char for char in self.character_manager.characters if char.role.name == '普通人']
        for role_name in role_name_list:

            chosen_character = random.choice(available_characters)  # 隨機選擇一個未分配角色
            available_characters.remove(chosen_character)  # 移除已分配角色
            role = Role.get_role_by_role_name(self.selected_rule_table , role_name)
            chosen_character.role = role # 分配角色
            #print(f"{chosen_character.name}被賦予{role_name}")
            
        # 3️⃣ **記錄所有角色的被動能力**
        self.collect_passive_abilities(chosen_character.role.passive_RAs)

    def collect_passive_abilities(self, passive_abilities):
        """ 輸入被動能力，依據其標籤自動歸類 """
        for passive_ability in passive_abilities:         
            if passive_ability.trigger_condition in self.passive_abilities:
                self.passive_abilities[passive_ability.trigger_condition].append(passive_ability)



    def select_events(self, max_events):
        if not self.selected_rule_table.events:
            raise ValueError("The main rule table has no events to select from.")

        # 確保 event_list 是純 list
        event_list = self.selected_rule_table.events[0] if isinstance(self.selected_rule_table.events, tuple) else self.selected_rule_table.events
        
        total_days = self.time_manager.total_days  # 取得遊戲總天數
        num_events = min(random.randint(10, max_events), total_days)  # 確保不超過天數
        
        event_days = random.sample(range(1, total_days + 1), num_events)  # 隨機選擇發生事件的日子
        scheduled_events = {}  # 事件時間表

        for day in event_days:
            event_template = random.choice(event_list)  # 取得一個事件樣本
            event = copy.deepcopy(event_template)  # 創建新的事件副本，確保不影響原始事件
            event.date = day  # 設定事件發生日期
            scheduled_events[day] = event  # 記錄事件

        return scheduled_events

    def assign_event_criminals(self):
        available_characters = set(self.character_manager.characters)  # 角色集合（確保唯一性）
        
        for day, event in self.scheduled_events.items():
            if not available_characters:
                raise ValueError("角色數不足，無法分配所有事件的犯人")

            criminal = random.choice(list(available_characters))  # 隨機選擇犯人
            available_characters.remove(criminal)  # 移除已分配的角色，確保不重複
            event.criminal = criminal  # 設定犯人

            print(f"✅ 事件 '{event.name}'（第 {event.date} 天）犯人設置為：{criminal.name}")


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
                next((char.name for char in self.character_manager.characters if char.Ch_id == Ch_id), f"未知角色 {Ch_id}"): role_name
                for Ch_id, role_name in self.roles.items()
            },

        }
        return secret_info