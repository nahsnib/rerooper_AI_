import tkinter as tk
from tkinter import ttk

# common/actions.py

class Action:
    def __init__(self, id, name, effect, usage_limit=None, is_daily_limited=False):
        self.id = id
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

    def reset(self):
        self.times_used = 0

    def __str__(self):
        return f"Action({self.id}: {self.name}, Used: {self.times_used}/{self.usage_limit})"

# 劇本家的行動列表
scriptwriter_actions = [
    Action(1, "橫向移動", lambda character: character.move_horizontal(), is_daily_limited=True),
    Action(2, "縱向移動", lambda character: character.move_vertical(), is_daily_limited=True),
    Action(3, "斜角移動", lambda character: character.move_diagonal(), usage_limit=1),
    Action(4, "不安+1 A", lambda character: character.change_anxiety(1), is_daily_limited=True),
    Action(5, "不安+1 B", lambda character: character.change_anxiety(1), is_daily_limited=True),
    Action(6, "陰謀+1", lambda target: target.change_conspiracy(1), is_daily_limited=True),
    Action(7, "陰謀+2", lambda target: target.change_conspiracy(2), usage_limit=1),
    Action(8, "不安-1", lambda character: character.change_anxiety(-1), is_daily_limited=True),
    Action(9, "不安禁止", lambda: None, is_daily_limited=True),
    Action(10, "友好禁止", lambda: None, is_daily_limited=True)
]

# 偵探的行動列表
detective_actions = [
    Action(11, "橫向移動", lambda character: character.move_horizontal()),
    Action(12, "縱向移動", lambda character: character.move_vertical()),
    Action(13, "禁止移動 A", lambda: None, usage_limit=1),
    Action(14, "禁止移動 B", lambda: None, usage_limit=1),
    Action(15, "禁止移動 C", lambda: None, usage_limit=1),
    Action(16, "不安+1", lambda character: character.change_anxiety(1)),
    Action(17, "不安-1 A", lambda character: character.change_anxiety(-1), usage_limit=1),
    Action(18, "不安-1 B", lambda character: character.change_anxiety(-1), usage_limit=1),
    Action(19, "不安-1 C", lambda character: character.change_anxiety(-1), usage_limit=1),
    Action(20, "友好+1", lambda character: character.change_friendship(1)),
    Action(21, "友好+2 A", lambda character: character.change_friendship(2), usage_limit=1),
    Action(22, "友好+2 B", lambda character: character.change_friendship(2), usage_limit=1),
    Action(23, "友好+2 C", lambda character: character.change_friendship(2), usage_limit=1),
    Action(24, "禁止陰謀", lambda: None, is_daily_limited=True)
]