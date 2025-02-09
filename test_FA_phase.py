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
        areas= [Area(3,"都市"), Area(4,"學校"), Area(1,"醫院"), Area(2,"神社")]
    )

    # 🟢 讓所有角色 +2 友好
    for char in game.character_manager.characters:
        char.change_friendship(3)
        char.change_anxiety(2)
        for char in game.character_manager.characters:
            print(f"角色 {char.name} 的友好能力：")
            print(f"  原始數據: {char.friendship_abilities}")  # 🟢 先列出原始內容，確保它的結構
            for ability in char.friendship_abilities:
                if isinstance(ability, FriendshipAbility):
                    print(f"  - {ability.name} (需求友好值: {ability.required_friendship})")
                else:
                    print(f"  - (未知類型) {ability}")

    game_gui = GameGUI(root, game, game.character_manager.characters, None)
    game_gui.update_area_widgets()  # ✅ 這行確保地區顯示

    friendship_phase = PlayerFriendshipAbilityPhase(game, game_gui)
    game_gui.set_phase(friendship_phase)

    friendship_phase.execute()
    root.mainloop()


if __name__ == "__main__":
    main()
