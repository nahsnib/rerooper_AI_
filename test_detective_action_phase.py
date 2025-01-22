import unittest
from unittest.mock import MagicMock
from scriptwriter.ai_gameset import AIGameSet
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from common.character import CharacterManager

class TestDetectiveActionPhase(unittest.TestCase):
    def setUp(self):
        # 模擬角色管理器
        self.root = MagicMock()
        self.character_manager = CharacterManager(self.root)
        
        # 加載角色
        self.character_manager.load_characters()
        
        # 初始化 AIGameSet，建構模擬版面
        self.game_set = AIGameSet(self.character_manager)
        
        # 初始化 PlayerDetectiveActionPhase
        self.action_phase = PlayerDetectiveActionPhase(self.character_manager)

    def test_action_phase(self):
        # 測試 Action Phase 的啟動和執行
        self.action_phase.execute()
        
        # 確保 selected_targets 不為空
        self.assertTrue(self.action_phase.selected_targets)

if __name__ == '__main__':
    unittest.main()