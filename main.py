# main.py
import tkinter as tk
from tkinter import messagebox
from game import GameLoop
from common.character import CharacterManager
from scriptwriter.ai_gameset import AIGameSet

def start_game(role, gameset):
    character_manager = CharacterManager()

    # 獲取公開信息
    public_info = gameset.get_public_info()
    total_days = public_info["total_days"]
    total_cycles = public_info["total_cycles"]
    scheduled_events = public_info["scheduled_events"]

    game = GameLoop(character_manager, role, total_days, total_cycles, scheduled_events)
    game.run()  # 假設在 game.py 中有 run 方法來啟動遊戲循環

if __name__ == "__main__":
    # 創建一個隱藏的根窗口，用於顯示提示訊息和簡單對話框
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口

    # 提供選擇方式：提示視窗
    response = messagebox.askquestion("選擇角色", "你想擔任偵探還是劇本家？\n選擇 '是' 表示偵探，選擇 '否' 表示劇本家")
    if response == 'yes':
        role = "偵探"
    else:
        role = "劇本家"

    # 顯示提示訊息
    messagebox.showinfo("提示", "測試版僅提供玩家扮演偵探")

    # 初始化 AIGameSet
    character_manager = CharacterManager()
    gameset = AIGameSet(character_manager)

    # 呼叫 start_game，強制使用 "偵探" 作為角色
    start_game("偵探", gameset)

    # 主窗口銷毀
    root.destroy()