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

    def execute(self):
        root = tk.Tk()
        targets = self.get_available_targets()
        actions = detective_actions
        gui = ActionSelectionGUI(root, 'detective', targets, actions)
        root.mainloop()

        self.selected_targets = gui.selected_targets
        self.resolve_actions()

    def get_available_targets(self):
        targets = []
        characters = self.character_manager.get_all_characters()
        for character in characters:
            targets.append(character.name)
        for area_id, area in areas.items():
            targets.append(area.name)
        return targets

    def resolve_actions(self):
        for selection in self.selected_targets:
            target_name = selection["target"]
            action = selection["action"]
            target = self.get_target_by_name(target_name)
            action.effect(target)

    def get_target_by_name(self, name):
        # 從角色或地區中查找目標
        for character in self.character_manager.get_all_characters():
            if character.name == name:
                return character
        for area in areas.values():
            if area.name == name:
                return area
        return None

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

        self.target_combobox = ttk.Combobox(self.root, values=self.targets)
        self.target_combobox.pack()

        self.action_combobox = ttk.Combobox(self.root, values=[action.name for action in self.actions])
        self.action_combobox.pack()

        self.confirm_button = tk.Button(self.root, text="確認", command=self.confirm_selection)
        self.confirm_button.pack()

    def confirm_selection(self):
        target = self.target_combobox.get()
        action_name = self.action_combobox.get()
        action = next((a for a in self.actions if a.name == action_name), None)

        if target and action:
            self.selected_targets.append({"target": target, "action": action})
            if len(self.selected_targets) < 3:
                self.targets.remove(target)
                self.target_combobox.set('')
                self.action_combobox.set('')
            else:
                self.show_confirmation_dialog()
        else:
            messagebox.showerror("錯誤", "請選擇有效的目標和行動")

    def show_confirmation_dialog(self):
        confirmation_text = "\n".join([f"{item['target']}: {item['action'].name}" for item in self.selected_targets])
        if self.check_validity():
            if messagebox.askyesno("確認", f"以下是您的選擇：\n{confirmation_text}\n是否確認？"):
                self.root.quit()
            else:
                self.reset_selection()
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
        self.target_combobox.set('')
        self.action_combobox.set('')
        self.targets = ["角色A", "角色B", "地區1", "地區2", "地區3", "地區4"]
        for prev in self.previous_selections:
            if prev["target"] in self.targets:
                self.targets.remove(prev["target"])

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

def resolve_actions(scriptwriter_actions, detective_actions):
    combined_actions = scriptwriter_actions + detective_actions
    combined_actions.sort(key=lambda x: x["action"].id)

    for action in combined_actions:
        print(f"{action['target']} - 行動ID: {action['action'].id}")

    resolve_movement_actions(combined_actions)
    resolve_anxiety_friendship_actions(combined_actions)
    resolve_conspiracy_actions(combined_actions)
    resolve_other_actions(combined_actions)

def resolve_movement_actions(actions):
    for action in actions:
        if action["action"].id in [1, 2, 3, 11, 12, 13]:
            if "角色" in action["target"]:
                pass  # 解決移動行動邏輯

def resolve_anxiety_friendship_actions(actions):
    for action in actions:
        if action["action"].id in [4, 5, 8, 9, 14, 15]:
            if "地區" in action["target"]:
                continue
            if action["action"].id == 9:
                pass  # 取消同目標的14效果

def resolve_conspiracy_actions(actions):
    for action in actions:
        if action["action"].id in [6, 7, 18]:
            if action["action"].id == 18:
                pass  # 取消同目標的6與7效果

def resolve_other_actions(actions):
    for action in actions:
        if action["action"].id in [10, 16, 17]:
            if "地區" in action["target"]:
                continue
            if action["action"].id == 10:
                pass  # 取消同目標的16與17效果

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
    resolve_actions(scriptwriter_action_choices, detective_action_choices)