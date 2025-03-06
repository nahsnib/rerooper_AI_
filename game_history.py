import tkinter as tk
from tkinter import ttk, messagebox
import copy

class GameHistory:
    def __init__(self):
        self.history = []

    def record_history(self, game):
        """記錄遊戲狀態"""
        self.history.append(copy.deepcopy(game))

    def get_history_choices(self):
        """取得歷史記錄的時間點選項"""
        return [
            f"Loop {game.time_manager.current_cycle} - Day {game.time_manager.current_day} - {game.phase_manager.current_phase}"
            for game in self.history
        ]

    def load_history(self, index):
        """根據索引載入遊戲記錄"""
        if 0 <= index < len(self.history):
            return self.history[index]
        return None

class GameHistoryGUI:
    def __init__(self, root, game, game_history):
        self.root = root
        self.game = game
        self.game_history = game_history  # 遊戲歷史記錄管理
        self.selected_history_index = tk.IntVar(value=-1)

        self.create_widgets()
        self.update_history_choices()

    def create_widgets(self):
        """創建 GUI 元件"""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # 遊戲歷史選擇框
        self.history_frame = tk.LabelFrame(self.main_frame, text="回溯歷史記錄", padx=5, pady=5)
        self.history_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.history_combobox = ttk.Combobox(
            self.history_frame, values=[], state="readonly", width=40
        )
        self.history_combobox.grid(row=0, column=0, padx=5, pady=5)

        self.load_button = tk.Button(
            self.history_frame, text="載入歷史記錄", command=self.load_selected_history
        )
        self.load_button.grid(row=0, column=1, padx=5, pady=5)

    def update_history_choices(self):
        """更新下拉式選單中的歷史記錄"""
        history_choices = self.game_history.get_history_choices()
        self.history_combobox["values"] = history_choices
        if history_choices:
            self.history_combobox.current(0)

    def load_selected_history(self):
        """載入選擇的歷史記錄"""
        selected_index = self.history_combobox.current()
        if selected_index == -1:
            messagebox.showerror("錯誤", "請先選擇一個歷史記錄")
            return

        game_record = self.game_history.load_history(selected_index)
        if game_record:
            self.game = game_record  # 替換當前遊戲狀態
            messagebox.showinfo("成功", "成功回溯至選定的時間點")
        else:
            messagebox.showerror("錯誤", "無法載入選定的歷史記錄")
