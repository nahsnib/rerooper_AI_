import tkinter as tk
from common.character import CharacterManager
from common.board import GameBoard
from game import GameLoop

if __name__ == "__main__":
    root = tk.Tk()
    root.title("遊戲版面")

    character_manager = CharacterManager()
    role = "偵探"
    total_days = 30
    scheduled_events = {
        3: "事件A",
        7: "事件B",
        15: "事件C"
    }

    game = GameLoop(character_manager, role, total_days, scheduled_events)
    game_board = GameBoard(root, game)

    def update_game_board():
        game.increment_day()
        game_board.update()
        root.after(1000, update_game_board)

    root.after(1000, update_game_board)
    root.mainloop()
