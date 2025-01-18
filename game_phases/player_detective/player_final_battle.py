import tkinter as tk
from tkinter import ttk
from common.character import CharacterManager
from database.RuleTable import RuleTable

class FinalBattle:
    def __init__(self, root, character_manager, rule_table):
        self.root = root
        self.character_manager = character_manager
        self.rule_table = rule_table
        self.identities = ["普通人"] + self.rule_table.get_identities()
        self.character_identities = {}  # 用於存儲玩家選擇的身份

        self.create_widgets()

    def create_widgets(self):
        # 建立表格
        characters = self.character_manager.get_all_characters()
        num_characters = len(characters)
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=0, column=0, padx=10, pady=10)

        # 第一橫列：展示所有角色
        for i, character in enumerate(characters):
            tk.Label(self.table_frame, text=character.name).grid(row=0, column=i)

        # 第二橫列：每個格子都有一個下拉式選單
        self.identity_vars = []
        for i, character in enumerate(characters):
            identity_var = tk.StringVar(value="普通人")
            self.identity_vars.append(identity_var)
            dropdown = ttk.Combobox(self.table_frame, textvariable=identity_var, values=self.identities, state='readonly')
            dropdown.grid(row=1, column=i)
            self.character_identities[character.name] = identity_var

        # 按鈕：最終決戰！
        self.final_battle_button = tk.Button(self.root, text="最終決戰！", command=self.check_answers)
        self.final_battle_button.grid(row=1, column=0, pady=10)

    def check_answers(self):
        # 檢視玩家的答案是否正確
        correct = True
        for character in self.character_manager.get_all_characters():
            selected_identity = self.character_identities[character.name].get()
            actual_identity = character.secret_identity if character.secret_identity else "普通人"
            if selected_identity != actual_identity:
                correct = False
                break

        if correct:
            self.show_message("恭喜！你成功識破了所有角色的身份！")
        else:
            self.show_message("很遺憾，你未能識破所有角色的身份。")

    def show_message(self, message):
        # 顯示訊息給玩家
        msg_box = tk.Toplevel(self.root)
        msg_box.title("結果")
        tk.Label(msg_box, text=message).pack(padx=20, pady=20)
        tk.Button(msg_box, text="確定", command=msg_box.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("最終決戰")
    
    character_manager = CharacterManager()
    rule_table = RuleTable()

    final_battle = FinalBattle(root, character_manager, rule_table)

    root.mainloop()
