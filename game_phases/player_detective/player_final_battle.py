import tkinter as tk
from tkinter import ttk

class FinalBattle:
    def __init__(self, game):
        self.game = game
        self.rule_table = game.selected_rule_table
        self.chance = 3
        self.selections = {}  # 存儲玩家的選擇

    def execute(self):
        self.create_gui()
        self.root.mainloop()
    
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Final Battle")
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # 設定 main_frame 內部的 Grid 欄位比例
        self.main_frame.columnconfigure(0, weight=1)  # A 角色選擇
        self.main_frame.columnconfigure(1, weight=2)  # B 正確答案
        self.main_frame.columnconfigure(2, weight=2)  # C 其他資訊
        
        self.create_character_and_role_pair()
        self.create_the_answer()
        self.create_other_info()
        
    def create_character_and_role_pair(self):
        # 第一區：角色選擇
        self.pair_frame = tk.Frame(self.main_frame)
        self.pair_frame.grid(row=0, column=0, sticky="ns")
        tk.Label(self.pair_frame, text="選擇角色身份", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

        self.role_options = [role.name for role in self.rule_table.roles] + ["普通人"]
        for i, character in enumerate(self.game.character_manager.characters):
            tk.Label(self.pair_frame, text=character.name, width=20, anchor="w").grid(row=i+1, column=0, sticky="w")
            var = tk.StringVar(value="普通人")
            dropdown = ttk.Combobox(self.pair_frame, textvariable=var, values=self.role_options, state="readonly")
            dropdown.grid(row=i+1, column=1)
            self.selections[character.name] = var

        self.result_label = tk.Label(self.pair_frame, text="剩餘嘗試次數: 3", font=("Arial", 10))
        self.result_label.grid(row=len(self.game.character_manager.characters) + 1, column=0, columnspan=2)

        confirm_button = tk.Button(self.pair_frame, text="確認", command=self.check_result)
        confirm_button.grid(row=len(self.game.character_manager.characters) + 2, column=0, columnspan=2)

    def create_the_answer(self):
        # 第二區：真實身份揭曉
        self.answer_frame = tk.Frame(self.main_frame)
        self.answer_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.answer_frame, text="真實身份", font=("Arial", 12, "bold")).grid(row=0, column=0)
        self.identity_text = tk.Text(self.answer_frame, height=20, width=25, state=tk.DISABLED)
        self.identity_text.grid(row=1, column=0)

    def create_other_info(self):    
        # 第三區：主規則、副規則、每日事件與犯人
        self.other_info_frame = tk.Frame(self.main_frame)
        self.other_info_frame.grid(row=0, column=2, sticky="nsew")
        tk.Label(self.other_info_frame, text="遊戲資訊", font=("Arial", 12, "bold")).grid(row=0, column=0)
        self.info_text = tk.Text(self.other_info_frame, height=20, width=25, state=tk.DISABLED)
        self.info_text.grid(row=1, column=0)

    def check_result(self):
        correct = all(self.selections[char_name].get() == char.role.name 
              for char_name, char in [(c.name, c) for c in self.game.character_manager.characters])

        if correct:
            self.show_result("偵探獲勝！")
        else:
            self.chance -= 1
            if self.chance == 0:
                self.show_result("偵探敗北...！")
            else:
                self.result_label.config(text=f"剩餘嘗試次數: {self.chance}")
    
    def show_result(self, message):
        self.result_label.config(text=message)
        self.root.update_idletasks()
        # 顯示真實身份
        self.identity_text.config(state=tk.NORMAL)
        self.identity_text.delete("1.0", tk.END)
        for char in self.game.character_manager.characters:
            self.identity_text.insert(tk.END, f"{char.name}: {char.role.name}\n")
        self.identity_text.config(state=tk.DISABLED)
        
        # 顯示遊戲規則與事件資訊
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, f"主規則: {self.game.selected_main_rule[0].name}\n")
        self.info_text.insert(tk.END, f"副規則X1:{self.game.selected_sub_rules[0].name}\n")
        self.info_text.insert(tk.END, f"副規則X2:{self.game.selected_sub_rules[1].name}\n")
        
        self.info_text.insert(tk.END, "\n事件與犯人揭曉:\n")
        events = self.game.time_manager.get_scheduled_events(self.game.scheduled_events)
        for date in range(1, self.game.time_manager.total_days + 1):
            if date in events:  # **確保該日期有對應的事件**
                event = events[date]  # **直接取得該日期的事件**
                self.info_text.insert(tk.END,f"第{date}天: {event.name}的犯人為{event.criminal.name}\n")
        
        self.info_text.config(state=tk.DISABLED)



