import tkinter as tk
from tkinter import ttk, messagebox
import random
from common.action import Action, scriptwriter_actions, detective_actions
from common.character import Character
from common.board import Area, hospital, shrine, city, school, areas
from common.board import get_area_by_id, display_all_areas

class PlayerDetectiveActionPhase:
    def __init__(self, character_manager):
        self.character_manager = character_manager
        self.selected_targets = []
        self.scriptwriter_selections = []  # 劇本家的選擇

    def execute(self):
        self.scriptwriter_choose_targets_and_actions()
        root = tk.Tk()
        targets = self.get_available_targets()
        actions = detective_actions
        gui = ActionSelectionGUI(root, 'detective', targets, actions, self.scriptwriter_selections)
        root.mainloop()

        self.selected_targets = gui.selected_targets
        self.resolve_actions()

    def scriptwriter_choose_targets_and_actions(self):
        characters = self.character_manager.load_characters()
        if characters is None:
            raise ValueError("Characters could not be loaded.")

        available_targets = [character.name for character in characters] + [area.name for area in areas.values()]
        chosen_targets = random.sample(available_targets, 3)

        for target in chosen_targets:
            action = random.choice(scriptwriter_actions)
            self.scriptwriter_selections.append({"target": target, "action": action})

    def get_available_targets(self):
        targets = []
        characters = self.character_manager.load_characters()
        if characters is None:
            raise ValueError("Characters could not be loaded.")
        for character in characters:
            targets.append(character.name)
        for area_id, area in areas.items():
            targets.append(area.name)
        return targets

    def get_target_by_name(self, name):
        # 從角色或地區中查找目標
        characters = self.character_manager.load_characters()
        if characters is None:
            raise ValueError("Characters could not be loaded.")
        for character in characters:
            if character.name == name:
                return character
        for area in areas.values():
            if area.name == name:
                return area
        return None

    def resolve_actions(self):
        # 先檢查是否有禁止行動的效果
        forbidden_actions = [13, 14, 15, 9, 10, 18]  # 禁止移動 ABC, 不安禁止, 友好禁止, 禁止陰謀
        forbidden_targets = set()
        
        for selection in self.selected_targets:
            action = selection["action"]
            if action.id in forbidden_actions:
                forbidden_targets.add(selection["target"])

        # 執行其他行動，排除被禁止的行動
        for selection in self.selected_targets:
            target_name = selection["target"]
            action = selection["action"]
            if target_name not in forbidden_targets:
                target = self.get_target_by_name(target_name)
                action.effect(target)

class ActionSelectionGUI:
    def __init__(self, root, role, targets, actions, previous_selections=[]):
        self.root = root
        self.role = role
        self.targets = targets
        self.actions = actions
        self.selected_targets = []
        self.previous_selections = previous_selections
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="選擇目標和行動")
        self.label.pack()

        if self.role == 'detective' and self.previous_selections:
            self.previous_selections_label = tk.Label(self.root, text="劇本家已選定的目標：")
            self.previous_selections_label.pack()
            self.previous_selections_text = tk.Text(self.root, height=5, width=50)
            self.previous_selections_text.pack()
            for selection in self.previous_selections:
                self.previous_selections_text.insert(tk.END, f"{selection['target']}\n")
            self.previous_selections_text.config(state=tk.DISABLED)

        self.target_comboboxes = []
        self.action_comboboxes = []

        for i in range(3):
            target_label = tk.Label(self.root, text=f"第{i + 1}選擇 目標")
            target_label.pack()
            target_combobox = ttk.Combobox(self.root, values=self.targets)
            target_combobox.pack()
            self.target_comboboxes.append(target_combobox)

            action_label = tk.Label(self.root, text=f"第{i + 1}選擇 行動")
            action_label.pack()
            action_combobox = ttk.Combobox(self.root, values=[action.name for action in self.actions])
            action_combobox.pack()
            self.action_comboboxes.append(action_combobox)

        self.confirm_button = tk.Button(self.root, text="確認", command=self.confirm_selection)
        self.confirm_button.pack()

    def confirm_selection(self):
        self.selected_targets = []
        for i in range(3):
            target = self.target_comboboxes[i].get()
            action_name = self.action_comboboxes[i].get()
            action = next((a for a in self.actions if a.name == action_name), None)

            if target and action:
                if action.can_use():
                    self.selected_targets.append({"target": target, "action": action})
                else:
                    messagebox.showerror("錯誤", f"【{action_name}】使用機會不足！")
                    return
            else:
                messagebox.showerror("錯誤", "請選擇有效的目標和行動")
                return

        if self.check_validity():
            self.root.quit()
        else:
            messagebox.showerror("錯誤", "選擇不符合規則，請重新選擇")
            self.reset_selection()

    def check_validity(self):
        targets = [item["target"] for item in self.selected_targets]
        actions = [item["action"].name for item in self.selected_targets]
        if len(set(targets)) != len(targets):
            return False
        if self.role == 'scriptwriter' and len(set(actions)) != len(actions):
            return False
        if self.role == 'detective' and actions.count("禁止陰謀") > 1:
            return False
        return True

    def reset_selection(self):
        self.selected_targets = []
        for target_combobox in self.target_comboboxes:
            target_combobox.set('')
        for action_combobox in self.action_comboboxes:
            action_combobox.set('')

def choose_targets_and_actions(role, num_targets=3):
    actions = scriptwriter_actions if role == 'scriptwriter' else detective_actions
    chosen_targets = []

    available_targets = ["角色A", "角色B", "地區1", "地區2", "地區3", "地區4"]
    for _ in range(num_targets):
        target = random.choice(available_targets)
        available_targets.remove(target)
        action = random.choice(actions)
        while action in [a["action"] for a in chosen_targets]:
            action = random.choice(actions)
        chosen_targets.append({"target": target, "action": action})

    return chosen_targets

def process_all_actions(scriptwriter_actions, detective_actions):
    combined_actions = scriptwriter_actions + detective_actions
    combined_actions.sort(key=lambda x: x["action"].id)

    resolve_movement_actions(combined_actions)
    resolve_anxiety_friendship_actions(combined_actions)
    resolve_conspiracy_actions(combined_actions)
    resolve_other_actions(combined_actions)

def resolve_movement_actions(actions):
    move_actions = {}
    forbidden_targets = set()
    
    # 首先找出被禁止移動的目標
    for action in actions:
        if action["action"].id == 13:  # 禁止移動
            forbidden_targets.add(action["target"])

    # 收集所有移動行動
    for action in actions:
        if action["action"].id in [1, 2, 3, 11, 12]:
            target = action["target"]
            if target not in move_actions:
                move_actions[target] = []
            move_actions[target].append(action["action"].id)

    # 執行合併後的移動行動
    for target, move_ids in move_actions.items():
        if target in forbidden_targets:
            continue  # 如果有禁止移動行動，什麼都不做

        # 根據規則決定最終的移動行動
        if 1 in move_ids and 11 in move_ids:
            target.move_horizontal()
        elif 3 in move_ids and 12 in move_ids:
            target.move_horizontal()
        elif 2 in move_ids and 12 in move_ids:
            target.move_vertical()
        elif 3 in move_ids and 11 in move_ids:
            target.move_vertical()
        elif 1 in move_ids and 12 in move_ids:
            target.move_diagonal()
        elif 2 in move_ids and 11 in move_ids:
            target.move_diagonal()
        else:
            # 如果沒有合併規則，執行單一移動行動
            for move_id in move_ids:
                if move_id == 1:
                    target.move_horizontal()
                elif move_id == 2:
                    target.move_vertical()
                elif move_id == 3:
                    target.move_diagonal()
                elif move_id == 11:
                    target.move_horizontal()
                elif move_id == 12:
                    target.move_vertical()

def resolve_anxiety_friendship_actions(actions):
    forbidden_anxiety_targets = set()
    forbidden_friendship_targets = set()
    
    # 找出被禁止不安和友好的目標
    for action in actions:
        if action["action"].id == 9:  # 不安禁止
            forbidden_anxiety_targets.add(action["target"])
        if action["action"].id == 10:  # 友好禁止
            forbidden_friendship_targets.add(action["target"])

    # 執行不安和友好行動
    for action in actions:
        if action["action"].id in [4, 5, 8, 14, 15]:  # 不安相關行動
            if action["target"] not in forbidden_anxiety_targets:
                target = action["target"]
                action["action"].effect(target)
        if action["action"].id in [16, 17]:  # 友好相關行動
            if action["target"] not in forbidden_friendship_targets:
                target = action["target"]
                action["action"].effect(target)

def resolve_conspiracy_actions(actions):
    forbidden_conspiracy_targets = set()
    
    # 找出被禁止陰謀的目標
    for action in actions:
        if action["action"].id == 18:  # 禁止陰謀
            forbidden_conspiracy_targets.add(action["target"])

    # 執行陰謀行動
    for action in actions:
        if action["action"].id in [6, 7]:
            if action["target"] not in forbidden_conspiracy_targets:
                target = action["target"]
                action["action"].effect(target)

def resolve_other_actions(actions):
    # 假設還有其他行動需要處理，可以在這裡添加處理邏輯
    for action in actions:
        if action["action"].id not in [4, 5, 8, 9, 10, 14, 15, 16, 17, 18]:  # 排除已處理的行動
            target = action["target"]
            action["action"].effect(target)

if __name__ == "__main__":
    scriptwriter_action_choices = choose_targets_and_actions('scriptwriter')
    root = tk.Tk()
    targets = ["角色A", "角色B", "地區1", "地區2", "地區3", "地區4"]
    actions = detective_actions

    print("劇本家選擇的目標：")
    for choice in scriptwriter_action_choices:
        print(choice["target"])

    gui = ActionSelectionGUI(root, 'detective', targets, actions, previous_selections=[item["target"] for item in scriptwriter_action_choices])
    root.mainloop()

    detective_action_choices = gui.selected_targets
    process_all_actions(scriptwriter_action_choices, detective_action_choices)