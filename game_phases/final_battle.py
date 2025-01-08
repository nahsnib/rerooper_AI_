# game_phases/final_battle.py

class FinalBattle:
    def __init__(self, board):
        self.board = board

    def execute(self):
        print("執行最終決戰...")
        # 實現最終決戰邏輯
        for character in self.board.characters:
            if character.alive:
                print(f"{character.name} 參與最終決戰")
                # 在這裡添加更多最終決戰的邏輯
                # 例如，角色使用特別能力或進行決定性行動
