class Player:
    def __init__(self, identity, available_actions):
        self.identity = identity  # "偵探" 或 "劇本家"
        self.available_actions = {action.action_id: action for action in available_actions}  # 可用的行動
        self.used_actions = set()  # 記錄已使用的行動
        self.special_actions = {}  # 特殊能力（暫時保留，日後設計）

    def use_action(self, action_id):
        """標記行動為已使用，並執行行動"""
        if action_id in self.available_actions:
            action = self.available_actions[action_id]
            if action.use():  # 直接調用 Action 內的 use()
                self.used_actions.add(action_id)
                return True  # 成功使用行動
        return False  # 行動已被使用或不存在

    def daily_reset_actions(self):
        """夜晚時，重置每日可用行動"""
        for action in self.available_actions.values():
            if action.is_daily_limited:  # 只重置每日限制的行動
                action.reset()
        self.used_actions.clear()

    def cycle_reset_actions(self):
        """輪迴結束時，重置所有可用行動"""
        for action in self.available_actions.values():
            action.reset()  # 重置所有行動
        self.used_actions.clear()
