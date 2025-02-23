class Action:
    def __init__(self, action_id, name, effect, usage_limit=999, is_daily_limited=False):
        self.action_id = action_id  # 統一命名 action_id，避免與內建 id() 函數衝突
        self.name = name
        self.effect = effect
        self.usage_limit = usage_limit
        self.times_used = 0
        self.is_daily_limited = is_daily_limited
     

    def cycle_reset(self):
        self.times_used = 0


    def __str__(self):
        return f"Action({self.action_id}: {self.name}, Used: {self.times_used}/{self.usage_limit})"




# 劇本家的行動列表
scriptwriter_actions = [
    Action(131, "橫向移動", lambda target: target.move_horizontal(), is_daily_limited=True),
    Action(141, "縱向移動", lambda target: target.move_vertical(), is_daily_limited=True),
    Action(151, "斜角移動", lambda target: target.move_diagonal(), usage_limit=1),
    Action(201, "不安禁止", lambda target: target.change_anxiety(0), is_daily_limited=True),
    Action(211, "不安+1 A", lambda target: target.change_anxiety(1), is_daily_limited=True),
    Action(221, "不安+1 B", lambda target: target.change_anxiety(1), is_daily_limited=True),
    Action(231, "不安-1", lambda target: target.change_anxiety(0), is_daily_limited=True),
    Action(301, "友好禁止", lambda target: target.change_anxiety(0), is_daily_limited=True),
    Action(411, "陰謀+1", lambda target: target.change_conspiracy(1), is_daily_limited=True),
    Action(421, "陰謀+2", lambda target: target.change_conspiracy(2), usage_limit=1),
    Action(999, "無此行動", lambda target: target.change_anxiety(0), usage_limit=0)
]

# 偵探的行動列表
detective_actions = [
    Action(132, "橫向移動", lambda target: target.move_horizontal()),
    Action(142, "縱向移動", lambda target: target.move_vertical()),
    Action(102, "禁止移動 A", lambda target: target.change_anxiety(0), usage_limit=1),
    Action(112, "禁止移動 B", lambda target: target.change_anxiety(0), usage_limit=1),
    Action(122, "禁止移動 C", lambda target: target.change_anxiety(0), usage_limit=1),
    Action(212, "不安+1", lambda target: target.change_anxiety(1)),
    Action(232, "不安-1 A", lambda target: target.change_anxiety(-1), usage_limit=1),
    Action(242, "不安-1 B", lambda target: target.change_anxiety(-1), usage_limit=1),
    Action(252, "不安-1 C", lambda target: target.change_anxiety(-1), usage_limit=1),
    Action(312, "友好+1", lambda target: target.change_friendship(1)),
    Action(322, "友好+2 A", lambda target: target.change_friendship(2), usage_limit=1),
    Action(332, "友好+2 B", lambda target: target.change_friendship(2), usage_limit=1),
    Action(342, "友好+2 C", lambda target: target.change_friendship(2), usage_limit=1),
    Action(402, "禁止陰謀", lambda target: target.change_anxiety(0), is_daily_limited=True)
]

