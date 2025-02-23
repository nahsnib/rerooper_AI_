from scriptwriter.ai_gameset import AIGameSet
from game import Game
from common.area_and_date import Area   

def test_ai_gameset():
    """ 測試 AIGameSet 並用它初始化 Game 物件 """
    
    # 1️⃣ 產生遊戲設定
    gameset = AIGameSet()
    
    # 2️⃣ 使用 AIGameSet 的數據建立 Game 物件
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
    
    # 3️⃣ 測試 Game 物件是否成功建立
    print("✅ 成功建立 Game 物件！")
    
    # 4️⃣ 輸出 Game 的基本資訊
    print("\n🔹 遊戲基本資訊")
    print(f"總天數: {game.time_manager.total_days}")
    print(f"總輪迴數: {game.time_manager.remaining_cycles}")
    print(f"已安排事件: {game.scheduled_events}")
    print(f"角色數量: {len(game.character_manager.characters)}")

    # 5️⃣ 測試 `AIGameSet` 的輸出是否符合 `Game` 設定

if __name__ == "__main__":
    test_ai_gameset()
