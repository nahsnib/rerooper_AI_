import tkinter as tk
from tkinter import ttk, messagebox
import random

class Action:
    def __init__(self, id, name, effect, usage_limit=None, is_daily_limited=False):
        self.id = id
        self.name = name
        self.effect = effect
        self.usage_limit = usage_limit
        self.times_used = 0
        self.is_daily_limited = is_daily_limited

    def can_use(self):
        if self.usage_limit is None:
            return True
        return self.times_used < self.usage_limit

    def use(self):
        if self.can_use():
            self.times_used += 1
            return True
        return False

    def reset(self):
        self.times_used = 0

    def __str__(self):
        return f"Action({self.id}: {self.name}, Used: {self.times_used}/{self.usage_limit})"

# 劇本家的行動列表
scriptwriter_actions = [
    Action(1, "橫向移動", lambda character: character.move_horizontal(), is_daily_limited=True),
    Action(2, "縱向移動", lambda character: character.move_vertical(), is_daily_limited=True),
    Action(3, "斜角移動", lambda character: character.move_diagonal(), usage_limit=1),
    Action(4, "不安+1 (A)", lambda character: character.change_anxiety(1), is_daily_limited=True),
    Action(5, "不安+1 (B)", lambda character: character.change_anxiety(1), is_daily_limited=True),
    Action(6, "陰謀+1", lambda target: target.change_conspiracy(1), is_daily_limited=True),
    Action(7, "陰謀+2", lambda target: target.change_conspiracy(2), usage_limit=1),
    Action(8, "不安-1", lambda character: character.change_anxiety(-1), is_daily_limited=True),
    Action(9, "不安禁止", lambda character: character.prevent_anxiety_increase(), is_daily_limited=True),
    Action(10, "友好禁止", lambda character: character.prevent_friendship_increase(), is_daily_limited=True)
]

# 偵探的行動列表
detective_actions = [
    Action(11, "橫向移動", lambda character: character.move_horizontal()),
    Action(12, "縱向移動", lambda character: character.move_vertical()),
    Action(13, "禁止移動", lambda character: character.prevent_movement(), usage_limit=3),
    Action(14, "不安+1", lambda character: character.change_anxiety(1)),
    Action(15, "不安-1", lambda character: character.change_anxiety(-1), usage_limit=3),
    Action(16, "友好+1", lambda character: character.change_friendship(1)),
    Action(17, "友好+2", lambda character: character.change_friendship(2), usage_limit=3),
    Action(18, "禁止陰謀", lambda target: target.prevent_conspiracy_increase(), is_daily_limited=True)
]

def get_action_by_id(action_id, role):
    actions = scriptwriter_actions if role == 'scriptwriter' else detective_actions
    for action in actions:
        if action.id == action_id:
            return action
    return None

def display_all_actions(role):
    actions = scriptwriter_actions if role == 'scriptwriter' else detective_actions
    for action in actions:
        print(f"行動編號: {action.id}, 名稱: {action.name}")

def choose_targets_and_actions(role, num_targets=3):
    actions = scriptwriter_actions if role == 'scriptwriter' else detective_actions
    chosen_targets = []

    available_targets = ["角色A", "角色B", "角色C", "地區1", "地區2", "地區3", "地區4"]
    for _ in range(num_targets):
        target = random.choice(available_targets)
        available_targets.remove(target)
        action = random.choice(actions)
        while action in [a["action"] for a in chosen_targets]:
            action = random.choice(actions)
        chosen_targets.append({"target": target, "action": action})

    return chosen_targets

def confirm_action_selection():
    response = input("是否確認您的行動選擇？（yes/no）：")
    return response.lower() == "yes"

def resolve_actions(scriptwriter_actions, detective_actions):
    combined_actions = scriptwriter_actions + detective_actions
    combined_actions.sort(key=lambda x: x["action"].id)

    for action in combined_actions:
        print(f"{action['target']} - 行動ID: {action['action'].id}")

    # 優先解決移動類行動
    resolve_movement_actions(combined_actions)

    # 解決不安與友好行動
    resolve_anxiety_friendship_actions(combined_actions)

    # 解決陰謀行動
    resolve_conspiracy_actions(combined_actions)

    # 解決其他行動
    resolve_other_actions(combined_actions)

def resolve_movement_actions(actions):
    for action in actions:
        if action["action"].id in [1, 2, 3, 11, 12, 13]:
            if "角色" in action["target"]:
                # 解決移動行動邏輯
                pass

def resolve_anxiety_friendship_actions(actions):
    for action in actions:
        if action["action"].id in [4, 5, 8, 9, 14, 15]:
            if "地區" in action["target"]:
                continue
            if action["action"].id == 9:
                # 取消同目標的14效果
                pass

def resolve_conspiracy_actions(actions):
    for action in actions:
        if action["action"].id in [6, 7, 18]:
            if action["action"].id == 18:
                # 取消同目標的6與7效果
                pass

def resolve_other_actions(actions):
    for action in actions:
        if action["action"].id in [10, 16, 17]:
            if "地區" in action["target"]:
                continue
            if action["action"].id == 10:
                # 取消同目標的16與17效果
                pass

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
        self.targets = ["角色A", "角色B", "角色C", "地區1", "地區2", "地區3", "地區4"]
        for prev in self.previous_selections:
            if prev["target"] in self.targets:
                self.targets.remove(prev["target"])

if __name__ == "__main__":
    # 劇本家選擇目標和行動
    scriptwriter_action_choices = choose_targets_and_actions('scriptwriter')

    # 建立偵探的行動選擇GUI，並顯示劇本家選擇的目標
    root = tk.Tk()
    targets = ["角色A", "角色B", "角色C", "地區1", "地區2", "地區3", "地區4"]
    actions = detective_actions

    # 顯示劇本家選擇的目標
    print("劇本家選擇的目標：")
    for choice in scriptwriter_action_choices:
        print(choice["target"])

    gui = ActionSelectionGUI(root, 'detective', targets, actions, previous_selections=[item["target"] for item in scriptwriter_action_choices])
    root.mainloop()

    detective_action_choices = gui.selected_targets

    # 解決雙方的行動
    resolve_actions(scriptwriter_action_choices, detective_action_choices)