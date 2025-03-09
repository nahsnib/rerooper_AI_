import tkinter as tk
from tkinter import ttk, messagebox
import copy

class MiniGame:
    """用於儲存遊戲歷史的輕量版 Game 物件"""
    def __init__(self, game):
        self.time_manager = copy.deepcopy(game.time_manager)  # 時間資訊
        self.EX_gauge = game.EX_gauge  # EX 槽
        self.area_manager = copy.deepcopy(game.area_manager)  # 地區狀態
        self.character_manager = copy.deepcopy(game.character_manager)  # 角色狀態

class Historymanager:
    def __init__(self):
        self.all_history = []
        self.selected_history_index = -1

    def record_history(self, game):
        """記錄遊戲狀態（改為儲存 MiniGame 物件）"""
        self.all_history.append(MiniGame(game))


    def load_history(self, index):
        """根據索引載入遊戲記錄"""
        if 0 <= index < len(self.all_history):
            return self.all_history[index]
        return None

class GameHistoryGUI:
    def __init__(self, history_manager, root, pickup_history=None):
        self.root = root  # ✅ 確保 root 是 Tkinter GUI
        self.history_manager = history_manager
        if not history_manager.all_history:
            messagebox.showerror("錯誤", "目前沒有任何遊戲履歷可查看！")
            root.destroy()  # 直接關閉視窗
            return
        self.pickup_history = pickup_history or history_manager.load_history(0)
        self.selected_history_index = tk.IntVar(value=-1)

        self.create_widgets()
        self.update_history_choices()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # 確保 main_frame 有 3 欄
        self.main_frame.columnconfigure(0, weight=1)  # A 時間
        self.main_frame.columnconfigure(1, weight=2)  # B 地區
        self.main_frame.columnconfigure(2, weight=2)  # C 操作區
        self.create_time_and_area_widgets()

    def create_time_and_area_widgets(self):       
        self.time_frame = tk.Frame(self.main_frame)
        self.time_frame.grid(row=0, column=0, sticky="ns")

        self.area_frame = tk.Frame(self.main_frame)
        self.area_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(self.time_frame, text="剩餘輪迴數量以及當時EX:").pack(anchor="w")
        loop_info = f"{self.pickup_history.time_manager.remaining_cycles} , {self.pickup_history.EX_gauge}"
        self.remaining_cycles_label =  tk.Label(self.time_frame, text=loop_info)
        self.remaining_cycles_label.pack(anchor="w")

        tk.Label(self.time_frame, text="當時日期/總日期").pack(anchor="w")
        date_info = f"{self.pickup_history.time_manager.current_day} / {self.pickup_history.time_manager.total_days}"
        self.date_info_label = tk.Label(self.time_frame, text=date_info)
        self.date_info_label.pack(anchor="w")

    def update_area_widgets(self):
        """更新地區的顯示，包含角色位置與地區資訊"""
        for widget in self.area_frame.winfo_children():
            widget.destroy()  # 清除舊的區域資訊

        areas_info = self.get_area_display_info()
        for i, (area_name, details) in enumerate(areas_info.items()):
            tk.Label(self.area_frame, text=details, relief="solid", padx=10, pady=5).grid(row=i // 2, column=i % 2, sticky="nsew")

    def get_area_display_info(self):
        """獲取所有地區的顯示資訊，包含角色位置、地區陰謀數值與角色狀態（包含死亡狀態）"""
        area_info = {}

        # 建立 name → area 的映射，確保能正確找到區域
        area_by_name = {area.name: area for area in self.pickup_history.area_manager.areas}

        for area_name in ["醫院", "神社", "都市", "學校"]:
            area = area_by_name.get(area_name, None)
            conspiracy_value = area.conspiracy if area else 0
            area_text = f"{area_name} - ☣{conspiracy_value}\n"

            # 找出該區域內的角色
            characters_in_area = self.pickup_history.character_manager.get_characters_in_area(area)
            for char in characters_in_area:
                char_text = f"{char.name}：❤ {char.friendship} || ⚠︎ {char.anxiety}/{char.anxiety_threshold} || ☣{char.conspiracy}"
                
                # **如果角色已死亡，則用刪除線表示**
                if not char.alive:
                    char_text = f"🪦{char_text}"

                area_text += char_text + "\n"

            area_info[area_name] = area_text

        return area_info


    def create_choice_widgets(self):
        # 遊戲歷史選擇框
        self.history_frame = tk.LabelFrame(self.main_frame, text="回溯歷史記錄", padx=5, pady=5)
        self.history_frame.grid(row=0, column=2, columnspan=2, sticky="nsew")

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
        history_choices = self.pickup_history.get_history_choices()
        self.history_combobox["values"] = history_choices
        if history_choices:
            self.history_combobox.current(0)

    def load_selected_history(self):
        """載入選擇的歷史記錄"""
        selected_index = self.history_combobox.current()
        if selected_index == -1:
            messagebox.showerror("錯誤", "請先選擇一個歷史記錄")
            return

        game_record = self.history_manager.load_history(selected_index)
        if game_record:
            self.pickup_history = game_record  # 替換當前遊戲狀態
            messagebox.showinfo("成功", "成功回溯至選定的時間點")
        else:
            messagebox.showerror("錯誤", "無法載入選定的歷史記錄")
