import tkinter as tk
from tkinter import ttk

class Character:
    def __init__(self, name):
        self.name = name

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

    def add_conspiracy_points(self, points):
        self.conspiracy_points += points

    def remove_conspiracy_ban(self):
        # 移除陰謀禁止卡片的邏輯
        pass

    def display_area_info(self):
        print(f"地區編號: {self.id}")
        print(f"名稱: {self.name}")
        print(f"陰謀值: {self.conspiracy_points}")
        print("角色:")
        for character in self.characters:
            print(f"  - {character.name}")

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

def display_all_areas():
    for area in areas.values():
        area.display_area_info()

def get_area_by_id(area_id):
    return areas.get(area_id, None)

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

class GameBoard:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # 剩餘輪迴數量
        tk.Label(self.frame, text="剩餘輪迴數量:").grid(row=0, column=0, sticky="w")
        self.remaining_cycles_label = tk.Label(self.frame, text=str(self.game.time_manager.remaining_cycles))
        self.remaining_cycles_label.grid(row=0, column=1, sticky="w")

        # 預定的總日期
        tk.Label(self.frame, text="預定的總日期:").grid(row=1, column=0, sticky="w")
        self.total_days_label = tk.Label(self.frame, text=str(self.game.time_manager.total_days))
        self.total_days_label.grid(row=1, column=1, sticky="w")

        # 今天的日期
        tk.Label(self.frame, text="今天的日期:").grid(row=2, column=0, sticky="w")
        self.current_day_label = tk.Label(self.frame, text=str(self.game.time_manager.current_day))
        self.current_day_label.grid(row=2, column=1, sticky="w")

        # 安排事件的日期和名稱
        tk.Label(self.frame, text="安排事件的日期和名稱:").grid(row=3, column=0, sticky="w")
        self.events_frame = tk.Frame(self.frame)
        self.events_frame.grid(row=4, column=0, columnspan=2, sticky="w")

        self.update_events()

        # 地區顯示
        self.areas_frame = tk.Frame(self.root)
        self.areas_frame.pack(padx=10, pady=10)

        self.create_area_widgets()

    def update_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        events = self.game.time_manager.get_scheduled_events(self.game.scheduled_events)
        for day, event_name in events.items():
            tk.Label(self.events_frame, text=f"{day}: {event_name}").pack(anchor="w")

    def create_area_widgets(self):
        # 創建地區顯示區域，設置寬度和高度
        self.hospital_frame = tk.LabelFrame(self.areas_frame, text="醫院", padx=10, pady=10, width=400, height=150)
        self.hospital_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.hospital_frame.grid_propagate(False)  # 防止自動調整大小

        self.shrine_frame = tk.LabelFrame(self.areas_frame, text="神社", padx=10, pady=10, width=400, height=150)
        self.shrine_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.shrine_frame.grid_propagate(False)  # 防止自動調整大小

        self.city_frame = tk.LabelFrame(self.areas_frame, text="鬧區", padx=10, pady=10, width=400, height=150)
        self.city_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.city_frame.grid_propagate(False)  # 防止自動調整大小

        self.school_frame = tk.LabelFrame(self.areas_frame, text="學校", padx=10, pady=10, width=400, height=150)
        self.school_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.school_frame.grid_propagate(False)  # 防止自動調整大小

        self.update_area_widgets()

    def update_area_widgets(self):
        # 清除現有的地區顯示
        for widget in self.hospital_frame.winfo_children():
            widget.destroy()
        for widget in self.shrine_frame.winfo_children():
            widget.destroy()
        for widget in self.city_frame.winfo_children():
            widget.destroy()
        for widget in self.school_frame.winfo_children():
            widget.destroy()

        # 更新地區顯示
        self.update_area_info(self.hospital_frame, hospital)
        self.update_area_info(self.shrine_frame, shrine)
        self.update_area_info(self.city_frame, city)
        self.update_area_info(self.school_frame, school)

    def update_area_info(self, frame, area):
        tk.Label(frame, text=f"陰謀值: {area.conspiracy_points}").pack(anchor="w")
        tk.Label(frame, text="角色:").pack(anchor="w")
        for character in area.characters:
            tk.Label(frame, text=f"  - {character.name}").pack(anchor="w")

    def update(self):
        self.remaining_cycles_label.config(text=str(self.game.time_manager.remaining_cycles))
        self.total_days_label.config(text=str(self.game.time_manager.total_days))
        self.current_day_label.config(text=str(self.game.time_manager.current_day))
        self.update_events()
        self.update_area_widgets()

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
    Action(4, "不安+1 (A)", lambda character: character.change_anxiety(1), is_daily_limited=True),
    Action(5, "不安+1 (B)", lambda character: character.change_anxiety(1), is_daily_limited=True),
    Action(6, "陰謀+1", lambda target: target.change_conspiracy(1), is_daily_limited=True),
    Action(7, "陰謀+2", lambda target: target.change_conspiracy(2), usage_limit=1),
    Action(8, "不安-1", lambda character: character.change_anxiety(-1), is_daily_limited=True),
    Action(9, "不安禁止", lambda character: character.prevent_anxiety_increase(), is_daily_limited=True),
    Action(10, "友好禁止", lambda character: character.prevent_friendship_increase(), is_daily_limited=True)
]

# 偵探的行動列表
detective_actions = [
    Action(11, "橫向移動", lambda character: character.move_horizontal()),
    Action(12, "縱向移動", lambda character: character.move_vertical()),
    Action(13, "禁止移動", lambda character: character.prevent_movement(), usage_limit=3),
    Action(14, "不安+1", lambda character: character.change_anxiety(1)),
    Action(15, "不安-1", lambda character: character.change_anxiety(-1), usage_limit=3),
    Action(16, "友好+1", lambda character: character.change_friendship(1)),
    Action(17, "友好+2", lambda character: character.change_friendship(2), usage_limit=3),
    Action(18, "禁止陰謀", lambda target: target.prevent_conspiracy_increase(), is_daily_limited=True)
]