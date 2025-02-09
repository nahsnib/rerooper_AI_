
import random

class AIScriptWriter:
    def __init__(self, game):
        self.game = game
    
    def decide_action_target(self, action_name, available_targets):
        """
        根據當前遊戲狀況與可用目標，決定應該選擇的對象。
        
        :param action_name: 操作名稱（例如 '殺死一個角色'）
        :param available_targets: 可選擇的角色列表
        :return: 被選擇的目標角色
        """
        if not available_targets:
            print(f"⚠ 操作 '{action_name}' 沒有可用目標，動作無效！")
            return None
        
        chosen_target = random.choice(available_targets)
        print(f"🎯 AI 選擇的 '{action_name}' 目標: {chosen_target.name}")
        return chosen_target
