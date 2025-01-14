import tkinter as tk
from tkinter import messagebox
from common.character import friendship_ignore  # 引入 friendship_ignore 函數

class PlayerDetectiveAbilityPhase:
    def __init__(self, character_manager, game, scriptwriter):
        self.character_manager = character_manager
        self.game = game
        self.scriptwriter = scriptwriter
        self.active_abilities = []

    def check_abilities(self):
        # 檢查哪些角色的能力可以啟用
        self.active_abilities = []
        for character in self.character_manager.get_all_characters():
            for ability in character.friendly_abilities:
                if self.can_use_ability(character, ability):
                    self.active_abilities.append((character, ability))
        self.highlight_active_abilities()

    def can_use_ability(self, character, ability):
        # 判斷角色的能力是否可以啟用
        if ability['trigger'](character) and not character.friendly_ability_usage[ability['name']]:
            if ability.get('target_required', False):
                for target in self.character_manager.get_all_characters():
                    if ability['target_condition'](target, character):
                        return True
            else:
                return True
        return False

    def highlight_active_abilities(self):
        # 高亮可啟用的能力
        print("以下角色的能力可以啟用:")
        for character, ability in self.active_abilities:
            print(f"{character.name} - {ability['name']}")

    def execute_ability(self, character, ability):
        # 執行角色的能力
        if (character, ability) in self.active_abilities:
            if ability.get('target_required', False):
                valid_targets = [target for target in self.character_manager.get_all_characters() if ability['target_condition'](target, character)]
                if valid_targets:
                    target = self.choose_target(valid_targets)
                    if self.check_friendship_ignore(character):
                        ability['effect'](target)
                        character.friendly_ability_usage[ability['name']] = True
                        print(f"{character.name} 使用了能力：{ability['name']} 對 {target.name}")
                    else:
                        print(f"友好能力被取消或無效：{character.name} 的能力 {ability['name']}")
                else:
                    print("沒有有效的目標")
                    return
            else:
                if self.check_friendship_ignore(character):
                    ability['effect'](self.game)
                    character.friendly_ability_usage[ability['name']] = True
                    print(f"{character.name} 使用了能力：{ability['name']}")
                else:
                    print(f"友好能力被取消或無效：{character.name} 的能力 {ability['name']}")
            self.check_abilities()
        else:
            print("該角色的能力無法啟用")

    def choose_target(self, valid_targets):
        # 選擇目標
        print("可選目標:")
        for i, target in enumerate(valid_targets):
            print(f"{i + 1}. {target.name}")
        choice = int(input("選擇目標編號: ")) - 1
        return valid_targets[choice]

    def check_friendship_ignore(self, character):
        # 檢查角色的友好能力是否會被無效或無視
        ignore, reason = friendship_ignore(character)
        print(reason)
        return not ignore

    def start(self):
        self.check_abilities()
        while True:
            choice = input("選擇要啟用的角色能力或輸入 'end' 結束階段: ")
            if choice == 'end':
                break
            else:
                selected_character = self.get_character_by_name(choice)
                if selected_character:
                    self.choose_ability(selected_character)
                else:
                    print("無效的選擇")

    def get_character_by_name(self, name):
        for character in self.character_manager.get_all_characters():
            if character.name == name:
                return character
        return None

    def choose_ability(self, character):
        # 選擇角色的能力
        valid_abilities = [ability for ability in character.friendly_abilities if self.can_use_ability(character, ability)]
        if valid_abilities:
            print(f"{character.name} 的可用能力:")
            for i, ability in enumerate(valid_abilities):
                print(f"{i + 1}. {ability['name']}")
            choice = int(input("選擇能力編號: ")) - 1
            self.execute_ability(character, valid_abilities[choice])
        else:
            print("該角色沒有可用的能力")

# PlayerDetectiveAbilityPhase GUI 的簡單範例
class DetectiveAbilityGUI:
    def __init__(self, root, phase):
        self.root = root
        self.phase = phase
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="選擇要啟用的角色能力")
        self.label.pack()

        self.character_listbox = tk.Listbox(self.root)
        self.character_listbox.pack()
        self.update_character_list()

        self.ability_listbox = tk.Listbox(self.root)
        self.ability_listbox.pack()

        self.character_listbox.bind('<<ListboxSelect>>', self.on_character_select)

        self.confirm_button = tk.Button(self.root, text="確認", command=self.confirm_selection)
        self.confirm_button.pack()

    def update_character_list(self):
        self.character_listbox.delete(0, tk.END)
        for character, ability in self.phase.active_abilities:
            self.character_listbox.insert(tk.END, character.name)

    def on_character_select(self, event):
        selected_index = self.character_listbox.curselection()
        if selected_index:
            character_name = self.character_listbox.get(selected_index)
            character = self.phase.get_character_by_name(character_name)
            self.update_ability_list(character)

    def update_ability_list(self, character):
        self.ability_listbox.delete(0, tk.END)
        valid_abilities = [ability for ability in character
