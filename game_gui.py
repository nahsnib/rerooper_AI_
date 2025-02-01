import tkinter as tk
from tkinter import ttk, messagebox
from common.area_and_date import hospital, shrine, city, school, TimeManager, areas
from common.character import CharacterManager
from common.action import detective_actions
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from game_phases.player_detective.player_friendship_ability_phase import PlayerFriendshipAbilityPhase

class GameGUI:
    def __init__(self, root, game, characters, phase):
        self.root = root
        self.game = game
        self.characters = characters
        self.phase = phase
        self.selected_targets = []
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 創建時間信息和地區顯示區域的框架
        self.time_frame = tk.Frame(self.main_frame)
        self.time_frame.grid(row=0, column=0, sticky="ns")
        
        self.area_frame = tk.Frame(self.main_frame)
        self.area_frame.grid(row=0, column=1, sticky="nsew")
        
        self.operation_frame = tk.Frame(self.main_frame)
        self.operation_frame.grid(row=0, column=2, sticky="ns")

        # 設置行和列的權重，以便自動調整大小
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # 添加時間信息和地區顯示區域在頂部
        self.create_time_and_area_widgets()

        # 根據 phase 類型創建相應的 GUI
        if isinstance(self.phase, PlayerDetectiveActionPhase):
            self.create_action_phase_widgets()
        elif isinstance(self.phase, PlayerFriendshipAbilityPhase):
            self.create_ability_phase_widgets()
        
        # 創建訊息框
        self.message_box = tk.Text(self.main_frame, state='disabled', height=10, wrap="word")
        self.message_box.grid(row=1, column=0, columnspan=3, sticky="ew")




    def create_time_and_area_widgets(self):
        # 剩餘輪迴數量
        tk.Label(self.time_frame, text="剩餘輪迴數量:").pack(anchor="w")
        self.remaining_cycles_label = tk.Label(self.time_frame, text=str(self.game.time_manager.remaining_cycles))
        self.remaining_cycles_label.pack(anchor="w")

        # 日期標籤和數值
        tk.Label(self.time_frame, text="當前日期/總日期").pack(anchor="w")
        date_info = f"{self.game.time_manager.current_day} / {self.game.time_manager.total_days}"
        self.date_info_label = tk.Label(self.time_frame, text=date_info)
        self.date_info_label.pack(anchor="w")


        # 安排事件的日期和名稱
        tk.Label(self.time_frame, text="安排事件的日期和名稱:").pack(anchor="w")
        self.events_frame = tk.Frame(self.time_frame)
        self.events_frame.pack(anchor="w")
        self.update_events()

        # 地區顯示
        self.areas_frame = tk.Frame(self.area_frame)
        self.areas_frame.pack(fill=tk.BOTH, expand=True)

        self.create_area_widgets()

    def update_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        events = self.game.time_manager.get_scheduled_events(self.game.scheduled_events)
        sorted_events = sorted(events.items())  # 按照日期排序事件

        for day, event in sorted_events:
            tk.Label(self.events_frame, text=f"{day}: {event}").pack(anchor="w")  # 直接使用 event 作為字符串

    def create_area_widgets(self):
        # 創建地區顯示區域，設置寬度和高度（假設每個中文字寬度為20像素，高度為20像素）
        self.hospital_frame = tk.LabelFrame(self.areas_frame, text="醫院----------------", padx=10, pady=10, width=7*20, height=5*20)
        self.hospital_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.hospital_frame.grid_propagate(False)  # 防止自動調整大小

        self.shrine_frame = tk.LabelFrame(self.areas_frame, text="神社----------------", padx=10, pady=10, width=7*20, height=5*20)
        self.shrine_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.shrine_frame.grid_propagate(False)  # 防止自動調整大小

        self.city_frame = tk.LabelFrame(self.areas_frame, text="鬧區----------------", padx=10, pady=10, width=7*20, height=5*20)
        self.city_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.city_frame.grid_propagate(False)  # 防止自動調整大小

        self.school_frame = tk.LabelFrame(self.areas_frame, text="學校----------------", padx=10, pady=10, width=7*20, height=5*20)
        self.school_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.school_frame.grid_propagate(False)  # 防止自動調整大小

        self.update_area_widgets()

    def update_area_widgets(self):
        for frame in [self.hospital_frame, self.shrine_frame, self.city_frame, self.school_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

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
            print(f"角色: {character.name}, 位置: {character.current_location}")  # 添加打印語句

    def get_available_targets(self):
        # 獲取可用的目標列表，包括角色和地區
        character_names = [character.name for character in self.characters]
        area_names = ["醫院", "神社", "鬧區", "學校"]
        return character_names + area_names
    
    def show_history(self):
        # 創建一個新窗口來顯示遊戲履歷
        history_window = tk.Toplevel(self.root)
        history_window.title("遊戲履歷")

        # 顯示遊戲履歷
        history_text = tk.Text(history_window, wrap="word", width=80, height=20)
        history_text.pack(padx=10, pady=10)

        # 獲取遊戲歷史記錄並顯示
        history = self.game.time_manager.get_game_history()
        for snapshot in history:
            history_text.insert(tk.END, f"Timestamp: {snapshot['timestamp']}\n")
            history_text.insert(tk.END, "GameBoard State:\n")
            gameboard_state = snapshot['gameboard_state']
            for area, state in gameboard_state['areas'].items():
                history_text.insert(tk.END, f"  - {area}: Conspiracy Points: {state['conspiracy_points']}, Characters: {', '.join([c.name for c in state['characters']])}\n")
            history_text.insert(tk.END, f"Time Manager: Day {gameboard_state['time_manager']['current_day']}, Remaining Cycles: {gameboard_state['time_manager']['remaining_cycles']}\n")
            history_text.insert(tk.END, "\n")

    # 創建行動階段的 GUI 元件
    def create_action_phase_widgets(self):
        self.action_phase_frame = tk.Frame(self.operation_frame)
        self.action_phase_frame.pack(fill=tk.BOTH, expand=True)

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

        self.confirm_button = tk.Button(self.action_phase_frame, text="確認", command=self.confirm_action_selection)
        self.confirm_button.pack()

        self.scriptwriter_actions_label = tk.Label(self.action_phase_frame, text="", wraplength=300, justify=tk.LEFT)
        self.scriptwriter_actions_label.pack()

        self.update_scriptwriter_actions()  # 更新劇本家的行動顯示






    def confirm_action_selection(self):
        self.selected_targets = []
        for i in range(3):
            target = self.target_vars[i].get()
            action_name = self.action_vars[i].get()
            action = next((a for a in detective_actions if a.name == action_name), None)

            if target and action:
                if action.can_use():
                    self.selected_targets.append({"target": target, "action": action})
                else:
                    messagebox.showerror("錯誤", f"【{action_name}】使用機會不足！")
                    return
            else:
                messagebox.showerror("錯誤", "請選擇有效的目標和行動")
                return

        if self.check_action_validity():
            self.phase.Player_Action(self.selected_targets)
            self.phase.execute_actions()  # 執行行動
            self.show_message(f"選擇了行動：{[action['action'].name for action in self.selected_targets]}，目標：{[target['target'] for target in self.selected_targets]}")
            self.update_area_widgets()  # 更新區域面板
        else:
            messagebox.showerror("錯誤", "選擇不符合規則，請重新選擇")
            self.reset_action_selection()

    def update_scriptwriter_actions(self):
        actions_text = "劇本家行動選擇目標："
        actions_text += "、".join([f"{selection['target']}({selection['action'].name})" for selection in self.phase.scriptwriter_selections])
        self.scriptwriter_actions_label.config(text=actions_text)    

    def check_action_validity(self):
        targets = [item["target"] for item in self.selected_targets]
        actions = [item["action"].name for item in self.selected_targets]
        if len(set(targets)) != len(targets):
            return False
        if actions.count("禁止陰謀") > 1:
            return False
        return True

    def reset_action_selection(self):
        self.selected_targets = []
        for target_var in self.target_vars:
            target_var.set('')
        for action_var in self.action_vars:
            action_var.set('')
    
    # 創建友好能力階段的 GUI 元件
    def create_ability_phase_widgets(self):
        # 創建友好能力階段的 GUI 元件
        self.ability_phase_frame = tk.Frame(self.operation_frame)
        self.ability_phase_frame.pack(fill=tk.BOTH, expand=True)

        self.ability_phase_label = tk.Label(self.ability_phase_frame, text="友好能力階段：選擇角色能力")
        self.ability_phase_label.pack()

        self.ability_combobox = ttk.Combobox(self.ability_phase_frame)
        self.ability_combobox.pack(pady=5)
        self.ability_combobox.bind("<<ComboboxSelected>>", self.on_ability_select)

        self.target_combobox = ttk.Combobox(self.ability_phase_frame)
        self.target_combobox.pack(pady=5)

        self.confirm_button = tk.Button(self.ability_phase_frame, text="確定", command=self.confirm_ability_selection)
        self.confirm_button.pack(pady=20)

        self.exit_button = tk.Button(self.ability_phase_frame, text="離開", command=self.exit_phase)
        self.exit_button.pack(pady=20)

        # 加入所有符合條件的角色能力
        self.update_ability_combobox()

    def update_ability_combobox(self):
        abilities = []
        for character in self.characters:
            for ability in character.friendly_abilities:
                if ability['trigger'](character) and not character.friendly_ability_usage.get(ability['name'], False):
                    abilities.append(f"{character.name}: {ability['name']}")
        self.ability_combobox.config(values=abilities)

    def on_ability_select(self, event):
        ability_text = self.ability_combobox.get()
        character_name, ability_name = ability_text.split(': ')
        self.selected_character = self.phase.get_character_by_name(character_name)
        self.selected_ability = next((a for a in self.selected_character.friendly_abilities if a['name'] == ability_name), None)

        if self.selected_ability and self.selected_ability['target_required']:
            target_names = [character.name for character in self.characters if character.alive]
            self.target_combobox.config(values=target_names)
            self.target_combobox.set('')

    def confirm_ability_selection(self):
        ability_text = self.ability_combobox.get()
        character_name, ability_name = ability_text.split(': ')
        character = self.phase.get_character_by_name(character_name)
        ability = next((a for a in character.friendly_abilities if a['name'] == ability_name), None)
        target_name = self.target_combobox.get()
        target = self.phase.get_character_by_name(target_name) if target_name else None

        if ability:
            result = self.phase.execute_ability(character, ability, target)
            self.show_message(result)
            self.update_area_widgets()  # 更新區域面板

    def show_message(self, message):
        self.message_box.config(state='normal')
        self.message_box.insert(tk.END, message + '\n')
        self.message_box.config(state='disabled')

    def exit_phase(self):
        if messagebox.askyesno("確認", "是否要結束友好能力階段？"):
            self.root.quit()

    def update(self):
        self.remaining_cycles_label.config(text=str(self.game.time_manager.remaining_cycles))
        date_info = f" {self.game.time_manager.current_day} /  {self.game.time_manager.total_days}"
        self.date_info_label.config(text=(date_info))
        self.update_events()
        self.update_area_widgets()