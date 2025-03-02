class CycleEnd:
    def __init__(self, game):
        self.game = game
        self.phase_type = "cycle_end"
        
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
        self.game.reset_game_state()

    def execute(self):
        """執行 CycleEnd 階段"""

        # 2. 執行 passive_ability["cycle_end"]
        self.game.check_passive_ability("cycle_end")

        # 3. 確認勝利條件
        if self.game.scriptwriter_win_this_cycle:
            self.display_message("劇本家的勝利！")
       
        # 如果有偵探勝利條件（例如所有嫌疑人都揭露），可以在這裡處理
        else:
            self.display_message("偵探獲勝！")


        # 4. 檢查是否還有剩餘輪迴
        if self.game.time_manager.remaining_cycles == 0:
            self.display_message("進入最終決戰！")
            self.game.phase_manager.run_final_battle

        # 5. 詢問玩家是否提前進入最終決戰
        elif self.prompt_final_battle():
            self.display_message("進入最終決戰！")
            self.game.phase_manager.run_final_battle

        # 6. 剩餘輪迴 -1，並執行 Cycle Reset
        else: 
            self.cycle_reset()
            self.game.check_passive_ability("cycle_start")
            self.on_end()
        # 7. 執行 passive_ability["cycle_start"]

    def on_end(self):
        print("輪迴重置完成，清除暫存數據")
        self.game.phase_manager.advance_phase()
        # 這裡可以清除行動記錄、計算效果等