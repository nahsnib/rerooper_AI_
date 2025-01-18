import tkinter as tk
from tkinter import messagebox
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
    Action(13, "禁止移動", lambda character: character.prevent_movement(), usage_limit=1),
    Action(14, "不安+1", lambda character: character.change_anxiety(1)),
    Action(15, "不安-1", lambda character: character.change_anxiety(-1), usage_limit=1),
    Action(16, "友好+1", lambda character: character.change_friendship(1)),
    Action(17, "友好+2", lambda character: character.change_friendship(2), usage_limit=1),
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

    for _ in range(num_targets):
        target = random.choice(["角色A", "角色B", "角色C", "地區1", "地區2", "地區3"])
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

class DetectiveActionGUI:
    def __init__(self, root):
        self.root = root
        self.selected_targets = []
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="選擇三個目標並設置行動")
        self.label.pack()

        self.target_entries = []
        self.action_entries = []

        for i in range(3):
            target_label = tk.Label(self.root, text=f"目標 {i+1}")
            target_label.pack()
            target_entry = tk.Entry(self.root)
            target_entry.pack()
            self.target_entries.append(target_entry)

            action_label = tk.Label(self.root, text=f"行動 {i+1}")
            action_label.pack()
            action_entry = tk.Entry(self.root)
            action_entry.pack()
            self.action_entries.append(action_entry)

        self.confirm_button = tk.Button(self.root, text="確認", command=self.confirm_selection)
        self.confirm_button.pack()

    def confirm_selection(self):
        self.selected_targets = []
        for i in range(3):
            target = self.target_entries[i].get()
            action_id = int(self.action_entries[i].get())
            action = get_action_by_id(action_id, 'detective')
            if action:
                self.selected_targets.append({"target": target, "action": action})

        if len(self.selected_targets) == 3:
            if messagebox.askyesno("確認", "是否確認您的行動選擇？"):
                self.root.quit()
            else:
                self.selected_targets = []

if __name__ == "__main__":
    # 劇本家選擇目標和行動
    scriptwriter_action_choices = choose_targets_and_actions('scriptwriter')

    # 建立偵探的行動選擇GUI
    root = tk.Tk()
    gui = DetectiveActionGUI(root)
    root.mainloop()

    detective_action_choices = gui.selected_targets

    # 解決雙方的行動
    resolve_actions(scriptwriter_action_choices, detective_action_choices)
