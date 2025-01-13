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

class GameBoard:
    def __init__(self, root, game, character_manager):
        self.root = root
        self.game = game
        self.character_manager = character_manager
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # 剩餘輪迴數量
        tk.Label(self.frame, text="剩餘輪迴數量:").grid(row=0, column=0, sticky="w")
        self.remaining_cycles_label = tk.Label(self.frame, text=str(self.game.remaining_cycles))
        self.remaining_cycles_label.grid(row=0, column=1, sticky="w")

        # 預定的總日期
        tk.Label(self.frame, text="預定的總日期:").grid(row=1, column=0, sticky="w")
        self.total_days_label = tk.Label(self.frame, text=str(self.game.total_days))
        self.total_days_label.grid(row=1, column=1, sticky="w")

        # 今天的日期
        tk.Label(self.frame, text="今天的日期:").grid(row=2, column=0, sticky="w")
        self.current_day_label = tk.Label(self.frame, text=str(self.game.day_counter))
        self.current_day_label.grid(row=2, column=1, sticky="w")

        # 安排事件的日期和名稱
        tk.Label(self.frame, text="安排事件的日期和名稱:").grid(row=3, column=0, sticky="w")
        self.events_frame = tk.Frame(self.frame)
        self.events_frame.grid(row=4, column=0, columnspan=2, sticky="w")

        self.update_events()

        # 顯示地區和角色
        self.areas_frame = tk.Frame(self.frame)
        self.areas_frame.grid(row=5, column=0, columnspan=2, sticky="w")
        self.update_areas()

    def update_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        events = self.game.get_scheduled_events()
        for day, event_name in events.items():
            tk.Label(self.events_frame, text=f"{day}: {event_name}").pack(anchor="w")

    def update_areas(self):
        for widget in self.areas_frame.winfo_children():
            widget.destroy()
        
        for area in self.character_manager.get_all_areas():
            area_frame = tk.Frame(self.areas_frame)
            area_frame.pack(fill="both", expand=True, padx=5, pady=5, anchor="w")
            tk.Label(area_frame, text=f"{area.name} ({area.conspiracy_points} ☠)").pack(anchor="w")
            for character in area.characters:
                char_btn = tk.Button(
                    area_frame, text=f"{character.name} (❤ {character.friendship}) (☹ {character.anxiety}) (☠ {character.conspiracy})",
                    command=lambda c=character: self.on_character_click(c)
                )
                char_btn.pack(anchor="w")

    def on_character_click(self, character):
        # Handle character click
        print(f"Clicked on {character.name}")
        # Here you can add additional logic to handle character actions or abilities

    def update(self):
        self.remaining_cycles_label.config(text=str(self.game.remaining_cycles))
        self.total_days_label.config(text=str(self.game.total_days))
        self.current_day_label.config(text=str(self.game.day_counter))
        self.update_events()
        self.update_areas()
