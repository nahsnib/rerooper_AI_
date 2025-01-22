import unittest
from unittest.mock import MagicMock
from game_phases.player_detective.player_detective_ability_phase import PlayerDetectiveAbilityPhase
from common.character import CharacterManager, Character
from database.character_database import load_character_database
from scriptwriter.ai_gameset import AIGameSet

class TestPlayerDetectiveAbilityPhase(unittest.TestCase):
    def setUp(self):
        # 模擬角色管理器
        self.root = MagicMock()
        self.character_manager = CharacterManager(self.root)

        # 加載角色
        characters_data = load_character_database()
        self.characters = []
        for char_data in characters_data:
            character = Character(**char_data.__dict__)  # 使用角色的字典來初始化
            character.friendship = 3  # 確保友好度足夠高以啟用能力
            self.character_manager.characters.append(character)
            self.characters.append(character)

        # 初始化 AIGameSet
        self.game_set = MagicMock()
        self.game_set.change_anxiety = MagicMock() # 模擬 change_anxiety 方法
        
        # 初始化 PlayerDetectiveAbilityPhase
        self.scriptwriter = MagicMock()
        self.phase = PlayerDetectiveAbilityPhase(self.character_manager, self.game_set, self.scriptwriter)

    def test_check_abilities(self):
        # 測試檢查能力
        self.phase.check_abilities()
        self.assertGreater(len(self.phase.active_abilities), 0)

    def test_check_friendship_ignore(self):
        # 測試檢查友好無效
        character = self.characters[0]
        self.assertTrue(self.phase.check_friendship_ignore(character))

    def test_choose_ability(self):
        # 測試選擇能力
        character = self.characters[0]
        self.phase.check_abilities()
        self.assertGreater(len(self.phase.active_abilities), 0)

    def test_execute_ability(self):
        # 測試執行能力
        self.phase.check_abilities()
        if len(self.phase.active_abilities) > 0:
            character, ability = self.phase.active_abilities[0]
            self.phase.execute_ability(character, ability)
            self.assertTrue(character.friendly_ability_usage[ability['name']])
        else:
            self.fail("No active abilities found")

    def test_get_character_by_name(self):
        # 測試根據名稱獲取角色
        character_name = self.characters[0].name
        character = self.phase.get_character_by_name(character_name)
        self.assertEqual(character.__dict__, self.characters[0].__dict__)  # 比較對象的屬性

if __name__ == "__main__":
    unittest.main()