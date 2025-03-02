
from game import Game
import tkinter as tk
from scriptwriter.ai_gameset import AIGameSet
from game_gui import GameGUI

def main():

    # 1️⃣ 產生遊戲設定
    pre_game = Game()
    gameset = AIGameSet(pre_game)
    
    # 2️⃣ 使用 AIGameSet 的數據建立 Game 物件
    game = gameset.pre_game

    root = tk.Tk()
    root.title("慘劇rerpooper")
    game_gui = GameGUI(root, game, None)
    game.game_gui = game_gui  # ✅ 這行確保 Game 類別能夠存取 GUI
    game_gui.update_area_widgets()  # ✅ 這行確保地區顯示
    
    game.phase_manager.set_phases(game)  
    game.phase_manager.start_phase()  # 如果遊戲有主要運行迴圈，則啟動它
    print(game.phase_manager.current_phase)
    root.mainloop()
if __name__ == "__main__":
    main()
