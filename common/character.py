# common/character.py

import tkinter as tk
from tkinter import ttk
from database.character_database import load_character_database

class Character:
    def __init__(self, name, anxiety_threshold, initial_location, forbidden_area, attribute, friendly_abilities=None, special_ability=None, hidden_abilities=None):
        # 固定資訊
        self.name = name
        self.anxiety_threshold = anxiety_threshold
        self.initial_location = initial_location
        self.forbidden_area = forbidden_area
        self.attribute = attribute
        self.special_ability = special_ability
        self.friendly_abilities = friendly_abilities or []
        self.hidden_abilities = hidden_abilities or []

        # 浮動資訊
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None
        self.abilities_used = []

    def reset(self):
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = self.initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None
        self.abilities_used.clear()

    def move(self, location):
        if self.alive and location != self.forbidden_area:
            self.current_location = location

    def change_anxiety(self, amount):
        self.anxiety += amount

    def change_conspiracy(self, amount):
        self.conspiracy += amount

    def change_friendship(self, amount):
        self.friendship += amount

    def use_ability(self, ability, target=None):
        if ability in self.friendly_abilities:
            # 根據能力的不同實現相應的邏輯
            if ability == "友好2：同地區的１名另外一個\"學生\"-1不安" and target:
                target.change_anxiety(-1)
            # 添加更多能力的實現邏輯
            self.abilities_used.append(ability)
            print(f"{self.name} 使用了能力：{ability}")
        else:
            print(f"{self.name} 沒有這個能力：{ability}")

    def use_hidden_ability(self, ability, target=None):
        if ability in self.hidden_abilities:
            # 根據隱藏能力的不同實現相應的邏輯
            print(f"{self.name} 使用了隱藏能力：{ability}，通知劇本家")
            self.abilities_used.append(ability)
            # 這裡可以添加邏輯來通知劇本家
        else:
            print(f"{self.name} 沒有這個隱藏能力：{ability}")

    def can_use_ability(self, ability):
        return ability not in self.abilities_used

    def __str__(self):
        return f"Character({self.name}, Anxiety: {self.anxiety}, Conspiracy: {self.conspiracy}, Friendship: {self.friendship}, Location: {self.current_location}, Alive: {self.alive})"


class CharacterManager(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.characters = []
        self.selected_character = None
        self.selected_ability = None

        self.character_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.character_listbox.grid(row=0, column=0, sticky="nsew")
        self.character_listbox.bind("<<ListboxSelect>>", self.on_character_select)

        self.character_details = tk.Label(self, text="請選擇一個角色")
        self.character_details.grid(row=0, column=1, sticky="nsew")

        self.actions_frame = tk.Frame(self)
        self.actions_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.load_characters()
        self.update_listbox()

    def load_characters(self):
        characters_data = load_character_database()
        for char_data in characters_data:
            character = Character(**char_data)
            self.characters.append(character)

    def update_listbox(self):
        self.character_listbox.delete(0, tk.END)
        for character in self.characters:
            self.character_listbox.insert(tk.END, character.name)

    def on_character_select(self, event):
        selection = self.character_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_character = self.characters[index]
            self.update_character_details()

    def update_character_details(self):
        if self.selected_character:
            details = (f"名稱: {self.selected_character.name}\n"
                       f"位置: {self.selected_character.current_location}\n"
                       f"不安: {self.selected_character.anxiety}\n"
                       f"陰謀: {self.selected_character.conspiracy}\n"
                       f"友好: {self.selected_character.friendship}\n"
                       f"死亡: {'是' if not self.selected_character.alive else '否'}")
            self.character_details.config(text=details)

            # 更新行動和能力
            self.update_actions_and_abilities()

    def update_actions_and_abilities(self):
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        actions_label = tk.Label(self.actions_frame, text="可用行動與能力")
        actions_label.pack()

        # 顯示角色的能力
        for ability in self.selected_character.friendly_abilities:
            if self.selected_character.can_use_ability(ability):
                ability_button = tk.Button(self.actions_frame, text=ability, command=lambda a=ability: self.select_ability(a))
                ability_button.pack()
            else:
                ability_button = tk.Button(self.actions_frame, text=ability, state=tk.DISABLED)
                ability_button.pack()

        # 顯示角色的隱藏能力
        for ability in self.selected_character.hidden_abilities:
            if self.selected_character.can_use_ability(ability):
                hidden_ability_button = tk.Button(self.actions_frame, text=ability, command=lambda a=ability: self.select_hidden_ability(a))
                hidden_ability_button.pack()
            else:
                hidden_ability_button = tk.Button(self.actions_frame, text=ability, state=tk.DISABLED)
                hidden_ability_button.pack()

    def select_ability(self, ability):
        self.selected_ability = ability
        self.character_details.config(text=f"選擇的能力: {ability}")
        # 檢查是否需要選擇目標角色
        if "同地區的" in ability:
            self.character_details.config(text=f"選擇的能力: {ability}\n請選擇目標角色")
            self.character_listbox.bind("<<ListboxSelect>>", self.on_target_select)
        else:
            self.execute_ability()

    def select_hidden_ability(self, ability):
        self.selected_ability = ability
        self.character_details.config(text=f"選擇的隱藏能力: {ability}")
        # 檢查是否需要選擇目標角色
        if "同地區的" in ability:
            self.character_details.config(text=f"選擇的隱藏能力: {ability}\n請選擇目標角色")
            self.character_listbox.bind("<<ListboxSelect>>", self.on_target_select_hidden)
        else:
            self.execute_hidden_ability()

    def on_target_select(self, event):
        selection = self.character_listbox.curselection()
        if selection:
            index = selection[0]
            target_character = self.characters[index]
            self.execute_ability(target_character)

    def on_target_select_hidden(self, event):
        selection = self.character_listbox.curselection()
        if selection:
            index = selection[0]
            target_character = self.characters[index]
            self.execute_hidden_ability(target_character)

    def execute_ability(self, target=None):
        if self.selected_character and self.selected_ability:
            self.selected_character.use_ability(self.selected_ability, target)
            self.update_character_details()
            self.selected_ability = None
            self.character_listbox.bind("<<ListboxSelect>>", self.on_character_select)

    def execute_hidden_ability(self, target=None):
        if self.selected_character and self.selected_ability:
            self.selected_character.use_hidden_ability(self.selected_ability, target)
            self.update_character_details()
            self.selected_ability = None
            self.character_listbox.bind("<<ListboxSelect>>", self.on_character_select)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("角色管理")
    character_manager = CharacterManager(root)
    character_manager.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
