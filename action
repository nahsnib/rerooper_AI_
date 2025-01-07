class Action:
    def __init__(self, name, effect, usage_limit=None):
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
        return f"Action({self.name}, Used: {self.times_used}/{self.usage_limit})"
# 劇本家的行動列表
scriptwriter_actions = [
    Action("橫向移動", lambda character: character.move_horizontal()),
    Action("縱向移動", lambda character: character.move_vertical()),
    Action("斜角移動", lambda character: character.move_diagonal(), usage_limit=1),
    Action("不安+1", lambda character: character.change_anxiety(1), usage_limit=2),
    Action("陰謀+1", lambda target: target.change_conspiracy(1)),
    Action("陰謀+2", lambda target: target.change_conspiracy(2), usage_limit=1),
    Action("不安-1", lambda character: character.change_anxiety(-1)),
    Action("不安禁止", lambda character: character.prevent_anxiety_increase()),
    Action("友好禁止", lambda character: character.prevent_friendship_increase())
]

# 偵探的行動列表
detective_actions = [
    Action("橫向移動", lambda character: character.move_horizontal()),
    Action("縱向移動", lambda character: character.move_vertical()),
    Action("禁止移動", lambda character: character.prevent_movement(), usage_limit=1),
    Action("不安+1", lambda character: character.change_anxiety(1)),
    Action("不安-1", lambda character: character.change_anxiety(-1), usage_limit=1),
    Action("友好+1", lambda character: character.change_friendship(1)),
    Action("友好+2", lambda character: character.change_friendship(2), usage_limit=1),
    Action("禁止陰謀", lambda target: target.prevent_conspiracy_increase())
]
