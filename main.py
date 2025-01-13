import tkinter as tk
from common.character import CharacterManager
from common.board import GameBoard
from game import GameLoop
from scriptwriter.ai_gameset import AIGameSet

if __name__ == "__main__":
    root = tk.Tk()
    root.title("遊戲版面")

    character_manager = CharacterManager()
    gameset = AIGameSet(character_manager)

    # 獲取公開信息
    public_info = gameset.get_public_info()
    total_days = public_info["total_days"]
    scheduled_events = public_info["scheduled_events"]

    game = GameLoop(character_manager, total_days, scheduled_events)
    game_board = GameBoard(root, game)

    def update_game_board():
        game.increment_day()
        game_board.update()
        root.after(1000, update_game_board)

    root.after(1000, update_game_board)
    root.mainloop()
