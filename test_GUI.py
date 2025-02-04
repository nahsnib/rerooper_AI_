import tkinter as tk
from common.area_and_date import hospital, shrine, city, school, TimeManager
from game_gui import GameGUI
from common.character import Character, CharacterManager
from game_phases.player_detective.player_friendship_ability_phase import PlayerFriendshipAbilityPhase
from database.RuleTable import Role, Ability

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
    character_manager = CharacterManager(root)

    # 設置預設角色
    characters = [
        Character(1, "男學生", anxiety_threshold=5, initial_location=hospital.id, forbidden_area=None, attributes=['學生'], friendly_abilities=[]),
        Character(2, "女學生", anxiety_threshold=5, initial_location=shrine.id, forbidden_area=None, attributes=['學生'], friendly_abilities=[]),
        Character(3, "刑警", anxiety_threshold=5, initial_location=city.id, forbidden_area=None, attributes=['大人'], friendly_abilities=[]),
        Character(4, "老師", anxiety_threshold=5, initial_location=school.id, forbidden_area=None, attributes=['大人'], friendly_abilities=[]),
    ]
    character_manager.characters = characters

    # 增加角色的友好度並新增友好能力
    for character in character_manager.characters:
        character.friendship = 1  # 增加友好度
        character.friendly_abilities.append(
            {
                'id': 1,
                'name': '友好1：自已+1陰謀',
                'trigger': lambda character: character.friendship >= 1,
                'active': True,  # 主動能力
                'target_required': False,  # 不需要指定目標
                'effect': lambda target: character.change_conspiracy(1),  # 自已+1陰謀
                'limit_use': False
            }
        )

    # 打印生成的角色信息
    for character in character_manager.characters:
        print(f"角色生成: {character.name}, 初始位置: {character.initial_location}")

    # 創建黑幕身分並分配給角色
    black_mastermind = Role(3, "黑幕")
    black_mastermind.add_trait("友好無視")
    black_mastermind.add_ability(Ability(
        "陰謀操控", "主動", "同地區其他角色或地區+1陰謀",
        lambda character, script_writer: (
            target.add_conspiracy(1) if isinstance(target := script_writer.choose_target_or_area(character.current_location)) else target.add_conspiracy(1)
        )
    ))
    character_manager.characters[0].role_name = black_mastermind.name
    character_manager.characters[1].role_name = black_mastermind.name

    # 初始化能力階段
    ability_phase = PlayerFriendshipAbilityPhase(character_manager, game, None)

    # 初始化並啟動主 GUI
    game_gui = GameGUI(root, game, character_manager.characters, ability_phase)
    game_gui.update()
    root.mainloop()

if __name__ == "__main__":
    main()