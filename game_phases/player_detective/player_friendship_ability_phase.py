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


    def execute(self):
        """啟動 GUI，讓玩家選擇能力"""
        
        self.game_gui.update_friendship_abilities()

    def confirm_ability_selection(self, ability_id):
        """確認選擇的能力"""
        self.selected_ability = next(
            (ability for ability in self.available_abilities if ability.FA_id == ability_id),
            None
        )
        print(f"🔍 Debug: 選擇的能力 = {self.selected_ability}")
        if self.selected_ability:
            if self.selected_ability.target_required:
                self.game_gui.prompt_for_target(self.selected_ability)
            else:
                self.execute_ability()


    def execute_ability(self):
        """執行玩家選擇的友好能力"""
        print(f"🔍 [DEBUG] self.selected_target: {self.selected_target} ({type(self.selected_target)})")

        if self.selected_ability and self.selected_target:
            
            target = self.selected_target  # 取得玩家選擇的目標

            print(f"🎯 正在對 {target.name} 使用 {self.selected_ability.name}")

            # ✅ 確保 `use()` 有傳入 `user` 和 `target`
            success = self.selected_ability.use(self.game, target)
            




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

