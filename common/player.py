class Player:
    def __init__(self, role, actions):
        self.role = role
        self.defeat_flags = set()  # 用於存儲敗北旗標
        self.actions = actions

    def set_defeat_flag(self, flag):
        self.defeat_flags.add(flag)

    def check_defeat_flags(self):
        return len(self.defeat_flags) > 0
    
    def choose_actions(self, board):
        # 選擇行動的邏輯（這裡可以使用玩家輸入或AI來選擇）
        chosen_actions = []
        for action in self.actions:
            if action.can_use():
                # 假設這裡選擇了某個角色為目標
                target = self.select_target(board)
                if action.use():
                    chosen_actions.append((action, target))
        return chosen_actions

    def select_target(self, board):
        # 選擇目標的邏輯（這裡可以使用玩家輸入或AI來選擇）
        # 這是一個簡單的示例，實際上應根據遊戲狀態來選擇
        return board.characters[0]

    def use_abilities(self, board):
        # 使用能力的邏輯（根據角色的特殊能力）
        pass

    def apply_special_effects(self, game):
        # 檢查主規則和副規則的特殊效果
        for rule in game.rule_table.main_rules + game.rule_table.sub_rules:
            rule.apply_special_effect(game)
