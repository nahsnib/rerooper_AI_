class Action:
    def __init__(self, id, name, effect, usage_limit=None, is_daily_limited=False):
        self.id = id  # 新增的編號屬性
        self.name = name
        self.effect = effect
        self.usage_limit = usage_limit
        self.times_used = 0

    def can_use(self):
        if self.usage_limit is None:
            return True
        return self.times_used < self.usage_limit

    def use(self):
        if self.can_use():
            self.times_used += 1
            return True
        return False

    def reset(self):
        self.times_used = 0

    def __str__(self):
        return f"Action({self.id}: {self.name}, Used: {self.times_used}/{self.usage_limit})"

# 劇本家的行動列表
scriptwriter_actions = [
    Action(1, "橫向移動", lambda character: character.move_horizontal()),
    Action(2, "縱向移動", lambda character: character.move_vertical()),
    Action(3, "斜角移動", lambda character: character.move_diagonal(), usage_limit=1),
    Action(4, "不安+1 (1)", lambda character: character.change_anxiety(1)),
    Action(5, "不安+1 (2)", lambda character: character.change_anxiety(1)),
    Action(6, "陰謀+1", lambda target: target.change_conspiracy(1)),
    Action(7, "陰謀+2", lambda target: target.change_conspiracy(2), usage_limit=1),
    Action(8, "不安-1", lambda character: character.change_anxiety(-1)),
    Action(9, "不安禁止", lambda character: character.prevent_anxiety_increase()),
    Action(10, "友好禁止", lambda character: character.prevent_friendship_increase())
]

# 偵探的行動列表
detective_actions = [
    Action(11, "橫向移動", lambda character: character.move_horizontal()),
    Action(12, "縱向移動", lambda character: character.move_vertical()),
    Action(13, "禁止移動", lambda character: character.prevent_movement(), usage_limit=1),
    Action(14, "不安+1", lambda character: character.change_anxiety(1)),
    Action(15, "不安-1", lambda character: character.change_anxiety(-1), usage_limit=1),
    Action(16, "友好+1", lambda character: character.change_friendship(1)),
    Action(17, "友好+2", lambda character: character.change_friendship(2), usage_limit=1),
    Action(18, "禁止陰謀", lambda target: target.prevent_conspiracy_increase(), is_daily_limited=True)
]

def get_action_by_id(action_id, role):
    actions = scriptwriter_actions if role == 'scriptwriter' else detective_actions
    for action in actions:
        if action.id == action_id:
            return action
    return None

def display_all_actions(role):
    actions = scriptwriter_actions if role == 'scriptwriter' else detective_actions
    for action in actions:
        print(f"名稱: {action.name}, 描述: {action.description}")

# 測試顯示所有行動
if __name__ == "__main__":
    print("劇本家的行動列表:")
    display_all_actions('scriptwriter')
    print("\n偵探的行動列表:")
    display_all_actions('detective')
