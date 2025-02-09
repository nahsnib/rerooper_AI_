from scriptwriter.ai_gameset import AIGameSet
from game import Game

def test_ai_gameset():
    """ 測試 AIGameSet 並用它初始化 Game 物件 """
    
    # 1️⃣ 產生遊戲設定
    gameset = AIGameSet()
    
    # 2️⃣ 使用 AIGameSet 的數據建立 Game 物件
    game = Game(
        total_days=gameset.total_days,
        total_cycles=gameset.total_cycles,
        characters=gameset.characters,
        scheduled_events=gameset.scheduled_events,
        areas=gameset.character_db  # 這部分要確保是地區資訊
    )
    
    # 3️⃣ 測試 Game 物件是否成功建立
    print("✅ 成功建立 Game 物件！")
    
    # 4️⃣ 輸出 Game 的基本資訊
    print("\n🔹 遊戲基本資訊")
    print(f"總天數: {game.time_manager.total_days}")
    print(f"總輪迴數: {game.time_manager.remaining_cycles}")
    print(f"已安排事件: {game.scheduled_events}")
    print(f"角色數量: {len(game.characters)}")

    # 5️⃣ 測試 `AIGameSet` 的輸出是否符合 `Game` 設定
    public_info = gameset.get_public_info()
    secret_info = gameset.get_secret_info()

    print("\n🔹 AIGameSet 公開資訊")
    for key, value in public_info.items():
        print(f"{key}: {value}")

    print("\n🔹 AIGameSet 秘密資訊")
    for key, value in secret_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_ai_gameset()
