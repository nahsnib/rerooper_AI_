import tkinter as tk
from game_gui import GameGUI
from game import Game
from common.area_and_date import Area
from scriptwriter.ai_gameset import AIGameSet
from game_phases.player_detective.player_friendship_ability_phase import PlayerFriendshipAbilityPhase
from database.Basecharacter import FriendshipAbility

def main():
    root = tk.Tk()
    root.title("測試友好能力階段")

    gameset = AIGameSet()
    game = Game(
        total_days=gameset.total_days,
        total_cycles=gameset.total_cycles,
        character_manager = gameset.character_manager,
        scheduled_events=gameset.scheduled_events,
        area_manager = gameset.area_manager,
        selected_main_rule = gameset.main_rule,
        selected_sub_rules = gameset.sub_rules,
    )
    

    # 🟢 讓所有角色 +N 友好
    for char in game.character_manager.characters:
        char.change_friendship(5)
        char.change_anxiety(2)


    game_gui = GameGUI(root, game, game.character_manager.characters, None)
    game.game_gui = game_gui  # ✅ 這行確保 Game 類別能夠存取 GUI
    game_gui.update_area_widgets()  # ✅ 這行確保地區顯示

    friendship_phase = PlayerFriendshipAbilityPhase(game, game_gui)
    game_gui.set_phase(friendship_phase)

    friendship_phase.execute()
    root.mainloop()


if __name__ == "__main__":
    main()
