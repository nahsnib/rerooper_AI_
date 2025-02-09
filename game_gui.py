import tkinter as tk
from tkinter import ttk, messagebox

class GameGUI:
    def __init__(self, root, game, characters, phase=None):  # ✅ 預設 phase=None
        self.root = root
        self.game = game
        self.characters = characters
        self.phase = phase  # 可以是 None
        self.selected_targets = []
        self.create_widgets()

    def set_phase(self, phase):
        self.phase = phase
        
        # 🟢 行動階段
        if self.phase.phase_type == "action":
            print(f"🎯 設定遊戲階段: {type(self.phase).__name__}")  # 🛠 除錯用
            self.update_action_combobox_values()
            self.ability_frame.grid_remove()
            self.action_phase_frame.grid()

        # 🔵 友好能力階段
        elif self.phase.phase_type == "friendship":
            self.update_friendship_abilities()
            self.action_phase_frame.grid_remove()
            self.ability_frame.grid()

        self.area_frame.grid()  # 確保地區資訊顯示
        self.update_area_widgets()  # ✅ 這行非常重要！

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # 確保 main_frame 有 3 欄
        self.main_frame.columnconfigure(0, weight=1)  # A 時間
        self.main_frame.columnconfigure(1, weight=2)  # B 地區
        self.main_frame.columnconfigure(2, weight=2)  # C 行動階段

        self.create_time_and_area_widgets()
        self.create_action_phase_widgets()
        self.create_ability_widgets()


    def create_time_and_area_widgets(self):

        
        self.time_frame = tk.Frame(self.main_frame)
        self.time_frame.grid(row=0, column=0, sticky="ns")

        self.area_frame = tk.Frame(self.main_frame)
        self.area_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(self.time_frame, text="剩餘輪迴數量:").pack(anchor="w")
        self.remaining_cycles_label = tk.Label(self.time_frame, text=str(self.game.time_manager.remaining_cycles))
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
        """獲取所有地區的顯示資訊，包含角色位置與地區陰謀數值"""
        area_info = {}
        for area_name in ["醫院", "神社", "都市", "學校"]:
            conspiracy_value = self.game.areas[area_name].conspiracy if area_name in self.game.areas else 0
            area_text = f"{area_name} - ☣{conspiracy_value}\n"

            # 找出該區域內的角色
            characters_in_area = [char for char in self.game.character_manager.characters if char.current_location == area_name]
            for char in characters_in_area:
                area_text += f"{char.name}：❤ {char.friendship} || ⚠︎ {char.anxiety}/{char.anxiety_threshold} || ☣{char.conspiracy}\n"

            area_info[area_name] = area_text

        return area_info

    def update_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        events = self.game.time_manager.get_scheduled_events(self.game.scheduled_events)
        
        # 按照事件的 date 屬性排序
        sorted_events = sorted(events.items(), key=lambda x: x[1].date)

        for day, event in sorted_events:
            tk.Label(self.events_frame, text=f"{event.date}: {event.name}").pack(anchor="w")



    def create_action_phase_widgets(self):
        self.action_phase_frame = tk.Frame(self.main_frame)
        self.action_phase_frame.grid(row=0, column=2, columnspan=2, sticky="nsew")

        self.scriptwriter_frame = tk.LabelFrame(self.action_phase_frame, text="劇本家的行動", padx=5, pady=5)
        self.scriptwriter_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.scriptwriter_actions_label = tk.Label(self.scriptwriter_frame, text="等待劇本家行動...", wraplength=300, justify=tk.LEFT)
        self.scriptwriter_actions_label.grid(row=0, column=0, padx=5, pady=5)

        self.player_frame = tk.LabelFrame(self.action_phase_frame, text="偵探的行動", padx=5, pady=5)
        self.player_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.target_vars = []
        self.action_comboboxes = []

        for i in range(3):
            choice_frame = tk.Frame(self.player_frame)
            choice_frame.grid(row=i, column=0, columnspan=2, sticky="nsew", padx=5, pady=2)

            target_var = tk.StringVar()
            target_combobox = ttk.Combobox(choice_frame, textvariable=target_var, 
                               values=self.get_available_targets(), width=15)
            target_combobox.grid(row=0, column=0, padx=2)
            self.target_vars.append(target_var)

            action_var = tk.StringVar()
            # ✅ 避免 `self.phase` 為 `None` 時發生錯誤
            action_combobox = ttk.Combobox(choice_frame, textvariable=action_var, 
                                        values=[action.name for action in self.phase.game.players["偵探"].available_actions.values()] if self.phase else [], 
                                        width=15)
            action_combobox.grid(row=0, column=1, padx=2)
            self.action_comboboxes.append(action_combobox)

        self.confirm_button = tk.Button(self.player_frame, text="確認行動", 
                                command=lambda: self.phase.confirm_action_selection() if self.phase else None)

        self.confirm_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_scriptwriter_actions(self, scriptwriter_selections):
        actions_text = "劇本家的行動目標：\n"
        for i, selection in enumerate(scriptwriter_selections, 1):
            actions_text += f"{i}. 目標：{selection['target']}\n"
        self.scriptwriter_actions_label.config(text=actions_text)

    def get_player_action_selection(self):
        selections = []
        invalid_selection = False
        used_actions = set()  # 紀錄本回合內已使用的行動

        for i in range(3):
            target = self.target_vars[i].get()
            action_name = self.action_comboboxes[i].get()
            action = next((a for a in self.phase.game.players["偵探"].available_actions.values() if a.name == action_name), None)

            if target and action:
                if action.can_use():  # ✅ 先確認行動是否可用
                    selections.append({"target": target, "action": action})
                else:
                    invalid_selection = True
                    print(f"⚠️ {action_name} 已達使用上限，無法選擇！")

                # 🛑 如果行動有 `usage_limit=1`，確保它沒被重複選擇
                if action.usage_limit == 1 and action_name in used_actions:
                    self.show_error(f"行動「{action_name}」一輪迴只能使用一次！")
                    return []

                # 🛑 如果行動是 `is_daily_limited`，檢查當天是否已使用過
                if action.is_daily_limited and action_name in used_actions:
                    self.show_error(f"行動「{action_name}」一天只能使用一次！")
                    return []

                
                used_actions.add(action_name)  # 標記該行動已選擇
            else:
                invalid_selection = True  # 標記有錯誤，等迴圈結束再處理

        if invalid_selection:
            self.show_error("請選擇有效的目標和行動")
            return []  # 返回空列表，而不是遞迴呼叫自己
        
        return selections  # 如果沒有錯誤，返回正確的選擇

    def update_action_combobox_values(self):
        """當 phase 被設置後，更新行動選單"""
        if not self.phase or not hasattr(self.phase, "game"):
            print("❌ Phase 或 game 不存在，無法更新行動選單")
            return  # 確保 phase 和 game 存在

        detective = self.phase.game.players.get("偵探")
        
        if detective:
            available_actions = [action.name for action in detective.available_actions.values()]
            print(f"✅ 更新 GUI 選單，偵探可用行動: {available_actions}")  # 🛠 除錯用

            for action_combobox in self.action_comboboxes:
                action_combobox["values"] = available_actions
        else:
            print("❌ 無法找到偵探玩家")
        
    def get_available_targets(self):
        """獲取所有可選擇的目標（角色 + 地區）"""
        targets = [character.name for character in self.game.character_manager.characters]  # 加入所有角色
        targets.extend(["醫院", "神社", "都市", "學校"])  # 加入所有地區
        return targets

    def create_ability_widgets(self):
        self.ability_frame = tk.LabelFrame(self.main_frame, text="友好能力", padx=5, pady=5)
        self.ability_frame.grid(row=0, column=2, columnspan=2, sticky="nsew")
        self.ability_frame.grid_remove()  # ✅ 預設隱藏，不會影響 layout

    def update_friendship_abilities(self):
        """顯示所有可用的友好能力（不區分角色）"""
        self.ability_frame.grid()  # ✅ 顯示友好能力框架
        for widget in self.ability_frame.winfo_children():
            widget.destroy()

        # 🟢 建立可用能力列表
        self.available_abilities = [
            ability for character in self.characters 
            for ability in character.friendship_abilities if ability.is_available(character)
        ]

        print("🎯 更新可用的友好能力:", [ability.name for ability in self.available_abilities])  # Debug

        self.ability_var = tk.StringVar()
        self.ability_combobox = ttk.Combobox(
            self.ability_frame, textvariable=self.ability_var,
            values=[ability.name for ability in self.available_abilities]
        )
        self.ability_combobox.pack()

        confirm_button = tk.Button(
            self.ability_frame, text="確認能力",
            command=self.update_target_selection
        )
        confirm_button.pack()

        # 目標選擇下拉式選單
        self.target_var = tk.StringVar()
        self.target_combobox = ttk.Combobox(self.ability_frame, textvariable=self.target_var)
        self.target_combobox.pack()

        confirm_target_button = tk.Button(
            self.ability_frame, text="確認目標",
            command=self.confirm_target_selection
        )
        confirm_target_button.pack()

        # 🟢 加入「結束友好能力階段」按鈕
        end_button = tk.Button(
            self.ability_frame, text="結束友好能力階段",
            command=self.phase.end_phase,
            fg="white", bg="red", font=("Arial", 12, "bold")
        )
        end_button.pack()

    def update_target_selection(self):
        """依據選擇的能力，更新可用目標列表"""
        selected_ability_name = self.ability_var.get()
        selected_ability = next((a for a in self.available_abilities if a.name == selected_ability_name), None)

        if not selected_ability:
            return

        # 🔹 **通知 PlayerFriendshipAbilityPhase**
        self.phase.confirm_ability_selection(selected_ability.FA_id)

        # 解析發動能力的角色
        ability_owner_id = selected_ability.FA_id // 100
        self.current_character = next((char for char in self.game.character_manager.characters if char.Ch_id == ability_owner_id), None)

        if not self.current_character:
            print(f"⚠️ 無法找到 ID 為 {ability_owner_id} 的角色")
            return

        # 更新可用目標列表
        self.valid_targets = [
            char.name for char in self.game.character_manager.characters
            if selected_ability.target_condition(char, self.current_character)
        ]
        self.target_combobox["values"] = self.valid_targets

        print(f"🎯 可選目標: {self.valid_targets}")



    def confirm_target_selection(self):
        """確認目標並執行能力"""
        selected_target_name = self.target_var.get()
        selected_ability_name = self.ability_var.get()

        if not selected_target_name:
            self.show_message("請先選擇目標！")
            return

        

        # 取得選擇的能力與目標
        selected_target = next((c for c in self.game.character_manager.characters if c.name == selected_target_name), None)
        selected_ability = next((a for a in self.available_abilities if a.name == selected_ability_name), None)

        if not selected_ability or not selected_target:
            self.show_message("請重新選擇能力與目標！")
            return

        # ✅ **通知 PlayerFriendshipAbilityPhase**
        self.phase.selected_ability = selected_ability
        self.phase.selected_target = selected_target
        # 🟢 執行能力


        if self.phase.selected_ability and self.phase.selected_target:
            self.phase.execute_ability()
            self.update_area_widgets()
            self.update_friendship_abilities()
        else:
            print("⚠️ [GUI] 無法執行能力，選擇的能力或目標為 None！")


    def show_message(self, message):
        messagebox.showinfo("訊息", message)
    
    def show_error(self, message):
        messagebox.showerror("錯誤", message)
    
    def create_snapshot_button(self):
        """新增快照按鈕"""
        self.snapshot_button = tk.Button(self.time_frame, text="📸 記錄當前狀態", command=self.record_snapshot)
        self.snapshot_button.pack(anchor="w")

    def record_snapshot(self):
        """記錄當前狀態"""
        self.game.history.take_snapshot(self.game)
        self.update_history_dropdown()

    def create_history_view(self):
        """新增履歷檢視的 UI"""
        tk.Label(self.time_frame, text="🔍 回顧遊戲履歷：").pack(anchor="w")

        self.history_var = tk.StringVar(self.time_frame)
        self.history_dropdown = tk.OptionMenu(self.time_frame, self.history_var, *self.game.history.get_snapshots())
        self.history_dropdown.pack(anchor="w")

        self.view_history_button = tk.Button(self.time_frame, text="🔎 檢視", command=self.view_history)
        self.view_history_button.pack(anchor="w")

    def update_history_dropdown(self):
        """更新下拉選單的內容"""
        menu = self.history_dropdown["menu"]
        menu.delete(0, "end")
        for label in self.game.history.get_snapshots():
            menu.add_command(label=label, command=lambda value=label: self.history_var.set(value))

    def view_history(self):
        """檢視選定的快照"""
        selected_label = self.history_var.get()
        index = self.game.history.get_snapshots().index(selected_label)
        snapshot = self.game.history.get_snapshot_by_index(index)

        if snapshot:
            self.show_history_window(snapshot)

    def show_history_window(self, snapshot):
        """顯示快照的獨立視窗"""
        history_window = tk.Toplevel(self.root)
        history_window.title(f"回顧 - {snapshot['label']}")

        tk.Label(history_window, text=snapshot["label"], font=("Arial", 12, "bold")).pack()

        # 顯示地區狀態
        for area_name, area_data in snapshot["areas"].items():
            tk.Label(history_window, text=f"📍 {area_name}").pack(anchor="w")
            for key, value in area_data.items():
                tk.Label(history_window, text=f"   {key}: {value}").pack(anchor="w")

        # 顯示角色狀態
        for char_name, char_data in snapshot["character_manager.characters"].items():
            tk.Label(history_window, text=f"🧑 {char_name}").pack(anchor="w")
            for key, value in char_data.items():
                tk.Label(history_window, text=f"   {key}: {value}").pack(anchor="w")


    def ask_user(self, message):
        """ 顯示詢問對話框，返回玩家的選擇（是 True / 否 False） """
        return messagebox.askyesno("能力發動確認", message)

class GameHistory:
    def __init__(self):
        """初始化快照記錄"""
        self.history_snapshots = []  # 存放所有快照 (list of dict)

    def take_snapshot(self, game):
        """記錄當前遊戲狀態"""
        snapshot = {
            "label": f"輪迴 {game.time_manager.remaining_cycles} / 日期 {game.time_manager.current_day} / 階段 {game.current_phase}",
            "time": game.time_manager.remaining_cycles,
            "day": game.time_manager.current_day,
            "phase": game.current_phase,
            "areas": {area.name: area.get_snapshot() for area in game.areas},
            "characters": {char.name: char.get_snapshot() for char in game.characters}
        }
        self.history_snapshots.append(snapshot)

    def get_snapshots(self):
        """取得所有快照標籤清單"""
        return [snap["label"] for snap in self.history_snapshots]

    def get_snapshot_by_index(self, index):
        """根據索引取得快照內容"""
        return self.history_snapshots[index] if 0 <= index < len(self.history_snapshots) else None
