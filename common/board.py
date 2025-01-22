import tkinter as tk
from tkinter import ttk
from datetime import datetime
import copy

# 假設 game_history.py 中的 GameHistory 類已定義
from game_history import GameHistory

class Character:
    def __init__(self, name, friendship=0, anxiety=0, anxiety_threshold=0, conspiracy=0):
        self.name = name
        self.friendship = friendship
        self.anxiety = anxiety
        self.anxiety_threshold = anxiety_threshold
        self.conspiracy = conspiracy

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

class GameBoard:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.game_history = GameHistory()
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

        # 添加顯示遊戲履歷按鈕
        self.history_button = tk.Button(self.frame, text="顯示遊戲履歷", command=self.show_history)
        self.history_button.grid(row=5, column=0, columnspan=2, pady=10)

    def update_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        events = self.game.time_manager.get_scheduled_events(self.game.scheduled_events)
        for day, event_name in events.items():
            tk.Label(self.events_frame, text=f"{day}: {event_name}").pack(anchor="w")

    def create_area_widgets(self):
        # 創建地區顯示區域，設置寬度和高度（假設每個中文字寬度為20像素，高度為20像素）
        self.hospital_frame = tk.LabelFrame(self.areas_frame, text="醫院", padx=10, pady=10, width=7*20, height=5*20)
        self.hospital_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.hospital_frame.grid_propagate(False)  # 防止自動調整大小

        self.shrine_frame = tk.LabelFrame(self.areas_frame, text="神社", padx=10, pady=10, width=7*20, height=5*20)
        self.shrine_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.shrine_frame.grid_propagate(False)  # 防止自動調整大小

        self.city_frame = tk.LabelFrame(self.areas_frame, text="鬧區", padx=10, pady=10, width=7*20, height=5*20)
        self.city_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.city_frame.grid_propagate(False)  # 防止自動調整大小

        self.school_frame = tk.LabelFrame(self.areas_frame, text="學校", padx=10, pady=10, width=7*20, height=5*20)
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
            character_info = (f"{character.name} - ❤{character.friendship} "
                            f"☹{character.anxiety}/{character.anxiety_threshold} "
                            f"☠{character.conspiracy}")
            tk.Label(frame, text=character_info).pack(anchor="w")

    def update(self):
        self.remaining_cycles_label.config(text=str(self.game.time_manager.remaining_cycles))
        self.total_days_label.config(text=str(self.game.time_manager.total_days))
        self.current_day_label.config(text=str(self.game.time_manager.current_day))
        self.update_events()
        self.update_area_widgets()
        self.record_snapshot()

    def record_snapshot(self):
        # 記錄當前 GameBoard 狀態的快照
        gameboard_state = {
            'areas': {area_id: {'conspiracy_points': area.conspiracy_points, 'characters': [c.name for c in area.characters]} for area_id, area in areas.items()},
            'time_manager': {'current_day': self.game.time_manager.current_day, 'remaining_cycles': self.game.time_manager.remaining_cycles}
        }
        timestamp = datetime.now()
        self.game_history.add_snapshot(timestamp, gameboard_state)

    def show_history(self):
        # 創建一個新窗口來顯示遊戲履歷
        history_window = tk.Toplevel(self.root)
        history_window.title("遊戲履歷")

        # 顯示遊戲履歷
        history_text = tk.Text(history_window, wrap="word", width=80, height=20)
        history_text.pack(padx=10, pady=10)

        # 獲取遊戲歷史記錄並顯示
        history = self.game_history.get_history()
        for snapshot in history:
            history_text.insert(tk.END, f"Timestamp: {snapshot['timestamp']}\n")
            history_text.insert(tk.END, "GameBoard State:\n")
            gameboard_state = snapshot['gameboard_state']
            for area, state in gameboard_state['areas'].items():
                history_text.insert(tk.END, f"  - {area}: Conspiracy Points: {state['conspiracy_points']}, Characters: {', '.join(state['characters'])}\n")
            history_text.insert(tk.END, f"Time Manager: Day {gameboard_state['time_manager']['current_day']}, Remaining Cycles: {gameboard_state['time_manager']['remaining_cycles']}\n")
            history_text.insert(tk.END, "\n")