import tkinter as tk
from game_gui import GameGUI
from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from scriptwriter.ai_gameset import AIGameSet
from game import Game

# 創建測試窗口
def main():
    root = tk.Tk()
    root.title("遊戲測試 - 友好能力階段與行動階段")

    # 1️⃣ 初始化 AI Game Set，同時啟動遊戲與角色管理器
    gameset = AIGameSet()

    game = Game(
        selected_rule_table = gameset.selected_rule_table,  # 選規則表
        selected_main_rule = gameset.selected_main_rule,    # 選主規則
        selected_sub_rules = gameset.selected_sub_rules,    # 選副規則

        character_manager = gameset.character_manager,      # 人
        scheduled_events = gameset.scheduled_events,        # 事件
        time_manager = gameset.time_manager,                # 時間
        area_manager = gameset.area_manager,                # 地區
        passive_abilities = gameset.passive_abilities       # 物件導向的被動能力列表
    )

    game_gui = GameGUI(root, game, None)
    game.game_gui = game_gui  # ✅ 這行確保 Game 類別能夠存取 GUI
    game_gui.update_area_widgets()  # ✅ 這行確保地區顯示

    phase = PlayerDetectiveActionPhase(game, game_gui)
    game_gui.set_phase(phase)
    phase.execute()


    # 4️⃣ 更新 GUI 並啟動
    game_gui.root.update_idletasks()
    root.mainloop()


if __name__ == "__main__":
    main()
