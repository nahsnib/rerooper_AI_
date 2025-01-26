import unittest
from unittest.mock import MagicMock
import tkinter as tk
from scriptwriter.ai_gameset import AIGameSet
from common.board import GameBoard, Character, Area
from common.character import CharacterManager
from game_phases.player_detective.player_detective_ability_phase import PlayerDetectiveAbilityPhase, DetectiveAbilityGUI

class TestPlayerDetectiveAbilityPhase(unittest.TestCase):
    def setUp(self):
        # 初始化 Tkinter 根窗口
        self.root = tk.Tk()

        # 初始化 CharacterManager
        self.character_manager = CharacterManager(parent=self.root)

        # 初始化 AIGameSet 並生成劇本
        self.ai_gameset = AIGameSet(self.character_manager)

        # 初始化 GameBoard
        self.game = MagicMock()
        self.game.time_manager = MagicMock()
        self.game.time_manager.remaining_cycles = self.ai_gameset.total_cycles
        self.game.time_manager.total_days = self.ai_gameset.total_days
        self.game.time_manager.current_day = 1
        self.game.scheduled_events = self.ai_gameset.scheduled_events

        self.game_board = GameBoard(root=self.root, game=self.game)
        self.game_board.update()  # 更新 GameBoard 顯示

        # 將所有角色的友好值增加3
        for character in self.character_manager.characters:
            character.change_friendship(3)

        # 初始化 PlayerDetectiveAbilityPhase
        self.phase = PlayerDetectiveAbilityPhase(self.character_manager, self.game, self.ai_gameset)

        # 檢查角色能力，這應該會生成 GUI 並讓我們選擇角色能力
        self.phase.check_abilities()
        self.gui = DetectiveAbilityGUI(self.root, self.phase)

    def tearDown(self):
        self.root.destroy()  # 銷毀根窗口以清理資源

    def test_ability_usage(self):
        # 顯示 GUI 並等待用戶選擇角色和能力
        self.root.mainloop()

if __name__ == "__main__":
    unittest.main()