import tkinter as tk
from common.character import CharacterManager, Character
from common.area_and_date import TimeManager
from game_gui import GameGUI
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from scriptwriter.ai_gameset import AIGameSet
from game import Game
from common.area_and_date import Area

# 創建測試窗口
def main():
    root = tk.Tk()
    root.title("遊戲測試 - 友好能力階段與行動階段")

    # 1️⃣ 初始化 AI Game Set，同時啟動遊戲與角色管理器
    gameset = AIGameSet()

    game = Game(
        total_days=gameset.total_days,
        total_cycles=gameset.total_cycles,
        character_manager = gameset.character_manager,
        scheduled_events=gameset.scheduled_events,
        area_manager = gameset.area_manager,
        selected_main_rule = gameset.main_rule,
        selected_sub_rules = gameset.sub_rules
    )

    # 2️⃣   啟動 GUI 介面
    game_gui = GameGUI(root, game, game.character_manager.get_pickup_characters())
    game_gui.update_area_widgets()  # ✅ 這行確保地區顯示

    # 3️⃣   初始化偵探行動階段
    action_phase = PlayerDetectiveActionPhase(game, game_gui)
    game_gui.set_phase(action_phase)
    action_phase.execute()


    # 4️⃣ 更新 GUI 並啟動
    game_gui.root.update_idletasks()
    root.mainloop()


if __name__ == "__main__":
    main()
