import tkinter as tk
from common.area_and_date import Area, hospital, shrine, city, school, Character, TimeManager
from GameGUI import GameGUI
from common.character import CharacterManager

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
    character_manager = CharacterManager(parent=root)

    characters = [
        Character(1, "男學生", anxiety_threshold=5, initial_location=hospital.id, forbidden_area=None, attributes={}, friendly_abilities=[]),
        Character(2, "女學生", anxiety_threshold=5, initial_location=shrine.id, forbidden_area=None, attributes={}, friendly_abilities=[]),
        Character(3, "刑警", anxiety_threshold=5, initial_location=city.id, forbidden_area=None, attributes={}, friendly_abilities=[]),
        Character(4, "老師", anxiety_threshold=5, initial_location=school.id, forbidden_area=None, attributes={}, friendly_abilities=[]),
    ]

    area_and_time = Area(game, characters)
    game_gui = GameGUI(root, game, characters)

    # 更新顯示
    game_gui.update()

    root.mainloop()

if __name__ == "__main__":
    main()