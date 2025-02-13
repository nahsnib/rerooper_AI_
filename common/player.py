class Identity:
    def __init__(self, name, available_actions):
        self.name = name  # "偵探" 或 "劇本家"
        self.available_actions = {action.action_id: action for action in available_actions}  # 存完整的行動
        self.used_actions = set()  # 記錄已使用的行動

    def use_action(self, action_id):
        """標記行動為已使用，並執行行動"""
        action = self.available_actions.get(action_id)
        if action and action.use():  # 確保行動存在並可使用
            self.used_actions.add(action_id)
            return True
        return False  # 行動已被使用或不存在

    def daily_reset_actions(self):
        """夜晚時，重置每日可用行動"""
        for action in self.available_actions.values():
            if action.is_daily_limited:
                action.reset()
        self.used_actions.clear()

    def cycle_reset_actions(self):
        """輪迴結束時，重置所有可用行動"""
        for action in self.available_actions.values():
            action.reset()
        self.used_actions.clear()


class Player:
    def __init__(self, identity_name):
        available_actions = self.initialize_actions(identity_name)
        self.identity = Identity(identity_name, available_actions)
        self.special_actions = {}  # 特殊能力（暫時保留）

    @staticmethod
    def initialize_actions(identity_name):
        """根據玩家身份獲取對應的可用行動"""
        from common.action import detective_actions, scriptwriter_actions
        return detective_actions if identity_name == "偵探" else scriptwriter_actions
