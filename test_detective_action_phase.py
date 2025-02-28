import tkinter as tk
from game_gui import GameGUI
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from scriptwriter.ai_gameset import AIGameSet
from game import Game

# 創建測試窗口
def main():
    root = tk.Tk()
    root.title("測試友好能力階段")

    # 1️⃣ 產生遊戲設定
    pre_game = Game()
    gameset = AIGameSet(pre_game)
    
    # 2️⃣ 使用 AIGameSet 的數據建立 Game 物件
    game = gameset.pre_game

    # 🟢 讓所有角色 +N 友好
    for char in game.character_manager.characters:
        char.change_friendship(5)
        char.change_anxiety(pre_game,2)


    game_gui = GameGUI(root, game, None)
    game.game_gui = game_gui  # ✅ 這行確保 Game 類別能夠存取 GUI
    game_gui.update_area_widgets()  # ✅ 這行確保地區顯示

    phase = PlayerDetectiveActionPhase(game)
    game.game_gui.set_phase(phase)
    phase.execute()


    # 4️⃣ 更新 GUI 並啟動
    game.game_gui.root.update_idletasks()
    root.mainloop()


if __name__ == "__main__":
    main()
