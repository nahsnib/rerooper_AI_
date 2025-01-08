# main.py

import tkinter as tk
from tkinter import messagebox
from common.character import CharacterManager
from game_phases.action_phase import ActionPhase
from game_phases.event_phase import EventPhase
from game_phases.night_phase import NightPhase
from game_phases.cycle_end import CycleEnd
from game_phases.final_battle import FinalBattle
from scriptwriter.gameset import ScriptEditor

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("遊戲")
        
        # 創建角色管理器
        self.character_manager = CharacterManager(self.root)
        self.character_manager.pack(expand=True, fill=tk.BOTH)
        
        # 初始化劇本編輯器
        self.script_editor = ScriptEditor()
        
        # 初始化遊戲階段
        self.action_phase = ActionPhase(self.character_manager)
        self.event_phase = EventPhase(self.character_manager)
        self.night_phase = NightPhase(self.character_manager)
        self.cycle_end = CycleEnd(self.character_manager)
        self.final_battle = FinalBattle(self.character_manager)
        
        self.current_phase = None
        
        # 角色選擇
        self.player_role = None
        self.ai_role = None

        # 開始角色選擇
        self.choose_role()

    def choose_role(self):
        role_window = tk.Toplevel(self.root)
        role_window.title("選擇角色")

        label = tk.Label(role_window, text="請選擇您的角色:")
        label.pack(pady=10)

        detective_button = tk.Button(role_window, text="偵探", command=lambda: self.set_role("偵探", "劇本家", role_window))
        detective_button.pack(pady=5)

        scriptwriter_button = tk.Button(role_window, text="劇本家", command=lambda: self.set_role("劇本家", "偵探", role_window))
        scriptwriter_button.pack(pady=5)

    def set_role(self, player_role, ai_role, window):
        self.player_role = player_role
        self.ai_role = ai_role
        window.destroy()
        messagebox.showinfo("角色選擇", f"您選擇了扮演 {self.player_role}，AI 將扮演 {self.ai_role}")
        self.start_game()

    def construct_scenario(self):
        self.script_editor.construct_scenario()
        # 更新角色管理器中的角色
        self.character_manager.characters = self.script_editor.characters
        self.character_manager.update_listbox()
        # 開始遊戲循環
        self.start_game()

    def start_game(self):
        if self.player_role == "偵探":
            self.construct_scenario()  # AI 構築劇本
        self.next_phase(self.action_phase)

    def next_phase(self, phase):
        self.current_phase = phase
        phase.execute()
        
        # 根據條件切換到下一個階段
        if isinstance(phase, ActionPhase):
            self.next_phase(self.event_phase)
        elif isinstance(phase, EventPhase):
            self.next_phase(self.night_phase)
        elif isinstance(phase, NightPhase):
            if self.cycle_end.is_game_over():
                self.next_phase(self.final_battle)
            else:
                self.next_phase(self.cycle_end)
        elif isinstance(phase, CycleEnd):
            self.start_game()  # 從新一輪開始
        elif isinstance(phase, FinalBattle):
            print("遊戲結束")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
