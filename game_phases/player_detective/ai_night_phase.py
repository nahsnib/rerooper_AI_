
# game_phase/night_phase.py
class NightPhase:
    def __init__(self, character_manager):
        self.character_manager = character_manager

    def execute(self):
        # 執行夜間階段的邏輯
        self.reset_all_abilities()

    def reset_all_abilities(self):
        for character in self.character_manager.characters:
            character.reset_ability_usage()


    def execute(self):
        print("執行夜晚階段...")
        # 實現夜晚階段邏輯
        for character in self.board.characters:
            if character.alive:
                print(f"{character.name} 在夜晚階段進行行動")
                # 在這裡添加更多夜晚階段的邏輯
                # 例如，角色進行秘密行動或事件觸發
