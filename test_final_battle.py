import tkinter as tk
from game import Game
from scriptwriter.ai_gameset import AIGameSet
from game_phases.player_detective.player_final_battle import FinalBattle

def main():

    # 1️⃣ 產生遊戲設定
    gameset = AIGameSet()
    
    # 2️⃣ 使用 AIGameSet 的數據建立 Game 物件
    game = Game(
        selected_rule_table=gameset.selected_rule_table,  # 選規則表
        selected_main_rule=gameset.selected_main_rule,    # 選主規則
        selected_sub_rules=gameset.selected_sub_rules,    # 選副規則
        character_manager=gameset.character_manager,      # 人
        scheduled_events=gameset.scheduled_events,        # 事件
        time_manager=gameset.time_manager,                # 時間
        area_manager=gameset.area_manager,                # 地區
        passive_abilities=gameset.passive_abilities       # 物件導向的被動能力列表
    )

    # 3️⃣ 啟動 Final Battle GUI
    FinalBattle(game)

if __name__ == "__main__":
    main()
