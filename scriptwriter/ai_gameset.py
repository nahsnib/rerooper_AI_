import random
from database.RuleTable import RuleTable, Role
from game_gui import GameGUI
from common.character import CharacterManager
from common.area_and_date import AreaManager, TimeManager
from game_phases.player_detective.phase_manager import PhaseManager
import copy
from collections import Counter


class AIGameSet:
    def __init__(self, pre_game):
        # 步驟 0: 建立前置遊戲，建立被動能力表
        self.pre_game = pre_game
        self.pre_game.passive_abilities = {
            "on_death": [],
            "night_phase": [],
            "cycle_end": [],
            "cycle_start": [],
            "change_anxiety": [],
            "change_conspiracy": [],
            "area_conspiracy": [],
            "assign_roles"
            "assign_criminals": [],
            "before_crime"
            "after_crime": []
        }
        self.pre_game.area_manager = AreaManager()
        self.pre_game.area_manager.initialize_areas()
        self.pre_game.phase_manager = PhaseManager()
        self.pre_game.time_manager = TimeManager(1, random.randint(4, 7), 5)
        
        # 步驟 1: 隨機選擇主要規則表
        self.pre_game.selected_rule_table = RuleTable.get_rule_table_by_id(random.randint(1,3))
        #print("選擇的規則表: ", self.pre_game.selected_rule_table.name) 

        # 步驟 2: 選擇一條主規則、二條副規則
        self.pre_game.selected_main_rule = random.choice(self.pre_game.selected_rule_table.main_rules)
        self.pre_game.selected_sub_rules = random.sample(self.pre_game.selected_rule_table.sub_rules, 2)
        print("選擇的主要規則: ", self.pre_game.selected_main_rule.name)
        print("選擇的副規則: ", [rule.name for rule in self.pre_game.selected_sub_rules])

        # 步驟 2-1:如果選定的規則有特殊被動，記錄起來
        if self.pre_game.selected_main_rule.passive_RAs:
            self.collect_passive_abilities(self.pre_game.selected_main_rule.passive_RAs)
        for subrule in self.pre_game.selected_sub_rules:
            if subrule.passive_RAs:
                self.collect_passive_abilities(subrule.passive_RAs)
        self.print_passive_ability()

        # 步驟 3: 建立角色管理器，並且選擇角色
        self.pre_game.character_manager = CharacterManager()
        self.pre_game.character_manager.initialize_characters()  # 讓 Manager 選角色
        #print("選擇的角色: ", [character.name for character in self.pre_game.character_manager.characters])

       

        # 步驟 4: 秘密分配角色身分

        self.assign_roles()
        # 輸出被動能力列表
        #self.check_passive_ability()
        # 輸出所有角色的當前身分與能力
        #print("\n🎭 所有角色的身份與能力：")
        #for character in self.pre_game.character_manager.characters:
            #print(f"🔹 {character.name} (ID: {character.Ch_id}) - 身分: {character.role.name}")
            
            #passive_names = [ability.name for ability in character.role.passive_RAs]
            #active_names = [ability.name for ability in character.role.active_RAs]

            #print(f"    🛡 被動能力: {passive_names if passive_names else '無'}")
            #print(f"    ⚔ 主動能力: {active_names if active_names else '無'}")
            #print("-" * 40)
        # 步驟 5: 決定事件及其發生日期與犯人
        self.select_events()
        self.assign_event_criminals()

    def assign_roles(self):
        """根據已選定的 main_rule 和 sub_rules，為角色分配適當的身分"""
        self.pre_game.check_passive_ability("assign_roles")

        # 1️⃣ **收集所有需要的角色**
        role_name_list = []
        role_name_list.extend(self.pre_game.selected_main_rule.assign_roles)  # 主規則角色
        for rule in self.pre_game.selected_sub_rules:
            role_name_list.extend(rule.assign_roles)  # 副規則角色

        # 2️⃣ **檢查總數限制**
        role_counts = Counter(role_name_list)  # 計算每種角色的需求數
        for role_name, count in role_counts.items():
            role = Role.get_role_by_role_name(self.pre_game.selected_rule_table.id, role_name)
            if role and role.total_limit is not None and count > role.total_limit:
                role_counts[role_name] = role.total_limit  # 限制數量

        # 轉回角色名單
        role_name_list = []
        for role_name, count in role_counts.items():
            role_name_list.extend([role_name] * count)

        available_characters = [char for char in self.pre_game.character_manager.characters if char.role.name == '普通人']

        # 3️⃣ **特殊角色分配**
        if self.pre_game.madoka_flag:
            girl_candidates = [char for char in available_characters if char.gender == "少女"]
            if girl_candidates:
                chosen_character = random.choice(girl_candidates)
                available_characters.remove(chosen_character)
            else:
                raise ValueError("沒有符合條件的『少女』來擔任關鍵人物！")

            role = Role.get_role_by_role_name(self.pre_game.selected_rule_table.id, "關鍵人物")
            chosen_character.role = role
            role_name_list.remove("關鍵人物")

            for passive_ability in role.passive_RAs:
                passive_ability.owner = chosen_character
            for active_ability in role.active_RAs:
                active_ability.owner = chosen_character

        # 4️⃣ **隨機分配剩餘角色**
        for role_name in role_name_list:
            chosen_character = random.choice(available_characters)
            available_characters.remove(chosen_character)
            role = Role.get_role_by_role_name(self.pre_game.selected_rule_table.id, role_name)
            if role == None:
                raise ValueError(f"找不到名為 {role_name} 的角色")
            chosen_character.role = role

            for passive_ability in role.passive_RAs:
                if passive_ability:
                    passive_ability.owner = chosen_character
            for active_ability in role.active_RAs:
                if active_ability:
                    active_ability.owner = chosen_character

        # 5️⃣ **記錄所有角色的被動能力**
        self.collect_passive_abilities(chosen_character.role.passive_RAs)




    def collect_passive_abilities(self, passive_abilities):
        """ 輸入被動能力，依據其標籤自動歸類 """
        if passive_abilities:
            for passive_ability in passive_abilities:         
                if passive_ability.trigger_condition in self.pre_game.passive_abilities:
                    self.pre_game.passive_abilities[passive_ability.trigger_condition].append(passive_ability)



    def select_events(self):
        if not self.pre_game.selected_rule_table.events:
            raise ValueError("The main rule table has no events to select from.")

        # 確保 event_list 是純 list
        event_list = self.pre_game.selected_rule_table.events
        total_days = self.pre_game.time_manager.total_days  # 取得遊戲總天數

        # **計算 must_criminal = 1 的角色數，確保事件數量至少等於這個數**
        must_criminal_count = sum(1 for char in self.pre_game.character_manager.characters if char.must_criminal == 1)

        # **確保事件數量不低於 must_criminal = 1 的角色數**
        min_events = max(1, must_criminal_count)  
        num_events = random.randint(min_events, total_days)  # 確保不超過天數

        event_days = random.sample(range(1, total_days + 1), num_events)  # 隨機選擇發生事件的日子
        scheduled_events = {}  # 事件時間表

        for day in event_days:
            event = copy.deepcopy(random.choice(event_list))  # 取得一個事件副本
            event.date = day  # 設定事件發生日期
            scheduled_events[day] = event

        self.pre_game.scheduled_events = scheduled_events

    def assign_event_criminals(self): 
        # 檢查 assign_criminals 的被動能力
        self.pre_game.check_passive_ability("assign_criminal")

        # **分為三類角色**
        available_must_criminals = [char for char in self.pre_game.character_manager.characters if char.must_criminal == 1]
        available_characters = [char for char in self.pre_game.character_manager.characters if char.must_criminal == 0]
        
        self.pre_game.check_passive_ability("cycle_start")

        for day, event in self.pre_game.scheduled_events.items():
            if not available_must_criminals and not available_characters:
                raise ValueError("角色數不足，無法分配所有事件的犯人")

            # **優先選擇 must_criminal = 1 的角色**
            if available_must_criminals:
                criminal = available_must_criminals.pop(0)  # 先指派給 `must_criminal=1` 的角色
            else:
                criminal = random.choice(available_characters)  # 剩下的才隨機選擇
                available_characters.remove(criminal)  # 移除已分配的角色

            event.criminal = criminal  # 設定犯人
            print(f"✅ 事件 '{event.name}'（第 {event.date} 天）犯人設置為：{criminal.name}")


    def get_public_info(self):
        return {
            "rule_table": self.pre_game.rule_table.name,
            "total_days": self.pre_game.total_days,
            "total_cycles": self.pre_game.total_cycles,
            "characters": [character.name for character in self.pre_game.character_manager.characters],
            "scheduled_events": {day: event.name for day, event in self.pre_game.scheduled_events.items()}
        }

    def get_secret_info(self):
        secret_info = {
            "main_rule": self.pre_game.main_rule.name,
            "sub_rules": [rule.name for rule in self.pre_game.sub_rules],
            "roles": {
                next((char.name for char in self.pre_game.character_manager.characters if char.Ch_id == Ch_id), f"未知角色 {Ch_id}"): role_name
                for Ch_id, role_name in self.pre_game.roles.items()
            },

        }
        return secret_info
    


    def print_passive_ability(self):
        print("=== 當前被動能力清單 ===")
        for trigger, abilities in self.pre_game.passive_abilities.items():
            if abilities:
                print(f"【{trigger}】:")
                for ability in abilities:
                    print(f"  - {ability.name} (ID: {ability.id})")
            else:
                print(f"【{trigger}】: 無被動能力")
        print("=========================")
