import tkinter as tk
from tkinter import messagebox
from game_phase.night_phase import NightPhase
from common.character import CharacterManager

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("遊戲")
        
        # Step 1: 選擇角色
        self.choose_role()
        
        # Step 2: 初始化角色管理器
        self.character_manager = CharacterManager(self.root)
        self.character_manager.pack(expand=True, fill=tk.BOTH)
        
        # Step 3: 進入遊戲階段
        self.start_game()

    def choose_role(self):
        self.role_window = tk.Toplevel(self.root)
        self.role_window.title("選擇角色")

        label = tk.Label(self.role_window, text="請選擇您的角色:")
        label.pack(pady=10)

        detective_button = tk.Button(self.role_window, text="偵探", command=lambda: self.set_role("偵探"))
        detective_button.pack(pady=5)

        scriptwriter_button = tk.Button(self.role_window, text="劇本家", command=lambda: self.set_role("劇本家"))
        scriptwriter_button.pack(pady=5)

    def set_role(self, role):
        self.role = role
        self.role_window.destroy()
        self.show_message(f"您選擇了角色：{role}")

    def show_message(self, message):
        messagebox.showinfo("提示", message)

    def start_game(self):
        # 展示遊戲地區等要素
        self.show_game_areas()
        
        # 進入夜間階段
        self.night_phase = NightPhase(self.character_manager)
        self.night_phase.execute()

    def show_game_areas(self):
        # 這裡是展示遊戲地區的邏輯
        self.area_window = tk.Toplevel(self.root)
        self.area_window.title("遊戲地區")
        
        areas = ["學校", "都市", "神社", "醫院", "鬧區"]
        for area in areas:
            label = tk.Label(self.area_window, text=area)
            label.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
