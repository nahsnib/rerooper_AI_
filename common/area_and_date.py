import tkinter as tk
from tkinter import ttk
from datetime import datetime
from common.character import Character
import copy

# 假設 game_history.py 中的 GameHistory 類已定義
from game_history import GameHistory

class Area:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.characters = []  # 該地區內的角色列表
        self.conspiracy_points = 0  # 該地區的陰謀值

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        self.characters.remove(character)

    def change_conspiracy(self, amount):
        self.conspiracy_points += amount

    def move_horizontal(self):
        pass

    def move_vertical(self):
        pass

    def move_diagonal(self):
        pass

    def move_anywhere(self):
        pass

    def prevent_movement(self):
        pass

    def change_anxiety(self, amount):
        pass

    def change_friendship(self, amount):
        pass


# 定義地區
hospital = Area(1, "醫院")
shrine = Area(2, "神社")
city = Area(3, "鬧區")
school = Area(4, "學校")

# 添加地區到地圖
areas = {
    hospital.id: hospital,
    shrine.id: shrine,
    city.id: city,
    school.id: school,
}

def get_area_by_id(area_id):
    return areas.get(area_id, None)

def display_all_areas():
    for area in areas.values():
        area.display_area_info()

class TimeManager:
    def __init__(self, total_days, total_cycles):
        self.total_days = total_days
        self.total_cycles = total_cycles
        self.current_day = 1
        self.remaining_cycles = total_cycles

    def increment_day(self):
        self.current_day += 1
        if self.current_day > self.total_days:
            self.current_day = 1
            self.remaining_cycles -= 1

    def get_scheduled_events(self, scheduled_events):
        return scheduled_events

