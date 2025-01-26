import tkinter as tk
from common.board import GameBoard, TimeManager, hospital, shrine, city, school
from scriptwriter.ai_gameset import AIGameSet
from common.character import CharacterManager, Character

# 模擬遊戲對象
class MockGame:
    def __init__(self, time_manager, scheduled_events):
        self.time_manager = time_manager
        self.scheduled_events = scheduled_events

# 創建測試窗口
def main():
    root = tk.Tk()
    root.title("測試遊戲版圖")

    # 初始化 CharacterManager
    character_manager = CharacterManager(parent=root)

    # 初始化 AIGameSet 並生成劇本
    ai_gameset = AIGameSet(character_manager)

    # 初始化 TimeManager 和 MockGame
    time_manager = TimeManager(total_days=ai_gameset.total_days, total_cycles=ai_gameset.total_cycles)
    game = MockGame(time_manager, ai_gameset.scheduled_events)

    # 初始化 GameBoard
    game_board = GameBoard(root, game, ai_gameset.characters)  # 傳遞選擇的角色

    # 將生成的角色分配到地區
    areas = [hospital, shrine, city, school]
    for i, character in enumerate(ai_gameset.characters):
        area = areas[i % len(areas)]
        area.add_character(character)

    # 更新顯示
    game_board.update()

    root.mainloop()

if __name__ == "__main__":
    main()