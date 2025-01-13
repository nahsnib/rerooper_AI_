import tkinter as tk
from tkinter import ttk
from database.character_database import load_character_database

class Character:
    def __init__(self, id, name, anxiety_threshold, initial_location, forbidden_area, attribute, friendly_abilities=None, role_abilities=None, special_ability=None, traits=None):
        # 固定資訊
        self.id = id  # 角色編號
        self.name = name
        self.anxiety_threshold = anxiety_threshold
        self.initial_location = initial_location
        self.forbidden_area = forbidden_area
        self.attribute = attribute
        self.special_ability = special_ability
        self.friendly_abilities = friendly_abilities or []
        self.role_abilities = role_abilities or []
        self.traits = traits or []  # 添加的特性屬性

        # 浮動資訊
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None
        self.friendly_ability_usage = {ability['name']: False for ability in self.friendly_abilities}
        self.role_ability_usage = {ability['name']: False for ability in self.role_abilities}

    def reset(self):
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = self.initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None
        self.reset_ability_usage()

    def move(self, location):
        if self.alive and location != self.forbidden_area:
            self.current_location = location

    def change_anxiety(self, amount):
        self.anxiety += amount

    def change_conspiracy(self, amount):
        self.conspiracy += amount

    def change_friendship(self, amount):
        self.friendship += amount

    def use_friendly_ability(self, ability_name, target=None):
        for ability in self.friendly_abilities:
            if ability['name'] == ability_name:
                if not self.friendly_ability_usage[ability_name] and ability['trigger'](self):
                    if ability['target_required']:
                        if target and ability['target_condition'](target, self):
                            ability['effect'](target)
                            self.friendly_ability_usage[ability_name] = True
                            print(f"{self.name} 使用了能力：{ability_name} 對 {target.name}")
                            return
                        else:
                            print(f"無效的目標：{target.name} 不符合條件")
                            return
                    else:
                        ability['effect'](self)
                        self.friendly_ability_usage[ability_name] = True
                        print(f"{self.name} 使用了能力：{ability_name}")
                        return
                else:
                    print(f"{self.name} 的友好度不足以使用能力：{ability_name} 或今天已使用過")
                    return
        print(f"{self.name} 沒有這個友好能力：{ability_name}")

    def use_role_ability(self, ability_name, target=None):
        for ability in self.role_abilities:
            if ability['name'] == ability_name:
                if not self.role_ability_usage[ability_name]:
                    if ability['target_required']:
                        if target and ability['target_condition'](target, self):
                            ability['effect'](target)
                            self.role_ability_usage[ability_name] = True
                            print(f"{self.name} 使用了身分能力：{ability_name} 對 {target.name}")
                            return
                        else:
                            print(f"無效的目標：{target.name} 不符合條件")
                            return
                    else:
                        ability['effect'](self)
                        self.role_ability_usage[ability_name] = True
                        print(f"{self.name} 使用了身分能力：{ability_name}")
                        return
                else:
                    print(f"{self.name} 今天已使用過身分能力：{ability_name}")
                    return
        print(f"{self.name} 沒有這個身分能力：{ability_name}")

    def can_use_ability(self, ability_name):
        return (ability_name not in self.friendly_ability_usage or not self.friendly_ability_usage[ability_name]) and \
               (ability_name not in self.role_ability_usage or not self.role_ability_usage[ability_name])

    def reset_ability_usage(self):
        for ability in self.friendly_ability_usage:
            self.friendly_ability_usage[ability] = False
        for ability in self.role_ability_usage:
            self.role_ability_usage[ability] = False

    def reveal_identity(self):
        self.identity_revealed = True
        print(f"{self.name} 的身份已公開")

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
            character = Character(**char_data.__dict__)  # 使用角色的字典來初始化
            self.characters.append(character)

    def update_listbox(self):
        self.character_listbox.delete(0, tk.END)
        for character in self.characters:
            self.character_listbox.insert(tk.END, f"{character.id}: {character.name}")

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

        # 顯示角色的友好能力和身分能力
        for ability in self.selected_character.friendly_abilities + self.selected_character.role_abilities:
            ability_name = ability['name']
            if self.selected_character.can_use_ability(ability_name):
                ability_button = tk.Button(self.actions_frame, text=ability_name, command=lambda a=ability_name: self.select_ability(a))
                ability_button.pack()
            else:
                ability_button = tk.Button(self.actions_frame, text=ability_name, state=tk.DISABLED)
                ability_button.pack()

    def select_ability(self, ability_name):
        self.selected_ability = ability_name
        self.character_details.config(text=f"選擇的能力: {ability_name}")
        # 檢查是否需要選擇目標角色
        selected_ability = next((a for a in self.selected_character.friendly_abilities + self.selected_character.role_abilities if a['name'] == ability_name), None)
        if selected_ability and selected_ability['target_required']:
            self.character_details.config(text=f"選擇的能力: {ability_name}\n請選擇目標角色")
            self.character_listbox.bind("<<ListboxSelect>>", self.on_target_select)
        else:
            self.execute_ability()

    def on_target_select(self, event):
        selection = self.character_listbox.curselection()
        if selection:
            index = selection[0]
            target_character = self.characters[index]
            self.execute_ability(target_character)

    def execute_ability(self, target=None):
        if self.selected_character and self.selected_ability:
            self.selected_character.use_friendly_ability(self.selected_ability, target)
            self.update_character_details()
            self.selected_ability = None
            self.character_listbox.bind("<<ListboxSelect>>", self.on_character_select)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("角色管理")
    character_manager = CharacterManager(root)
    character_manager.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
