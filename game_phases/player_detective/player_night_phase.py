from common.character import CharacterManager
from common.character import Character
from database.RuleTable import RuleTable

class NightPhase:
    def __init__(self, game):
        self.game = game
        self.phase_type = "night"
        self.character_manager = game.character_manager
        self.selected_rule_table = game.selected_rule_table

    def reset_RAFA(self):
        for character in self.character_manager.get_pickup_characters():
            character.daily_reset()
            print(f"{character.name} 的每日行動已重置")

    def reset_players_actions(self):
        self.game.players['偵探'].daily_reset_actions
        self.game.players['劇本家'].daily_reset_actions




    def execute(self):
        print("夜晚階段開始")
        self.game.check_passive_ability("night_phase")
        self.reset_RAFA()
        self.reset_players_actions()
        self.on_end()
        print("夜晚階段結束")

    def on_start(self):
        print("夜晚階段開始")
    
    def on_end(self):
        print("夜晚階段結束，清除暫存數據")
        # 這裡可以清除行動記錄、計算效果等
        self.game.phase_manager.advance_phase()

