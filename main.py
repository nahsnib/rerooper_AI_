
from game import Game
import tkinter as tk
from scriptwriter.ai_gameset import AIGameSet
from game_gui import GameGUI

def main():
    root = tk.Tk()
    root.title("測試友好能力階段")

    # 1️⃣ 產生遊戲設定
    pre_game = Game()
    gameset = AIGameSet(pre_game)
    
    # 2️⃣ 使用 AIGameSet 的數據建立 Game 物件
    game = gameset.pre_game

    game_gui = GameGUI(root, game, None)
    game.game_gui = game_gui  # ✅ 這行確保 Game 類別能夠存取 GUI
    game_gui.update_area_widgets()  # ✅ 這行確保地區顯示
    print(f"game: {game}")  
    print(f"game.game_gui: {getattr(game, 'game_gui', None)}")  
    game.phase_manager.run()  # 如果遊戲有主要運行迴圈，則啟動它

if __name__ == "__main__":
    main()
