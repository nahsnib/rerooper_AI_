import unittest
from unittest.mock import MagicMock
from game_phases.player_detective.player_detective_ability_phase import PlayerDetectiveAbilityPhase
from common.character import CharacterManager, Character
from database.character_database import load_character_database
from scriptwriter.ai_gameset import AIGameSet

class TestPlayerDetectiveAbilityPhase(unittest.TestCase):
    def setUp(self):
        # 初始化測試環境
        self.character_manager = CharacterManager()
        self.game = MagicMock()
        self.scriptwriter = MagicMock()
        self.phase = PlayerDetectiveAbilityPhase(self.character_manager, self.game, self.scriptwriter)

    def test_can_use_ability(self):
        character = Character("角色A", {"友好無效"})
        ability = {
            'name': '能力A',
            'trigger': lambda character: character.friendship >= 3,
            'active': True,  # 主動能力
            'target_required': False,
            'target_condition': None,
            'limit_use': True  # 限用能力
        }
        character.friendship = 4  # 設置友好值
        character.friendly_ability_usage = {'能力A': False}  # 能力未使用過

        self.assertTrue(self.phase.can_use_ability(character, ability))

        # 使用能力後標記為已使用
        character.friendly_ability_usage['能力A'] = 'used'
        self.assertFalse(self.phase.can_use_ability(character, ability))

        # 測試被動能力
        ability['active'] = False
        self.assertFalse(self.phase.can_use_ability(character, ability))

    def test_reset_ability_usage(self):
        character = Character("角色A", {"友好無效"})
        character.friendly_ability_usage = {'能力A': 'used', '能力B': True}

        self.phase.reset_ability_usage()
        self.assertEqual(character.friendly_ability_usage['能力A'], 'used')  # 限用能力不重置
        self.assertFalse(character.friendly_ability_usage['能力B'])  # 非限用能力重置

    def test_reset_limited_abilities(self):
        character = Character("角色A", {"友好無效"})
        character.friendly_ability_usage = {'能力A': 'used', '能力B': True}

        self.phase.reset_limited_abilities()
        self.assertFalse(character.friendly_ability_usage['能力A'])  # 限用能力重置
        self.assertFalse(character.friendly_ability_usage['能力B'])  # 非限用能力重置

if __name__ == "__main__":
    unittest.main()