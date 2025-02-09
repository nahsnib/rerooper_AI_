import random
from common.character import CharacterManager
from common.area_and_date import areas
from common.player import Player
from game_gui import GameGUI
from common.action import Action

class PlayerDetectiveActionPhase:
    def __init__(self, game, game_gui):
        self.game = game  # 整合 Game，讓 Phase 可以存取玩家
        self.game_gui = game_gui  # 讓行動階段控制 GUI
        self.scriptwriter_selections = []  # AI 劇本家的行動
        self.phase_type = "action"  # ✅ 新增此屬性
        self.player_selections = []  # 玩家偵探的行動
    
    def execute(self):
        """ 執行整個行動階段，先讓劇本家選擇行動，然後請求玩家輸入 """
        self.scriptwriter_select_actions()  # 讓 AI 劇本家選擇行動
        self.game_gui.update_scriptwriter_actions(self.scriptwriter_selections)
        
        # 請求玩家輸入

    def scriptwriter_select_actions(self):
        """ 劇本家 AI 自動選擇 3 個不同的目標和行動 """
        scriptwriter = self.game.players["劇本家"]
        available_targets = self.get_available_targets()
        selected_targets = []
        
        for _ in range(3):
            remaining_targets = [t for t in available_targets if t not in selected_targets]
            if not remaining_targets:
                break
            
            target = self.select_target_by_priority(remaining_targets)
            action = self.select_action_for_target(scriptwriter, target)
            
            if target and action:
                self.scriptwriter_selections.append({
                    "target": target,
                    "action": action
                })
                selected_targets.append(target)
        print(f"🤖 劇本家 AI 選擇了行動：{[action['action'].name for action in self.scriptwriter_selections]}，目標：{[action['target'] for action in self.scriptwriter_selections]}")
    
    def confirm_action_selection(self):
        selections = self.game_gui.get_player_action_selection()
        
        if not selections:
            return  # ✅ 玩家選擇無效，應該重新選擇，而不是繼續執行

        self.player_selections = selections

        self.player_selections = selections
        self.execute_actions()  # ✅ 直接執行，因為 `get_player_action_selection()` 已經過濾無效選擇
        self.game_gui.show_message(f"選擇了行動：{[action['action'].name for action in self.player_selections]}，目標：{[action['target'] for action in self.player_selections]}")
        self.game_gui.update_area_widgets()  # ✅ 更新區域資訊

    def select_target_by_priority(self, targets):
        """ 劇本家 AI 根據優先順序選擇目標（焦慮值高的角色優先） """
        character_manager = self.game.character_manager
        character_dict = {c.name: c for c in character_manager.characters}
        
        highest_anxiety = -1
        priority_target = None
        
        for target in targets:
            if target in character_dict:
                character = character_dict[target]
                if character.anxiety > highest_anxiety:
                    highest_anxiety = character.anxiety
                    priority_target = target
        
        return priority_target if priority_target else targets[0]

    def select_action_for_target(self, player, target):
        """ 根據目標選擇合適的行動 """
        character_manager = self.game.character_manager
        character_dict = {c.name: c for c in character_manager.characters}
        
        if target in character_dict:
            character = character_dict[target]
            if character.anxiety > 3:
                for action in player.available_actions.values():
                    if "陰謀" in action.name and action.can_use():
                        return action
        
        for action in player.available_actions.values():
            if action.can_use():
                return action
        return None

    def get_available_targets(self):
        """ 獲取所有可用的目標（角色 + 地區） """
        targets = [char.name for char in self.game.character_manager.characters]
        targets.extend(["醫院", "神社", "都市", "學校"])
        return targets
   
    def execute_actions(self):
        """執行所有行動（AI + 玩家），按照遊戲的結算順序處理"""
        all_actions = self.scriptwriter_selections + self.player_selections

        # ✅ 按照目標整理行動
        action_dict = {}
        for selection in all_actions:
            target = selection["target"]
            action = selection["action"]
            if target not in action_dict:
                action_dict[target] = []
            action_dict[target].append(action)

        # ✅ 開始按照規則執行行動
        for target, actions in action_dict.items():
            # 1️⃣ **先標記原始行動為已使用**
            for action in actions:
                action.used = True  # 確保所有原始行動都被標記
                action.times_used += 1  # 🚀 確保執行時累加使用次數
            # 2️⃣ **合成行動（若有需要）**
            combined_action = self.combine_action(actions)
            if combined_action is not None:
                actions = [combined_action]  # ✅ 成功合成則只執行合成行動
            
            # 3️⃣ **執行行動（排除 999 無效行動）**
            for action in actions:
                if action.action_id == 999:
                    print(f"❌ {target} 的行動無效，跳過。")
                    continue
                
                print(f"✅ {target} 執行行動：{action.name}")
                action.effect(self.get_target_instance(target))



           

    def combine_action(self, actions):
        """ 根據規則合成行動，若無合成則回傳 None """
        action_map = {
            (101, 201): 101, (102, 201): 103, (103, 201): 102, 
            (101, 202): 103, (102, 202): 102, (103, 202): 101,
            (101, 203): 999, (102, 203): 999, (103, 203): 999,
            (101, 204): 999, (102, 204): 999, (103, 204): 999, 
            (101, 205): 999, (102, 205): 999, (103, 205): 999,
            (106, 214): 999, (107, 214): 999, (109, 210): 999,
            (110, 210): 999, (110, 211): 999, (110, 212): 999, (110, 213): 999     
        }

        action_ids = {action.action_id for action in actions}

        for (a, b), result in action_map.items():
            if {a, b}.issubset(action_ids):
                # 根據合成結果創建對應的行動
                action_effects = {
                    101: lambda target: target.move_horizontal(),
                    102: lambda target: target.move_vertical(),
                    103: lambda target: target.move_diagonal(),
                    999: lambda target: target.change_anxiety(0),
                }
                action_names = {
                    101: "橫向移動",
                    102: "縱向移動",
                    103: "斜角移動",
                    999: "無此行動"
                }
                combined_action = Action(result, action_names[result], action_effects[result], is_daily_limited=True)
                return combined_action  # ✅ 確保回傳正確的 Action

        return None  # 🚨 若無合成行動，回傳 None


    def get_target_instance(self, target):
        """ 回傳角色或地區物件 """
        print(f"🔍 Debug: 現有地區名稱列表 -> {[a.name for a in self.game.areas]}")
        print(f"🔍 Debug: 嘗試搜尋目標 -> {target}")
        print(f"🔍 Debug: self.game.areas 類型 -> {type(self.game.areas)}")
        
        character = next((c for c in self.game.character_manager.characters if c.name == target), None)
        area = next((a for a in self.game.areas if a.name == target), None)
        print(f"🔍 Debug: 嘗試搜尋 {target} -> 角色: {character}, 地區: {area}")
        if character:
            return character
            # 確保 areas 是列表時，使用 `next()` 搜尋    
        elif area:
            return area
        return None


