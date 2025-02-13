class Action:
    def __init__(self, action_id, name, effect, usage_limit=None, is_daily_limited=False):
        self.action_id = action_id  # 統一命名 action_id，避免與內建 id() 函數衝突
        self.name = name
        self.effect = effect
        self.usage_limit = usage_limit
        self.times_used = 0
        self.is_daily_limited = is_daily_limited
       


    def can_use(self):
        if self.usage_limit is None:
            return True
        return self.times_used < self.usage_limit

    def use(self):
        if self.can_use():
            self.times_used += 1
            return True
        return False


    def __str__(self):
        return f"Action({self.action_id}: {self.name}, Used: {self.times_used}/{self.usage_limit})"


def reset_chosen_action(game_gui, player):
    """讓玩家選擇一個已經用過的【1輪迴只能使用1次】的行動，並重置它"""
    used_limited_actions = {
        action.name: action
        for action in player.role.available_actions.values()
        if action.usage_limit == 1 and action.times_used > 0
    }

    # 如果沒有可重置的行動，則直接返回
    if not used_limited_actions:
        game_gui.show_message("沒有可重置的行動。")
        return

    # 讓玩家選擇要重置的行動
    choice = game_gui.prompt_choice(
        message="要重置哪一個行動？",
        choices={**used_limited_actions, "取消": None}
    )

    if choice is not None:
        choice.times_used = 0

# 劇本家的行動列表
scriptwriter_actions = [
    Action(101, "橫向移動", lambda target: target.move_horizontal(), is_daily_limited=True),
    Action(102, "縱向移動", lambda target: target.move_vertical(), is_daily_limited=True),
    Action(103, "斜角移動", lambda target: target.move_diagonal(), usage_limit=1),
    Action(104, "不安+1 A", lambda target: target.change_anxiety(1), is_daily_limited=True),
    Action(105, "不安+1 B", lambda target: target.change_anxiety(1), is_daily_limited=True),
    Action(106, "陰謀+1", lambda target: target.change_conspiracy(1), is_daily_limited=True),
    Action(107, "陰謀+2", lambda target: target.change_conspiracy(2), usage_limit=1),
    Action(108, "不安-1", lambda target: target.change_anxiety(0), is_daily_limited=True),
    Action(109, "不安禁止", lambda target: target.change_anxiety(0), is_daily_limited=True),
    Action(110, "友好禁止", lambda target: target.change_anxiety(0), is_daily_limited=True),
    Action(999, "無此行動", lambda target: target.change_anxiety(0), usage_limit=0)
]

# 偵探的行動列表
detective_actions = [
    Action(201, "橫向移動", lambda target: target.move_horizontal()),
    Action(202, "縱向移動", lambda target: target.move_vertical()),
    Action(203, "禁止移動 A", lambda target: target.change_anxiety(0), usage_limit=1),
    Action(204, "禁止移動 B", lambda target: target.change_anxiety(0), usage_limit=1),
    Action(205, "禁止移動 C", lambda target: target.change_anxiety(0), usage_limit=1),
    Action(206, "不安+1", lambda target: target.change_anxiety(1)),
    Action(207, "不安-1 A", lambda target: target.change_anxiety(-1), usage_limit=1),
    Action(208, "不安-1 B", lambda target: target.change_anxiety(-1), usage_limit=1),
    Action(209, "不安-1 C", lambda target: target.change_anxiety(-1), usage_limit=1),
    Action(210, "友好+1", lambda target: target.change_friendship(1)),
    Action(211, "友好+2 A", lambda target: target.change_friendship(2), usage_limit=1),
    Action(212, "友好+2 B", lambda target: target.change_friendship(2), usage_limit=1),
    Action(213, "友好+2 C", lambda target: target.change_friendship(2), usage_limit=1),
    Action(214, "禁止陰謀", lambda target: target.change_anxiety(0), is_daily_limited=True)
]

