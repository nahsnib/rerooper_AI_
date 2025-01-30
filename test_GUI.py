import tkinter as tk
from common.area_and_date import hospital, shrine, city, school, TimeManager
from GameGUI import GameGUI
from common.character import Character, CharacterManager
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from game_phases.player_detective.player_detective_ability_phase import PlayerDetectiveAbilityPhase

# 模擬遊戲對象
class MockGame:
    def __init__(self):
        self.time_manager = TimeManager(total_days=30, total_cycles=3)
        self.scheduled_events = {
            1: "事件A",
            5: "事件B",
            10: "事件C"
        }

def main():
    root = tk.Tk()
    root.title("測試遊戲版圖")

    game = MockGame()
    character_manager = CharacterManager(root)

    # 設置預設角色
    characters = [
        Character(1, "男學生", anxiety_threshold=5, initial_location=hospital.id, forbidden_area=None, attributes=['學生'], friendly_abilities=[]),
        Character(2, "女學生", anxiety_threshold=5, initial_location=shrine.id, forbidden_area=None, attributes=['學生'], friendly_abilities=[]),
        Character(3, "刑警", anxiety_threshold=5, initial_location=city.id, forbidden_area=None, attributes=['大人'], friendly_abilities=[]),
        Character(4, "老師", anxiety_threshold=5, initial_location=school.id, forbidden_area=None, attributes=['大人'], friendly_abilities=[]),
    ]
    character_manager.characters = characters

    # 初始化行動階段或友好能力階段
    action_phase = PlayerDetectiveActionPhase(character_manager)
    # ability_phase = PlayerDetectiveAbilityPhase(character_manager, game, None)

    # 初始化並啟動主 GUI
    game_gui = GameGUI(root, game, character_manager.characters, action_phase)
    # game_gui = GameGUI(root, game, character_manager.characters, ability_phase)
    game_gui.update()
    root.mainloop()

if __name__ == "__main__":
    main()