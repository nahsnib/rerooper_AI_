import tkinter as tk
from common.character import CharacterManager
from common.area_and_date import Area, hospital, shrine, city, school, TimeManager
from common.character import Character, CharacterManager
from game_phases.player_detective.player_detective_ability_phase import PlayerDetectiveAbilityPhase
from GameGUI import DetectiveAbilityGUI
import tkinter as tk
from database.Basecharacter import load_character_database, BaseCharacter
from database.RuleTable import Role, Ability, get_rule_table_by_id



def create_character_manager(root):
    character_manager = CharacterManager(root)
    characters = load_character_database()
    character_manager.characters = [Character(**char.__dict__) for char in characters]
    return character_manager

# 從角色列表中引用男學生和女學生
def get_characters(character_manager):
    male_student = next(character for character in character_manager.characters if character.name == '男學生')
    female_student = next(character for character in character_manager.characters if character.name == '女學生')
    return male_student, female_student

# 從 RuleTable 中引用黑幕身分
def create_black_mastermind_role():
    black_mastermind = Role(3, "黑幕")
    black_mastermind.add_trait("友好無視")
    black_mastermind.add_ability(Ability(
        "陰謀操控", "主動", "同地區其他角色或地區+1陰謀",
        lambda character, script_writer: (
            target.add_conspiracy(1) if isinstance(target := script_writer.choose_target_or_area(character.current_location)) else target.add_conspiracy(1)
        )
    ))
    return black_mastermind

# 設定角色的身分
def assign_role_to_character(character, role):
    character.role_name = role.name
    character.traits = role.traits
    character.role_abilities = role.abilities

# 初始化遊戲對象和腳本家對象
class MockGame:
    def __init__(self):
        self.time_manager = TimeManager(total_days=30, total_cycles=3)
        self.scheduled_events = {
            1: "事件A",
            5: "事件B",
            10: "事件C"
        }
        self.action_cards = []

if __name__ == "__main__":
    root = tk.Tk()

    # 初始化角色管理器
    character_manager = create_character_manager(root)

    # 獲取男學生和女學生
    male_student, female_student = get_characters(character_manager)

    # 創建黑幕身分並分配給角色
    black_mastermind = create_black_mastermind_role()
    assign_role_to_character(male_student, black_mastermind)
    assign_role_to_character(female_student, black_mastermind)

    # 初始化遊戲對象和腳本家對象
    game = MockGame()
    scriptwriter = None  # 初始化劇本家對象

    # 初始化能力階段
    phase = PlayerDetectiveAbilityPhase(character_manager, game, scriptwriter)

    # 啟動能力階段的 GUI
    gui = DetectiveAbilityGUI(root, phase)
    root.mainloop()