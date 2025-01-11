import tkinter as tk
from tkinter import messagebox
from game_phase.action_phase import ActionPhase
from game_phase.ability_phase_1 import AbilityPhase1
from game_phase.ability_phase_2 import AbilityPhase2
from game_phase.event_phase import EventPhase
from game_phase.night_phase import NightPhase
from scriptwriter.gameset import GameSet
from common.character import CharacterManager
from game import Player

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("遊戲")
        
        # 初始化角色管理器
        self.character_manager = CharacterManager(self.root)
        self.character_manager.pack(expand=True, fill=tk.BOTH)
        
        # 選擇玩家身份
        self.choose_role()

    def choose_role(self):
        self.role_window = tk.Toplevel(self.root)
        self.role_window.title("選擇角色")
        
        label = tk.Label(self.role_window, text="請選擇您的角色:")
        label.pack(pady=10)
        
        detective_button = tk.Button(self.role_window, text="偵探", command=lambda: self.set_role("偵探"))
        detective_button.pack(pady=5)
        
        scriptwriter_button = tk.Button(self.role_window, text="劇本家（未實現）", state=tk.DISABLED)
        scriptwriter_button.pack(pady=5)

    def set_role(self, role):
        self.role = role
        self.role_window.destroy()
        self.show_message(f"您選擇了角色：{role}")

        # 初始化玩家
        self.player = Player(self.role)
        
        # 如果玩家選擇劇本家，進行劇本編寫
        if self.role == "劇本家":
            self.setup_script()
        else:
            # 如果玩家選擇偵探，直接開始遊戲
            self.start_game()

    def show_message(self, message):
        messagebox.showinfo("提示", message)

    def setup_script(self):
        self.show_message("劇本家正在設置劇本...")
        # 使用 GameSet 模組進行劇本設置
        self.game_set = GameSet(self.character_manager)
        self.game_set.setup()
        self.show_message("劇本設置完成！")
        # 劇本設置完成後開始遊戲
        self.start_game()

    def start_game(self):
        self.show_message("遊戲開始！")
        # 展示遊戲地區等要素
        self.show_game_areas()
        
        # 進入遊戲循環
        self.game_loop()

    def show_game_areas(self):
        self.area_window = tk.Toplevel(self.root)
        self.area_window.title("遊戲地區")
        
        areas = ["學校", "都市", "神社", "醫院"]
        for area in areas:
            label = tk.Label(self.area_window, text=area)
            label.pack(pady=5)

    def game_loop(self):
        # 每個回合依序啟用各個階段
        self.action_phase = ActionPhase(self.character_manager)
        self.ability_phase_1 = AbilityPhase1(self.character_manager)
        self.ability_phase_2 = AbilityPhase2(self.character_manager)
        self.event_phase = EventPhase(self.character_manager)
        self.night_phase = NightPhase(self.character_manager)
        
        # 這裡可以依照遊戲邏輯來進行各個階段的調用
        self.action_phase.execute()
        self.ability_phase_1.execute()
        self.ability_phase_2.execute()
        self.event_phase.execute()
        self.night_phase.execute()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
