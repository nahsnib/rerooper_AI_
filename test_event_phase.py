from database.RuleTable import RuleTable
from common.character import CharacterManager
from scriptwriter.ai_gameset import AIGameSet
from game_phases.player_detective.player_event_phase import EventPhase  # 確保這個檔案已經有 EventPhase 類別
from common.area_and_date import Area
from game import Game

# 初始化遊戲

rule_table = RuleTable()
game_set = AIGameSet()
game = Game(
    total_days=game_set.total_days,
    total_cycles=game_set.total_cycles,
    character_manager = game_set.character_manager,
    scheduled_events=game_set.scheduled_events,
    areas= [Area(3,"都市"), Area(4,"學校"), Area(1,"醫院"), Area(2,"神社")]
)
# 讓所有角色 +100 不安值
for character in game.character_manager.get_pickup_characters():
    character.change_anxiety(100)

# 建立事件階段物件
event_phase = EventPhase(game.character_manager, rule_table, game_set, game)

# 模擬從第一天到最終日的事件觸發
start_day = game.time_manager.current_day
end_day = game.time_manager.total_days  # 假設這是輪迴的最終日

for day in range(start_day, end_day + 1):
    print(f"\n=== 第 {day} 天 ===")
    game.time_manager.current_day = day  # 模擬時間推進
    event_phase.main()  # 執行事件階段
