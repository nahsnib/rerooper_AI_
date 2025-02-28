class CycleEnd:
    def __init__(self, game):
        self.game = game

    def display_message(self, message):
        """顯示訊息給玩家"""
        print(message)
        input("點選確定繼續...")

    def prompt_final_battle(self):
        """詢問玩家是否進入最終決戰"""
        response = input("是否要進入最後決戰？（yes/no）: ")
        return response.lower() == 'yes'

    def cycle_reset(self):
        """執行輪迴重置機制"""
        self.game.time_manager.today = 1
        self.game.time_manager.reamin_cycle -= 1

        for event in self.game.event_manager.events:
            event.reset()
        
        for character in self.game.character_manager.get_all_characters():
            character.cycle_reset()
        
        for area in self.game.area_manager.areas:
            area.cycle_reset()
        
        self.game.rule_table.reset_limited_abilities()
        
        self.display_message("輪迴已重置，遊戲回到初始狀態。")

    def execute(self):
        """執行 CycleEnd 階段"""

        # 1. 結束當前 Phase
        self.game.phase_manager.end_current_phase()

        # 2. 執行 passive_ability["cycle_end"]
        self.game.check_passive_ability("cycle_end")

        # 3. 確認勝利條件
        if self.scriptwriter_win_this_cycle:
            self.display_message("劇本家的勝利！")
       
        # 如果有偵探勝利條件（例如所有嫌疑人都揭露），可以在這裡處理
        else:
            self.display_message("偵探獲勝！")


        # 4. 檢查是否還有剩餘輪迴
        if self.game.get_remaining_cycles() == 0:
            self.display_message("進入最終決戰！")
            return "final_battle"
        # 5. 詢問玩家是否提前進入最終決戰
        elif self.prompt_final_battle():
            self.display_message("進入最終決戰！")
            return "final_battle"

        # 6. 剩餘輪迴 -1，並執行 Cycle Reset
        self.cycle_reset()

        # 7. 執行 passive_ability["cycle_start"]
        self.game.check_passive_ability("cycle_start")
        
        return "cycle_reset"

