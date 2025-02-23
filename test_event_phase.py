
from scriptwriter.ai_gameset import AIGameSet
from game_phases.player_detective.player_event_phase import EventPhase  # 確保這個檔案已經有 EventPhase 類別
from common.area_and_date import Area
from game import Game

# 初始化遊戲

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
print(game.scheduled_events)
# 讓所有角色 +2 不安值&+2陰謀
for character in game.character_manager.characters:
    character.change_anxiety(6)
    character.change_conspiracy(2)

for area in game.area_manager.areas:
    area.change_conspiracy(1)

# 建立事件階段物件
event_phase = EventPhase(game)

# 模擬從第一天到最終日的事件觸發
start_day = game.time_manager.current_day
end_day = game.time_manager.total_days  # 假設這是輪迴的最終日

for day in range(start_day, end_day + 1):
    print(f"\n=== 第 {day} 天 ===")
    game.time_manager.current_day = day  # 模擬時間推進
    event_phase.main()  # 執行事件階段
