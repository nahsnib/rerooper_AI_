
from common.action import Action

class PlayerDetectiveActionPhase:
    def __init__(self, game):
        self.game = game  # 整合 Game，讓 Phase 可以存取玩家
        self.phase_type = "action"  # ✅ 新增此屬性
        self.scriptwriter_selections = []  # AI 劇本家的行動
        self.player_selections = []  # 玩家偵探的行動
    
    def execute(self):
        """ 執行整個行動階段，先讓劇本家選擇行動，然後請求玩家輸入 """
        self.scriptwriter_select_actions()  # 讓 AI 劇本家選擇行動
        self.game.game_gui.update_scriptwriter_actions(self.scriptwriter_selections)
        
        # 請求玩家輸入

    def scriptwriter_select_actions(self):
        scriptwriter = self.game.players["劇本家"]
        selected_targets = []
        
        for _ in range(3):
            available_targets = self.get_available_action_targets()  # 每次更新可用目標
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
    
    def select_target_by_priority(self, targets):
        """ 劇本家 AI 根據優先順序選擇目標（焦慮值高的角色優先） """
        character_manager = self.game.character_manager
        character_dict = {c.name: c for c in character_manager.characters}
        highest_anxiety = -1
        priority_target = None
        
        for target in targets:
            if target in character_dict and target != "幻象": # 不可對幻象設置行動
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
            if action.times_used < action.usage_limit:
                return action
        return None

    def get_available_action_targets(self):
        """ 獲取所有可用的目標（角色 + 地區） """
        targets = [char.name for char in self.game.character_manager.characters if char.alive]
        targets.extend(["醫院", "神社", "都市", "學校"])
        if "幻象" in targets:
            targets.remove("幻象")  # 不可對幻象設置行動

        return tuple(targets)

    def confirm_action_selection(self):
        selections = []
        invalid_selection = False
        used_actions = set()  # 紀錄本回合內已使用的行動
        character_seted = set()  # 紀錄本回合已經被偵探設置行動過的對象

        for i in range(3):
            target = self.game.game_gui.action_target_vars[i].get()
            action_name = self.game.game_gui.action_comboboxes[i].get()
            action = next((a for a in self.game.players["偵探"].available_actions.values() if a.name == action_name), None)
            if target and action:
                if action.times_used >= action.usage_limit:  # 檢查限用能力是否超出使用次數
                    invalid_selection = True
            
                if action.usage_limit == 1 and action_name in used_actions: # 檢查限用能力，一天不可用兩次
                    print(f"行動「{action_name}」一輪迴只能使用一次！")
                    invalid_selection = True

                if action.is_daily_limited and action_name in used_actions: # daily_limited檢查
                    print(f"行動「{action_name}」一天只能使用一次！")
                    invalid_selection = True
                
                if target in character_seted: # 不可以對同一個目標設置兩個行動
                    print(f"目標「{target}」不可以設置複數行動！")
                    invalid_selection = True

                selections.append({"target": target, "action": action})
                used_actions.add(action_name)  # 標記該行動已選擇
                character_seted.add(target)
            else:
                invalid_selection = True  # 標記有錯誤，等迴圈結束再處理
        if invalid_selection:
            print("請選擇有效的目標和行動")
            return  # 停止執行
        if selections:
            self.player_selections = selections
        else:
            return  # ✅ 玩家選擇無效，應該重新選擇，而不是繼續執行
        self.execute_actions()  # ✅ 直接執行
        self.game.game_gui.show_message(f"選擇了行動：{[action['action'].name for action in self.player_selections]}，目標：{[action['target'] for action in self.player_selections]}")


    def execute_actions(self):
        """執行所有行動（AI + 玩家），按照遊戲的結算順序處理"""
        all_actions = self.scriptwriter_selections + self.player_selections
        # ✅ 按照目標整理行動
        action_dict = {}
        for selection in all_actions:
            target_name = selection["target"]
            target = self.game.character_manager.get_character_by_name(target_name)
            if not target:
                target = self.game.area_manager.fecth_area_by_name(target_name)
            action = selection["action"]
            if target_name not in action_dict:
                action_dict[target] = []
            action_dict[target].append(action)

        # ✅ 開始按照行動 ID 排序執行行動
        for target, actions in sorted(action_dict.items(), key=lambda x: min(a.action_id for a in x[1])):
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
                action.effect(target)
        self.game.game_gui.update_area_widgets()  # ✅ 更新區域資訊
        self.on_end()  

    def combine_action(self, actions):
        """ 根據規則合成行動，若無合成則回傳 None """
        action_map = {
            (131, 132): 131, (141, 132): 151, (151, 132): 142, # 橫/綜/斜 + 橫 = 橫/斜/縱
            (131, 142): 151, (141, 142): 141, (151, 142): 132, # 橫/綜/斜 + 縱 = 斜/縱/橫
            (131, 102): 999, (141, 102): 999, (151, 102): 999, # 禁止移動A
            (131, 112): 999, (141, 112): 999, (151, 112): 999, # 禁止移動B
            (131, 122): 999, (141, 122): 999, (151, 122): 999, # 禁止移動C
            (212, 201): 999, (411, 402): 999, (421, 402): 999, # 禁止不安、陰謀
            (301, 312): 999, (301, 322): 999, (301, 332): 999, (301, 342): 999     # 禁止友好
        }

        action_ids = {action.action_id for action in actions}

        for (a, b), result in action_map.items():
            if {a, b}.issubset(action_ids):
                # 根據合成結果創建對應的行動
                action_effects = {
                    131: lambda target: target.move_horizontal(),
                    141: lambda target: target.move_vertical(),
                    151: lambda target: target.move_diagonal(),
                    999: lambda target: None,
                }
                action_names = {
                    131: "橫向移動",
                    141: "縱向移動",
                    151: "斜角移動",
                    999: "無此行動"
                }
                combined_action = Action(result, action_names[result], action_effects[result], is_daily_limited=True)
                return combined_action  # ✅ 確保回傳正確的 Action

        return None  # 🚨 若無合成行動，回傳 None

    def on_start(self):
        print("行動階段開始")
    
    def on_end(self):
        """行動階段結束，通知 phase_manager 進入下一個階段"""
        print("行動階段結束，清除暫存數據")
        
        # 🟢 1. 清理行動紀錄（如有需要）
        #self.clear_action_records()
        
        # 🟢 2. 讓 phase_manager 進入下一個階段
        self.game.phase_manager.advance_phase()
        


