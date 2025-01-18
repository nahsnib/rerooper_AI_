import tkinter as tk
from tkinter import ttk

class Area:
    def __init__(self, id, name):
        self.id = id  # 新增的編號屬性
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
school = Area(1, "學校")
shrine = Area(2, "神社")
city = Area(3, "都市")
hospital = Area(4, "醫院")

# 添加地區到地圖
areas = {
    school.id: school,
    shrine.id: shrine,
    city.id: city,
    hospital.id: hospital,
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

    def update_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        events = self.game.time_manager.get_scheduled_events(self.game.scheduled_events)
        for day, event_name in events.items():
            tk.Label(self.events_frame, text=f"{day}: {event_name}").pack(anchor="w")

    def update(self):
        self.remaining_cycles_label.config(text=str(self.game.time_manager.remaining_cycles))
        self.total_days_label.config(text=str(self.game.time_manager.total_days))
        self.current_day_label.config(text=str(self.game.time_manager.current_day))
        self.update_events()
