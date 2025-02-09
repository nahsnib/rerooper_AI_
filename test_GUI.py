import tkinter as tk
from common.character import CharacterManager
from game_gui import GameGUI
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from scriptwriter.ai_gameset import AIGameSet
from game import Game  # 確保我們使用正式的 Game 類別


# 創建測試窗口
def main():
    root = tk.Tk()
    root.title("遊戲測試 - 偵探行動階段")

    # 1️⃣ 啟動遊戲與角色管理器
    game = Game
    character_manager = CharacterManager()

    # 2️⃣ 初始化 AI Game Set
    game = AIGameSet()

    # 3️⃣ 啟動 GUI
    game_gui = GameGUI(root, game, character_manager.get_pickup_characters(), None)

    # 4️⃣  初始化偵探行動階段
    action_phase = PlayerDetectiveActionPhase(game, game_gui)
    action_phase.execute()
    
    print("\n=== 偵探行動階段開始 ===")
    for action in action_phase.scriptwriter_selections:
        print(f"劇本家行動 - 目標：{action['target']}，動作：{action['action'].name}")

    # 5️⃣ 更新 GUI 並啟動
    game_gui.update()
    root.mainloop()

if __name__ == "__main__":
    main()
