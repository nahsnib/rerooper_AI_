
import tkinter as tk
from tkinter import ttk
from database.character_database import load_character_database

class Character:
    def __init__(self, name, anxiety_threshold, initial_location, forbidden_area, attribute, friendly_abilities=None, special_ability=None):
        # 固定資訊
        self.name = name
        self.anxiety_threshold = anxiety_threshold
        self.initial_location = initial_location
        self.forbidden_area = forbidden_area
        self.attribute = attribute
        self.special_ability = special_ability
        self.friendly_abilities = friendly_abilities or []

        # 浮動資訊
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None

    def reset(self):
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = self.initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None

    def move(self, location):
        if self.alive and location != self.forbidden_area:
            self.current_location = location

    def change_anxiety(self, amount):
        self.anxiety += amount

    def change_conspiracy(self, amount):
        self.conspiracy += amount

    def change_friendship(self, amount):
        self.friendship += amount

    def __str__(self):
        return f"{self.name} (位置: {self.current_location}, 不安: {self.anxiety}, 陰謀: {self.conspiracy}, 友好: {self.friendship}, 死亡: {self.alive})"

class CharacterManager(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.characters = []
        self.selected_character = None

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

        # 行動階段和能力階段的行動和能力顯示（示例）
        actions = ["行動1", "行動2", "行動3"]
        abilities = ["能力1", "能力2", "能力3"]

        for action in actions:
            action_button = tk.Button(self.actions_frame, text=action)
            action_button.pack()

        for ability in abilities:
            ability_button = tk.Button(self.actions_frame, text=ability)
            ability_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("角色管理")
    character_manager = CharacterManager(root)
    character_manager.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
