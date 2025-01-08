
# game_phases/night_phase.py

class NightPhase:
    def __init__(self, board):
        self.board = board

    def execute(self):
        print("執行夜晚階段...")
        # 實現夜晚階段邏輯
        for character in self.board.characters:
            if character.alive:
                print(f"{character.name} 在夜晚階段進行行動")
                # 在這裡添加更多夜晚階段的邏輯
                # 例如，角色進行秘密行動或事件觸發
