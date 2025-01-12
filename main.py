import tkinter as tk
from tkinter import messagebox
from common.board import Board
from scriptwriter.ai_gameset import AIGameSet
from game import GameLoop, Player
from common.character import CharacterManager


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
        
        scriptwriter_button = tk.Button(self.role_window, text="劇本家（目前不可用）", state=tk.DISABLED)
        scriptwriter_button.pack(pady=5)

    def set_role(self, role):
        self.role = role
        self.role_window.destroy()
        self.show_message(f"您選擇了角色：{role}")

        # 無論選擇什麼角色，都當成玩家想扮演偵探
        self.role = "偵探"
        self.player = Player(self.role)

        # 設置遊戲版圖
        self.setup_board()

        # 啟用 AI 劇本家設置
        self.setup_ai_scriptwriter()

        # 開始遊戲
        self.start_game()

    def show_message(self, message):
        messagebox.showinfo("提示", message)

    def setup_board(self):
        self.show_message("設置遊戲版圖...")
        self.board = Board()
        self.board.setup()

    def setup_ai_scriptwriter(self):
        self.show_message("AI 劇本家正在設置劇本...")
        ai_gameset = AIGameSet()
        ai_gameset.construct_scenario()
        self.show_message("劇本設置完成！")

    def start_game(self):
        self.show_message("遊戲開始！")
        # 初始化並運行遊戲循環
        self.game_loop = GameLoop(self.character_manager, self.role)
        self.game_loop.run()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
