import tkinter as tk
from game_gui import GameGUI
from game import Game

def main():
    pre_game = Game()
    game = Game()  # 創建遊戲對象
    root = tk.Tk()
    game_gui = GameGUI(root, pre_game, None)
    pre_game.game_gui = game_gui  # ✅ 這行確保 Game 類別能夠存取 GUI
    game = game.initialize_and_record_game(pre_game)  # 初始化並記錄遊戲
    game.phase_manager.run()  # 如果遊戲有主要運行迴圈，則啟動它
    try:
        pre_game = Game()
        game = Game()  # 創建遊戲對象
        game = game.initialize_and_record_game(pre_game)  # 初始化並記錄遊戲
        game.phase_manager.run()  # 如果遊戲有主要運行迴圈，則啟動它
    except Exception as e:
        print(f"遊戲初始化失敗: {e}")  # 防止遊戲因錯誤而崩潰

if __name__ == "__main__":
    main()
