import tkinter as tk
from tkinter import ttk, messagebox
from common.character import CharacterManager, friendship_ignore  # 引入 CharacterManager 和 friendship_ignore 函數

import tkinter as tk
from tkinter import messagebox

def check_friendship_ignore(character):
    """
    檢查角色的友好能力是否會被無效或無視。
    
    參數:
        character: 需要檢查的角色對象。
        
    返回:
        (bool, str): (是否無效或無視, 原因描述)
    """
    ignore, reason = friendship_ignore(character)
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口
    messagebox.showinfo("友好能力檢查結果", reason)
    root.destroy()
    return not ignore, reason

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

    def can_use_ability(self, character, ability):
        # 判斷角色的能力是否可以啟用
        if not character.alive:
            return False  # 角色必須是存活的

        if ability.get('active', False) and ability['trigger'](character) and not character.friendly_ability_usage[ability['name']]:
            if ability.get('limit_use', False) and character.friendly_ability_usage[ability['name']] == 'used':
                return False  # 能力已在此輪迴中使用過
            
            if ability.get('target_required', False):
                for target in self.character_manager.characters:
                    if target.alive or ability['name'] == '復活同地區的一具屍體':
                        if ability['target_condition'](target, character):
                            return True
            else:
                return True
        return False
    def use_classleader_ability(self, character, ability, target):
        # 處理特殊能力的使用邏輯
        if ability['name'] == '友好2：偵探回收1張【1輪迴只能使用1次】的行動卡（1輪迴限用1次）':
            if ability['trigger'](character) and not character.friendly_ability_usage[ability['name']]:
                if target and target.alive:
                    self.game.detective_recover_action_card()
                    character.friendly_ability_usage[ability['name']] = 'used'
                    return True
        return False

    def detective_recover_action_card(self):
        # 偵探回收一張限用行動卡的邏輯
        for action_card in self.game.action_cards:
            if action_card['limit_use'] and action_card['used']:
                action_card['used'] = False
                return action_card['name']
        return None
    
    def execute_ability(self, character, ability, target=None):
        # 執行角色的能力
        if (character, ability) in self.active_abilities:
            if ability.get('target_required', False) and target:
                ability['effect'](target)
                character.friendly_ability_usage[ability['name']] = True
                message = f"{character.name} 使用了能力：{ability['name']} 對 {target.name}"
            else:
                ability['effect'](self.game)
                character.friendly_ability_usage[ability['name']] = True
                message = f"{character.name} 使用了能力：{ability['name']}"
            self.check_abilities()
        else:
            message = "該角色的能力無法啟用"
        return message

    def get_character_by_name(self, name):
        for character in self.character_manager.characters:
            if character.name == name:
                return character
        return None

    def check_friendship_ignore(self, character):
        # 使用通用函數來檢查友好能力是否會被無效或無視
        return check_friendship_ignore(character)


class DetectiveAbilityGUI:
    def __init__(self, root, phase):
        self.root = root
        self.phase = phase
        self.selected_character = None
        self.selected_ability = None
        self.characters = self.phase.character_manager.characters
        self.create_widgets()

    def create_widgets(self):
        self.root.title("友好能力階段")

        # 第一個下拉式選單 - 選擇角色
        tk.Label(self.root, text="選擇角色").pack(pady=5)
        character_names = [character.name for character in self.characters if character.alive]
        self.character_combobox = ttk.Combobox(self.root, values=character_names)
        self.character_combobox.pack(pady=5)
        self.character_combobox.bind("<<ComboboxSelected>>", self.on_character_select)

        # 第二個下拉式選單 - 選擇能力
        tk.Label(self.root, text="選擇能力").pack(pady=5)
        self.ability_combobox = ttk.Combobox(self.root)
        self.ability_combobox.pack(pady=5)
        self.ability_combobox.bind("<<ComboboxSelected>>", self.on_ability_select)

        # 第三個下拉式選單 - 選擇目標
        tk.Label(self.root, text="選擇目標").pack(pady=5)
        self.target_combobox = ttk.Combobox(self.root)
        self.target_combobox.pack(pady=5)

        # 確定按鈕
        self.confirm_button = tk.Button(self.root, text="確定", command=self.confirm_selection)
        self.confirm_button.pack(pady=20)

        # 離開按鈕
        self.exit_button = tk.Button(self.root, text="離開", command=self.exit_phase)
        self.exit_button.pack(pady=20)

        # 消息框
        self.message_box = tk.Text(self.root, height=10, state='disabled')
        self.message_box.pack(pady=5)

    def on_character_select(self, event):
        character_name = self.character_combobox.get()
        self.selected_character = self.phase.get_character_by_name(character_name)
        if self.selected_character:
            # 更新第二個下拉式選單的選項
            abilities = [ability['name'] for ability in self.selected_character.friendly_abilities]
            self.ability_combobox.config(values=abilities)
            self.ability_combobox.set('')
            self.target_combobox.config(values=[''])

    def on_ability_select(self, event):
        ability_name = self.ability_combobox.get()
        self.select_ability(ability_name)

    def select_ability(self, ability_name):
        self.selected_ability = ability_name
        selected_ability = next((a for a in self.selected_character.friendly_abilities if a['name'] == ability_name), None)
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

    def confirm_selection(self):
        character_name = self.character_combobox.get()
        character = self.phase.get_character_by_name(character_name)
        ability_name = self.ability_combobox.get()
        target_name = self.target_combobox.get()

        ability = next((a for a in character.friendly_abilities if a['name'] == ability_name), None)
        target = self.phase.get_character_by_name(target_name) if target_name else None

        if ability:
            result = self.phase.execute_ability(character, ability, target)
            self.show_message(result)

    def exit_phase(self):
        if messagebox.askyesno("確認", "是否要結束友好能力階段？"):
            self.root.quit()

    def show_message(self, message):
        self.message_box.config(state='normal')
        self.message_box.insert(tk.END, message + '\n')
        self.message_box.config(state='disabled')

    def update_character_details(self):
        # 更新角色詳情的方法
        pass

if __name__ == "__main__":
    root = tk.Tk()
    character_manager = CharacterManager()
    character_manager.load_characters()  # 確保加載角色
    game = None  # 初始化遊戲對象
    scriptwriter = None  # 初始化劇本家對象
    phase = PlayerDetectiveAbilityPhase(character_manager, game, scriptwriter)
    gui = DetectiveAbilityGUI(root, phase)
    root.mainloop()