import tkinter as tk
from common.board import GameBoard, TimeManager, hospital, shrine, city, school, Character

# 模擬遊戲對象
class MockGame:
    def __init__(self):
        self.time_manager = TimeManager(total_days=30, total_cycles=3)
        self.scheduled_events = {
            1: "事件A",
            5: "事件B",
            10: "事件C"
        }

# 創建測試窗口
def main():
    root = tk.Tk()
    root.title("測試遊戲版圖")

    game = MockGame()
    game_board = GameBoard(root, game)

    # 更新測試角色數據
    hospital.add_character(Character("男學生"))
    shrine.add_character(Character("女學生"))
    city.add_character(Character("刑警"))
    school.add_character(Character("老師"))

    # 更新顯示
    game_board.update()

    root.mainloop()

if __name__ == "__main__":
    main()