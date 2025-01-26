import tkinter as tk
from tkinter import ttk, messagebox
from common.area_and_date import hospital, shrine, city, school, TimeManager, areas
from common.character import CharacterManager
from common.action import Action, detective_actions
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase

class GameGUI:
    def __init__(self, root, game, characters, action_phase):
        self.root = root
        self.game = game
        self.characters = characters  # 只顯示選擇的角色
        self.action_phase = action_phase
        self.selected_targets = []
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

        # 添加行動階段的 GUI
        self.action_phase_frame = tk.Frame(self.root)
        self.action_phase_frame.pack(padx=10, pady=10)
        self.create_action_phase_widgets()

    def update_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        events = self.game.time_manager.get_scheduled_events(self.game.scheduled_events)
        sorted_events = sorted(events.items())  # 按照日期排序事件

        for day, event in sorted_events:
            tk.Label(self.events_frame, text=f"{day}: {event}").pack(anchor="w")  # 直接使用 event 作為字符串

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
        for character in self.characters:
            if character.current_location == area.id:  # 只顯示在當前地區的角色
                character_info = (f"{character.name} - ❤{character.friendship} "
                                f"☹{character.anxiety}/{character.anxiety_threshold} "
                                f"☠{character.conspiracy}")
                tk.Label(frame, text=character_info).pack(anchor="w")

    def show_history(self):
        # 創建一個新窗口來顯示遊戲履歷
        history_window = tk.Toplevel(self.root)
        history_window.title("遊戲履歷")

        # 顯示遊戲履歷
        history_text = tk.Text(history_window, wrap="word", width=80, height=20)
        history_text.pack(padx=10, pady=10)

        # 獲取遊戲歷史記錄並顯示
        history = self.area_and_time.get_game_history()
        for snapshot in history:
            history_text.insert(tk.END, f"Timestamp: {snapshot['timestamp']}\n")
            history_text.insert(tk.END, "GameBoard State:\n")
            gameboard_state = snapshot['gameboard_state']
            for area, state in gameboard_state['areas'].items():
                history_text.insert(tk.END, f"  - {area}: Conspiracy Points: {state['conspiracy_points']}, Characters: {', '.join([c.name for c in state['characters']])}\n")
            history_text.insert(tk.END, f"Time Manager: Day {gameboard_state['time_manager']['current_day']}, Remaining Cycles: {gameboard_state['time_manager']['remaining_cycles']}\n")
            history_text.insert(tk.END, "\n")

    def create_action_phase_widgets(self):
        # 創建行動階段的 GUI 元件
        self.action_phase_label = tk.Label(self.action_phase_frame, text="行動階段：選擇目標和行動")
        self.action_phase_label.pack()

        self.target_vars = []
        self.action_vars = []

        for i in range(3):
            target_label = tk.Label(self.action_phase_frame, text=f"第{i + 1}選擇 目標")
            target_label.pack()
            target_var = tk.StringVar()
            target_combobox = ttk.Combobox(self.action_phase_frame, textvariable=target_var, values=self.get_available_targets())
            target_combobox.pack()
            self.target_vars.append(target_var)

            action_label = tk.Label(self.action_phase_frame, text=f"第{i + 1}選擇 行動")
            action_label.pack()
            action_var = tk.StringVar()
            action_combobox = ttk.Combobox(self.action_phase_frame, textvariable=action_var, values=[action.name for action in detective_actions])
            action_combobox.pack()
            self.action_vars.append(action_var)

        self.confirm_button = tk.Button(self.action_phase_frame, text="確認", command=self.confirm_selection)
        self.confirm_button.pack()

    def get_available_targets(self):
        targets = []
        characters = self.characters
        if characters is None:
            raise ValueError("Characters could not be loaded.")
        for character in characters:
            targets.append(character.name)
        for area_id, area in areas.items():
            targets.append(area.name)
        return targets

    def confirm_selection(self):
        self.selected_targets = []
        for i in range(3):
            target = self.target_vars[i].get()
            action_name = self.action_vars[i].get()
            action = next((a for a in detective_actions if a.name == action_name), None)

            if target and action:
                self.selected_targets.append({"target": target, "action": action})
            else:
                messagebox.showerror("錯誤", "請選擇有效的目標和行動")
                return

        if self.action_phase.receive_detective_selection(self.selected_targets):
            # 執行完操作後更新GUI
            self.update()
        else:
            messagebox.showerror("錯誤", "選擇不符合規則，請重新選擇")
            self.reset_selection()

    def reset_selection(self):
        self.selected_targets = []
        for target_var in self.target_vars:
            target_var.set('')
        for action_var in self.action_vars:
            action_var.set('')

    def update(self):
        self.remaining_cycles_label.config(text=str(self.game.time_manager.remaining_cycles))
        self.total_days_label.config(text=str(self.game.time_manager.total_days))
        self.current_day_label.config(text=str(self.game.time_manager.current_day))
        self.update_events()
        self.update_area_widgets()