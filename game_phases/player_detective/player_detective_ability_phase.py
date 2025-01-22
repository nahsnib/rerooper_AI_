import tkinter as tk
from tkinter import ttk, messagebox
from common.character import CharacterManager, friendship_ignore  # 引入 CharacterManager 和 friendship_ignore 函數

class PlayerDetectiveAbilityPhase:
    def __init__(self, character_manager, game, scriptwriter):
        self.character_manager = character_manager
        self.game = game
        self.scriptwriter = scriptwriter
        self.active_abilities = []

    def check_abilities(self):
        # 檢查哪些角色的能力可以啟用
        self.active_abilities = []
        for character in self.character_manager.characters:
            for ability in character.friendly_abilities:
                if self.can_use_ability(character, ability):
                    self.active_abilities.append((character, ability))
        self.highlight_active_abilities()

    def can_use_ability(self, character, ability):
        # 判斷角色的能力是否可以啟用
        if ability['trigger'](character) and not character.friendly_ability_usage[ability['name']]:
            if ability.get('target_required', False):
                for target in self.character_manager.characters:
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
                valid_targets = [target for target in self.character_manager.characters if ability['target_condition'](target, character)]
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
        for character in self.character_manager.characters:
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
        # 結束階段按鈕
        self.end_phase_button = tk.Button(self.root, text="結束本階段", command=self.confirm_end_phase)
        self.end_phase_button.pack()

        # 選擇角色的下拉式選單
        self.character_combobox = ttk.Combobox(self.root, values=[character.name for character in self.phase.character_manager.characters if character.alive])
        self.character_combobox.pack()
        self.character_combobox.bind("<<ComboboxSelected>>", self.on_character_select)

        # 選擇能力的下拉式選單
        self.ability_combobox = ttk.Combobox(self.root)
        self.ability_combobox.pack()
        self.ability_combobox.bind("<<ComboboxSelected>>", self.on_ability_select)

        # 確認按鈕
        self.confirm_button = tk.Button(self.root, text="確認", command=self.confirm_selection)
        self.confirm_button.pack()

    def confirm_end_phase(self):
        if messagebox.askyesno("確認", "是否確認結束本階段？"):
            self.root.quit()

    def on_character_select(self, event):
        character_name = self.character_combobox.get()
        character = self.phase.get_character_by_name(character_name)
        valid_abilities = [ability['name'] for ability in character.friendly_abilities if self.phase.can_use_ability(character, ability)]
        if valid_abilities:
            self.ability_combobox.config(values=valid_abilities)
            self.ability_combobox.set('')
        else:
            messagebox.showinfo("提示", "該角色沒有可使用的能力")

    def on_ability_select(self, event):
        self.selected_ability = self.ability_combobox.get()

    def confirm_selection(self):
        character_name = self.character_combobox.get()
        character = self.phase.get_character_by_name(character_name)
        ability_name = self.selected_ability
        ability = next((a for a in character.friendly_abilities if a['name'] == ability_name), None)
        
        if ability:
            if ability.get('target_required', False):
                valid_targets = [target.name for target in self.phase.character_manager.characters if ability['target_condition'](target, character)]
                if valid_targets:
                    target_name = self.choose_target(valid_targets)
                    target = self.phase.get_character_by_name(target_name)
                    if self.phase.check_friendship_ignore(character):
                        ability['effect'](target)
                        character.friendly_ability_usage[ability['name']] = True
                        self.update_board()
                    else:
                        messagebox.showinfo("提示", f"友好能力被取消或無效：{character.name} 的能力 {ability['name']}")
                else:
                    messagebox.showinfo("提示", "沒有有效的目標")
            else:
                if self.phase.check_friendship_ignore(character):
                    ability['effect'](self.phase.game)
                    character.friendly_ability_usage[ability['name']] = True
                    self.update_board()
                else:
                    messagebox.showinfo("提示", f"友好能力被取消或無效：{character.name} 的能力 {ability['name']}")
        self.phase.check_abilities()

    def choose_target(self, valid_targets):
        target_window = tk.Toplevel(self.root)
        target_window.title("選擇目標")
        target_label = tk.Label(target_window, text="選擇目標")
        target_label.pack()

        target_combobox = ttk.Combobox(target_window, values=valid_targets)
        target_combobox.pack()

        def confirm_target():
            target_name = target_combobox.get()
            target_window.destroy()
            self.selected_target = target_name

        confirm_button = tk.Button(target_window, text="確認", command=confirm_target)
        confirm_button.pack()

        target_window.wait_window()
        return self.selected_target

    def update_board(self):
        # 更新遊戲板狀態
        print("更新遊戲板狀態")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("偵探能力階段")
    # 初始化角色管理器和遊戲
    character_manager = CharacterManager(root)
    character_manager.load_characters()  # 確保加載角色
    game = None  # 初始化遊戲對象
    scriptwriter = None  # 初始化劇本家對象
    phase = PlayerDetectiveAbilityPhase(character_manager, game, scriptwriter)
    gui = DetectiveAbilityGUI(root, phase)
    root.mainloop()