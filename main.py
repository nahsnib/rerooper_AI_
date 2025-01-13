import tkinter as tk
from tkinter import messagebox
from common.character import CharacterManager
from common.board import GameBoard
from game import GameLoop
from scriptwriter.ai_gameset import AIGameSet

def start_game():
    root = tk.Tk()
    root.title("遊戲版面")

    character_manager = CharacterManager()
    gameset = AIGameSet(character_manager)

    # 獲取公開信息
    public_info = gameset.get_public_info()
    total_days = public_info["total_days"]
    total_cycles = public_info["total_cycles"]
    scheduled_events = public_info["scheduled_events"]

    game = GameLoop(character_manager, "偵探", total_days, total_cycles, scheduled_events)
    game_board = GameBoard(root, game)

    def update_game_board():
        game.increment_day()
        game_board.update()
        root.after(1000, update_game_board)

    root.after(1000, update_game_board)
    root.mainloop()

if __name__ == "__main__":
    # 顯示提示訊息
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口
    messagebox.showinfo("提示", "測試版遊戲僅提供玩家為偵探的模式")
