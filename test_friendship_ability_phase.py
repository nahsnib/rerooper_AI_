import tkinter as tk
from tkinter import ttk, messagebox
from common.area_and_date import hospital, shrine, city, school, TimeManager
from common.character import Character, CharacterManager, friendship_ignore
from game_phases.player_detective.player_friendship_ability_phase import PlayerFriendshipAbilityPhase
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from database.RuleTable import Role, Ability
from game_gui import GameGUI

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

    characters = [
        Character(1, "男學生", anxiety_threshold=5, initial_location=hospital.id, forbidden_area=None, attributes=['學生'], friendly_abilities=[]),
        Character(2, "女學生", anxiety_threshold=5, initial_location=shrine.id, forbidden_area=None, attributes=['學生'], friendly_abilities=[]),
        Character(3, "刑警", anxiety_threshold=5, initial_location=city.id, forbidden_area=None, attributes=['大人'], friendly_abilities=[]),
        Character(4, "老師", anxiety_threshold=5, initial_location=school.id, forbidden_area=None, attributes=['大人'], friendly_abilities=[]),
    ]
    
    # 添加角色到 character_manager 並設置 pickup 屬性
    for character in characters:
        character.pickup = True  # 假設所有角色都被選中
        character_manager.add_character(character)

    for character in character_manager.get_pickup_characters():
        character.friendship = 1
        character.friendly_abilities.append(
            {
                'id': 1,
                'name': '友好1：自已+1陰謀',
                'trigger': lambda c: c.friendship >= 1,
                'active': True,
                'target_required': False,
                'effect': lambda c: c.change_conspiracy(1),
                'limit_use': False
            }
        )

    for character in character_manager.get_pickup_characters():
        print(f"角色生成: {character.name}, 初始位置: {character.initial_location}")

    black_mastermind = Role(3, "黑幕")
    black_mastermind.add_trait("友好無視")
    black_mastermind.add_ability(Ability(
        "陰謀操控", "主動", "同地區其他角色或地區+1陰謀",
        lambda character, script_writer: (
            target.add_conspiracy(1) if isinstance(target := script_writer.choose_target_or_area(character.current_location)) else target.add_conspiracy(1)
        )
    ))
    character_manager.get_pickup_characters()[0].role_name = black_mastermind.name
    character_manager.get_pickup_characters()[1].role_name = black_mastermind.name

    ability_phase = PlayerFriendshipAbilityPhase(character_manager, game, None)
    action_phase = PlayerDetectiveActionPhase(character_manager)

    game_gui = GameGUI(root, game, character_manager.get_pickup_characters(), ability_phase)
    game_gui.update()
    root.mainloop()

if __name__ == "__main__":
    main()