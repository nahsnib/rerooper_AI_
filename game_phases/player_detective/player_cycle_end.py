class CycleEnd:
    def __init__(self, game):
        self.game = game
    
    def check_scriptwriter_defeat(self):
        """
        檢查劇本家是否敗北。
        若敗北，則宣布偵探勝利，並結束遊戲。
        """
        if self.game.scriptwriter.is_defeated():
            print("劇本家敗北，偵探獲勝！")
            self.game.end_game(winner="detective")
            return True
        return False
    
    def check_cycle_count(self):
        """
        檢查剩餘輪迴數量，若為 0，則遊戲結束，並判定勝負。
        """
        if self.game.remaining_cycles <= 0:
            print("輪迴結束，判定遊戲勝負。")
            self.game.end_game(winner=self.determine_winner())
            return True
        return False
    
    def determine_winner(self):
        """
        判定最終勝利者，根據遊戲規則決定。
        """
        if self.game.scriptwriter.has_won():
            return "scriptwriter"
        else:
            return "detective"
    
    def execute(self):
        """
        執行 Cycle 結束時的檢查。
        """
        print("進行 Cycle 結束檢查...")
        if self.check_scriptwriter_defeat():
            return
        if self.check_cycle_count():
            return
        
        print("輪迴尚未結束，進入下一天。")
        self.game.start_new_day()

if __name__ == "__main__":
    # 測試用例 (假設有一個 Game 物件)
    game = None  # 這裡需要替換成實際的 Game 物件
    cycle_end = CycleEnd(game)
    cycle_end.execute()
