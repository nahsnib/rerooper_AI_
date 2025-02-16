import random
from common.character import CharacterManager
from common.player import Player
from game_gui import GameGUI

class PlayerFriendshipAbilityPhase:
    def __init__(self, game, game_gui):
        self.game = game
        self.game_gui = game_gui
        self.phase_type = "friendship"  # ✅ 新增此屬性
        self.selected_ability = None
        self.selected_target = None
        self.available_abilities = []
        self.available_targets = []


    def execute(self):
        """啟動 GUI，讓玩家選擇能力"""
        
        self.game_gui.update_FA_selection()

    def update_available_abilities(self):
        """更新可用的友好能力"""
        self.available_abilities = [
            ability for character in self.game.character_manager.characters 
            if character.alive  # 檢查角色是否存活
            for ability in character.friendship_abilities 
            if ability.is_available(character)
        ]

    def confirm_FA_selection(self, fa_name):
        """確認選擇的能力"""
        self.selected_ability = next(
            (ability for ability in self.available_abilities if ability.name == fa_name),
            None
        )
        print(f"🔍 [DEBUG] self.selected_ability: {self.selected_ability}")

        # 🔒 鎖定能力選擇
        if self.selected_ability != None:
            self.game_gui.ability_combobox["state"] = "disabled"
            self.game_gui.confirm_FA_button["state"] = "disabled"

        # 更新可用目標列表
        self.update_available_targets()

    def update_available_targets(self):
        """依據選擇的能力，更新可用目標列表"""
        owner = self.selected_ability.get_owner_by_name(self.game)
        # 取得符合 target_condition 的角色
        self.available_targets = [
            char.name for char in self.game.character_manager.characters
            if self.selected_ability.target_condition(char, owner)
        ]
        # 如果是 FA_id=401（巫女移除陰謀），則額外將神社加入可用目標
        if self.selected_ability.FA_id == 401:
            self.available_targets.append(self.game.area_manager.area[2])

        # 如果是 FA_id=1201（神格揭露犯人），則額外將事件加入可用目標
        if self.selected_ability.FA_id == 1201:
            for event in self.game.scheduled_events.values():
                if event.criminal_name:
                    self.available_targets.append(event)

        # 如果是 FA_id=1202（神格移除陰謀），則額外將當前地區加入可用目標        
        if self.selected_ability.FA_id == 1202:
            current_location = self.game.area_manager.fetch_area_by_name(self.current_character.current_location)
            if current_location:
                self.available_targets.append(current_location.name)

        # 更新 GUI
        self.game_gui.update_FA_targets_selection()
     

    def confirm_FA_target_selection(self, target_name):
        """確認目標後，執行能力"""

        if not target_name:
            self.ability_combobox["state"] = "normal"  # 解鎖能力選擇
            return

        # 🟢 1.嘗試尋找角色作為目標
        self.selected_target = next((c for c in self.game.character_manager.characters if c.name == target_name), None)

        # 🟢 2.嘗試尋找地區作為目標
        if not self.selected_target:
            selected_target = self.game.area_manager.fetch_area_by_name(target_name)

        # 🟢 3.嘗試尋找事件作為目標.
        if not self.selected_target:
            print(f"🎯 選擇的目標: {target_name}")
            event_names = [e.name for e in self.game.scheduled_events.values()]
            print(f"📋 目前遊戲中的事件名稱: {event_names}")
            if not selected_target:
                selected_target = next((e for e in self.game.scheduled_events.values() if e.name == target_name), None)
            print(f"🎯 選擇的目標: {selected_target}")

        # 🟢 4.嘗試尋找行動作為目標
        if not self.selected_target:
            self.selected_target = next(
                (a for a in self.game.players["偵探"].identity.available_actions.values() if a.name == target_name), None)
        # 🔴 如果仍然找不到，顯示錯誤訊息
        if not self.selected_target:
            print(f"⚠️ 無法找到名為 {target_name} 的目標")
            return

        # 如果能力需要額外選擇，則更新額外選擇
        if self.selected_ability.require_extra_selection:
            self.update_extra_selection()
            self.confirm_extra_selection()
        else:
            self.execute_ability()

    def update_extra_selection(self):
        """更新額外選擇"""
        # 如果是 FA_id=
        self.game_gui.update_extra_selection()

    def confirm_extra_selection(self):
        """執行額外選擇"""
        if self.selected_ability and self.selected_target:
            target = self.selected_target
            ability = self.selected_ability

            print(f"🎯 需要額外選擇，正在對 {target.name} 使用 {ability.name}")

            # 讓玩家做額外選擇
            extra_choice = target.anxiety_ctrl(self.game)
            if extra_choice is not None:
                self.execute_ability(extra_choice)  # 最終執行能力

    def execute_ability(self, extra_choice=None):
        
        """執行玩家選擇的友好能力"""
        print(f"🔍 [DEBUG] self.selected_target: {self.selected_target} ({type(self.selected_target)})")

        if self.selected_ability and self.selected_target:
            
            target = self.selected_target  # 取得玩家選擇的目標

            # ✅ 確保 `use()` 有傳入 `user` 和 `target`
            self.selected_ability.use(self.game, target, extra_choice)
            
            # 🟢 確保能力存在於列表內再移除
            if self.selected_ability in self.available_abilities:
                self.available_abilities.remove(self.selected_ability)

            # 清除已選擇的能力與目標
            self.selected_ability = None
            self.selected_target = None

            # ✅ 確保更新 GUI，而非錯誤呼叫
            if hasattr(self.game_gui, "update_friendship_abilities"):
                self.game_gui.update_friendship_abilities()
            else:
                print("⚠️ 無法更新友好能力清單，請確認 GUI 是否正確初始化！")





    def end_phase(self):
        """結束友好能力階段"""
        self.game_gui.show_message("結束友好能力階段")

