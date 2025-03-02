from common.action import detective_actions, scriptwriter_actions
class Player:
    def __init__(self, identity, available_actions):
        available_actions = available_actions
        self.identity = identity
        self.special_active_ability = {}  # 特殊主動能力（暫時保留）
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
        self.used_actions.clear()

    def cycle_reset_actions(self):
        """輪迴結束時，重置所有可用行動"""
        for action in self.available_actions.values():
            action.reset()
        self.used_actions.clear()
    
def load_players():
    return  {"偵探":Player("偵探", detective_actions),"劇本家": Player("劇本家", scriptwriter_actions)}
