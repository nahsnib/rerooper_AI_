import tkinter as tk
from game import Game
from scriptwriter.ai_gameset import AIGameSet
from game_phases.player_detective.player_final_battle import FinalBattle

def main():

    # 1️⃣ 產生遊戲設定
    pre_game = Game()
    gameset = AIGameSet(pre_game)
    game = gameset.pre_game
    # 3️⃣ 啟動 Final Battle GUI
    final_battle = FinalBattle(game)
    final_battle.execute()

if __name__ == "__main__":
    main()
