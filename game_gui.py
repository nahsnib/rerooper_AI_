import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from game_history import GameHistoryGUI, Historymanager

class GameGUI:
    def __init__(self, root, game,  phase=None):  # ✅ 預設 phase=None
        self.root = root
        self.game = game
        self.phase = phase  # 可以是 None
        self.selected_targets = []

        self.game_history = Historymanager()   # 🔥 創建遊戲歷史記錄管理

        self.ask_popup = None  # 🔹 用來存放詢問視窗
        self.ask_result = None  # 🔹 用來存放玩家選擇（True/False）
        self.create_widgets()
        self.area_frame.grid()  # 確保地區資訊顯示
        self.update_area_widgets()  # ✅ 這行非常重要！
        self.create_action_phase_widgets()
        self.create_ability_widgets()

        # 🔥 設定 `phase_manager` 讓它知道如何記錄歷史
        self.game.phase_manager.set_history_callback(self.record_game_history)

    def set_phase(self, phase):
        self.phase = phase
        print(phase.phase_type)
        # 🟢 行動階段
        if self.phase.phase_type == "action":

            self.update_action_combobox_values()
            self.ability_frame.grid_remove() 
            self.action_phase_frame.grid()

        # 🔵 友好能力階段
        elif self.phase.phase_type == "FA":
            self.update_FA_selection()
            self.action_phase_frame.grid_remove() 
            self.ability_frame.grid()

        else:
            self.action_phase_frame.grid_remove() 
            self.ability_frame.grid_remove() 

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # 確保 main_frame 有 3 欄
        self.main_frame.columnconfigure(0, weight=1)  # A 時間
        self.main_frame.columnconfigure(1, weight=2)  # B 地區
        self.main_frame.columnconfigure(2, weight=2)  # C 行動階段

        self.create_time_and_area_widgets()

    def create_time_and_area_widgets(self):       
        self.time_frame = tk.Frame(self.main_frame)
        self.time_frame.grid(row=0, column=0, sticky="ns")

        self.area_frame = tk.Frame(self.main_frame)
        self.area_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(self.time_frame, text="使用劇本表:").pack(anchor="w")
        self.remaining_cycles_label = tk.Label(self.time_frame, text=str(self.game.selected_rule_table.name))
        self.remaining_cycles_label.pack(anchor="w")

        tk.Label(self.time_frame, text="剩餘輪迴數量以及當前EX:").pack(anchor="w")
        loop_info = f"{self.game.time_manager.remaining_cycles} , {self.game.EX_gauge}"
        self.remaining_cycles_label =  tk.Label(self.time_frame, text=loop_info)
        self.remaining_cycles_label.pack(anchor="w")


        tk.Label(self.time_frame, text="當前日期/總日期").pack(anchor="w")
        date_info = f"{self.game.time_manager.current_day} / {self.game.time_manager.total_days}"
        self.date_info_label = tk.Label(self.time_frame, text=date_info)
        self.date_info_label.pack(anchor="w")

        tk.Label(self.time_frame, text="安排事件的日期和名稱:").pack(anchor="w")
        self.events_frame = tk.Frame(self.time_frame)
        self.events_frame.pack(anchor="w")
        self.update_events()

        # 🔽 新增 "已公開情報" 標籤 🔽
        tk.Label(self.time_frame, text="📢 已公開情報：").pack(anchor="w")

        # 🔽 創建滾動視窗來顯示公開資訊 🔽
        self.info_frame = tk.Frame(self.time_frame)
        self.info_frame.pack(fill="both", expand=True)

        self.info_text = tk.Text(self.info_frame, height=6, width=40, wrap="word")
        self.info_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.info_frame, orient="vertical", command=self.info_text.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.info_text.config(yscrollcommand=self.scrollbar.set, state="disabled")  # 讓內容不可編輯

        # 🔽 新增「啟動遊戲履歷」按鈕 🔽
        self.history_button = tk.Button(self.time_frame, text="啟動遊戲履歷", command=self.show_game_history)
        self.history_button.pack(anchor="w", pady=5)



    def update_public_information(self):
        """更新公開資訊的滾動顯示"""
        self.info_text.config(state="normal")  # 允許寫入
        self.info_text.delete("1.0", tk.END)  # 清除舊內容
        for info in self.game.public_information:
            self.info_text.insert(tk.END, info + "\n")  # 加入新資訊
        self.info_text.config(state="disabled")  # 設定為不可編輯

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
        area_by_name = {area.name: area for area in self.game.area_manager.areas}

        for area_name in ["醫院", "神社", "都市", "學校"]:
            area = area_by_name.get(area_name, None)
            conspiracy_value = area.conspiracy if area else 0
            area_text = f"{area_name} - ☣{conspiracy_value}\n"

            # 找出該區域內的角色
            characters_in_area = [char for char in self.game.character_manager.characters if char.current_location == area_name]
            for char in characters_in_area:
                char_text = f"{char.name}：❤ {char.friendship} || ⚠︎ {char.anxiety}/{char.anxiety_threshold} || ☣{char.conspiracy}"
                
                # **如果角色已死亡，則用刪除線表示**
                if not char.alive:
                    char_text = f"🪦{char_text}"

                area_text += char_text + "\n"

            area_info[area_name] = area_text

        return area_info

    def update_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()  # 清除舊的事件顯示

        events = self.game.time_manager.get_scheduled_events(self.game.scheduled_events)

        # **按照日期順序顯示事件**
        for date in range(1, self.game.time_manager.total_days + 1):  # 從第 1 天到最後一天
            if date in events:  # **確保該日期有對應的事件**
                event = events[date]  # **直接取得該日期的事件**
                tk.Label(self.events_frame, text=f"{date}: {event.name}").pack(anchor="w")





    def create_action_phase_widgets(self):
        self.action_phase_frame = tk.Frame(self.main_frame)
        self.action_phase_frame.grid(row=0, column=2, columnspan=2, sticky="nsew")

        self.scriptwriter_frame = tk.LabelFrame(self.action_phase_frame, text="劇本家的行動", padx=5, pady=5)
        self.scriptwriter_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.scriptwriter_actions_label = tk.Label(self.scriptwriter_frame, text="等待劇本家行動...", wraplength=300, justify=tk.LEFT)
        self.scriptwriter_actions_label.grid(row=0, column=0, padx=5, pady=5)

        self.player_frame = tk.LabelFrame(self.action_phase_frame, text="偵探的行動", padx=5, pady=5)
        self.player_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.action_target_vars = []
        self.action_comboboxes = []
        self.action_target_comboboxes = []

        for i in range(3):
            choice_frame = tk.Frame(self.player_frame)
            choice_frame.grid(row=i, column=0, columnspan=2, sticky="nsew", padx=5, pady=2)

            action_target_var = tk.StringVar()
            action_target_combobox = ttk.Combobox(choice_frame, textvariable=action_target_var, values=[], width=15)
            action_target_combobox.grid(row=0, column=0, padx=2)
            self.action_target_vars.append(action_target_var)
            self.action_target_comboboxes.append(action_target_combobox)  # ✅ 這行確保 target_combobox 可被更新


            action_var = tk.StringVar()
            action_combobox = ttk.Combobox(choice_frame, textvariable=action_var, values= [],  width=15)
            action_combobox.grid(row=0, column=1, padx=2)
            self.action_comboboxes.append(action_combobox)

        self.confirm_action_button = tk.Button(self.player_frame, text="確認行動", 
                                command=lambda: self.phase.confirm_action_selection() if self.phase else None)

        self.confirm_action_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_scriptwriter_actions(self, scriptwriter_selections):
        actions_text = "劇本家的行動目標：\n"
        for i, selection in enumerate(scriptwriter_selections, 1):
            actions_text += f"{i}. 目標：{selection['target']}\n"
        self.scriptwriter_actions_label.config(text=actions_text)

    def update_action_combobox_values(self):
        """當 phase 被設置後，更新行動選單"""
        if not self.phase or not hasattr(self.phase, "game"):
            print("❌ Phase 或 game 不存在，無法更新行動選單")
            return  # 確保 phase 和 game 存在

        detective = self.phase.game.players.get("偵探")
        
        if detective:
            available_actions = [action.name for action in detective.available_actions.values() if action.times_used < action.usage_limit]
            #print(f"✅ 更新 GUI 選單，偵探可用行動: {available_actions}")  # 🛠 除錯用
            for action_combobox in self.action_comboboxes:
                action_combobox["values"] = available_actions
                action_combobox.set(available_actions[0] if available_actions else "")  # 重新設定選單值

            available_action_targets = self.phase.get_available_action_targets()
            #print(f"✅ 更新目標選單，可選目標: {available_action_targets}")  # 🛠 除錯用
            for action_target_combobox in self.action_target_comboboxes:  # ✅ 改成 `self.action_target_comboboxes`
                action_target_combobox["values"] = available_action_targets
                action_target_combobox.set(available_action_targets[0] if available_action_targets else "")  # 重新設定選單值            
           
        else:
            print("❌ 無法找到偵探玩家")
        
        
    def create_ability_widgets(self):
        self.ability_frame = tk.LabelFrame(self.main_frame, text="友好能力", padx=5, pady=5)
        self.ability_frame.grid(row=0, column=2, columnspan=2, sticky="nsew")
        self.ability_frame.grid_remove()  # ✅ 預設隱藏，不會影響 layout

    def update_FA_selection(self):
        """顯示所有可用的友好能力（不區分角色）"""
        self.ability_frame.grid()  # ✅ 顯示友好能力框架
        for widget in self.ability_frame.winfo_children():
            widget.destroy()

        # 更新可用能力列表
        self.phase.update_available_abilities()
        
        # 建立下拉選單：能力
        self.ability_var = tk.StringVar()
        self.ability_combobox = ttk.Combobox(
            self.ability_frame, textvariable=self.ability_var,
            values=[ability.name for ability in self.phase.available_abilities]
        )
        self.ability_combobox.pack()

        # 確認按鈕，使用 lambda 來確保選擇的能力名稱正確傳入 phase
        self.confirm_FA_button = tk.Button(
            self.ability_frame, text="確認能力",
            command=lambda: self.phase.confirm_FA_selection(self.ability_var.get())
        )
        self.confirm_FA_button.pack()

        # 選擇下拉式選單：目標
        self.FA_target_var = tk.StringVar()
        self.FA_target_combobox = ttk.Combobox(self.ability_frame, textvariable=self.FA_target_var)
        self.FA_target_combobox.pack()

        self.confirm_FA_target_button = tk.Button(
            self.ability_frame, text="確認目標",
            command=lambda: self.phase.confirm_FA_target_selection(self.FA_target_var.get())
        )
        self.confirm_FA_target_button.pack()

        # 🟢 選擇下拉式選單：額外
        self.extra_var = tk.StringVar()
        self.extra_combobox = ttk.Combobox(self.ability_frame, textvariable=self.extra_var)
        self.extra_combobox.pack()

        self.extra_selected_choice = None  # 用來存儲選擇的結果
        self.extra_selection_done = False  # 用來追蹤是否按下確認


        self.confirm_extra_button = tk.Button(
            self.ability_frame, text="確認額外選擇",
            command=lambda: self.phase.confirm_extra_selection(self.extra_var.get())
        )
        self.confirm_extra_button.pack()

        # 🟢 加入「結束友好能力階段」按鈕
        self.end_button = tk.Button(
            self.ability_frame, text="結束友好能力階段",
            command=lambda: self.phase.on_end(),
            fg="white", bg="red", font=("Arial", 12, "bold")
        )
        self.end_button.pack()


    def update_FA_targets_selection(self):
        """依據選擇的能力，更新可用目標列表"""
        self.FA_target_combobox["values"] = [target for target in self.phase.available_targets]

    def update_extra_selection(self, choices):
        """
        讓玩家在 GUI 中選擇額外選項，並回傳選擇結果。
        
        :param message: 提示訊息
        :param choices: 可供選擇的選項（字典，鍵值相同）
        :return: 玩家選擇的選項（或 None）
        """
        # 更新選單內容
        self.extra_combobox["values"] = choices
        self.extra_combobox.pack()  # 顯示選擇框
        self.confirm_extra_button.pack()  # 顯示確認按鈕
        

        # 重置選擇狀態
        self.extra_selected_choice = None
        self.extra_selection_done = False

        # 等待玩家選擇（使用主迴圈）
        while not self.extra_selection_done:
            self.root.update()  # 更新 UI，防止卡死

        return choices.get(self.extra_selected_choice)  # 回傳選擇的數值


    def ask_player(self, target, reason):
        """依據輸入的reason，判斷要問什麼問題"""
        
        # 確保不會有多個視窗
        if hasattr(self, "ask_popup") and self.ask_popup:
            self.ask_popup.destroy()

        # 創建詢問視窗
        self.ask_popup = tk.Toplevel(self.root)
        self.ask_popup.geometry("300x150")
        self.ask_popup.transient(self.root)  # 讓視窗始終在主視窗上方
        self.ask_popup.grab_set()   # 讓玩家只能操作這個視窗

        # 設定標題與內容
        self.ask_popup.title("詢問玩家")
        ask_messages = {
            502: "是否要讓刑警拯救 {target_name} ？",
            "final_battle": "是否要直接進入最終決戰？"
        }
        message = ask_messages.get(reason, "是否要進行這個動作？").format(target_name=target.name)
        
        label = tk.Label(self.ask_popup, text=message, wraplength=250)
        label.pack(pady=10)

        # 建立按鈕
        button_frame = tk.Frame(self.ask_popup)
        button_frame.pack()

        yes_button = tk.Button(button_frame, text="是", width=10, command=partial(self.set_ask_result, True))
        yes_button.pack(side="left", padx=10, pady=5)

        no_button = tk.Button(button_frame, text="否", width=10, command=partial(self.set_ask_result, False))
        no_button.pack(side="right", padx=10, pady=5)

        self.ask_popup.wait_window()  # 等待玩家選擇
        return self.ask_result  # 回傳玩家選擇結果

    def set_ask_result(self, result):
        """儲存玩家選擇結果並關閉視窗"""
        self.ask_result = result
        if self.ask_popup and self.ask_popup.winfo_exists():
            self.ask_popup.destroy()
        self.ask_popup = None

    def show_message(self, message):
        messagebox.showinfo("訊息", message)
    
    def show_error(self, message):
        messagebox.showerror("錯誤", message)
    
    def show_game_history(self):
        """開啟遊戲履歷 GUI"""
        history_window = tk.Toplevel(self.root)  # ✅ 創建新視窗
        history_window.title("遊戲履歷")
        history_window.geometry("500x200")  # ✅ 設定大小

        # ✅ 正確傳遞 `root` 和 `game_history`
        GameHistoryGUI(self.game_history, history_window)


    def record_game_history(self):
        """記錄遊戲歷史"""
        self.game_history.record_history(self.game)  # 🔥 記錄當前遊戲狀態