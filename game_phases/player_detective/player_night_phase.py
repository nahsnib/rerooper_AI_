from common.character import CharacterManager
from common.character import Character
from database.RuleTable import RuleTable

class NightPhase:
    def __init__(self, game):
        self.game = game
        self.character_manager = game.character_manager
        self.rule_table = game.rule_table

    def reset_daily_limited_actions(self):
        for character in self.character_manager.get_all_characters():
            character.daily_reset_actions()
            print(f"{character.name} 的每日行動已重置")

    def reset_ability_usage(self):
        for character in self.character_manager.get_all_characters():
            for ability in character.friendship_abilities:
                ability.usage_reset()
            for identity_ability in character.identity_abilities:
                identity_ability.usage_reset()
            print(f"{character.name} 的能力使用次數已重置")

    def reset_character_states(self):
        for character in self.character_manager.get_all_characters():
            character.reset_daily_states()
            print(f"{character.name} 的每日狀態已重置")

    def trigger_passive_abilities(self):
        for character in self.character_manager.get_all_characters():
            for ability in character.passive_abilities:
                if ability.trigger == 'night_phase':
                    ability.effect(character, self.game)
                    print(f"觸發 {character.name} 的被動能力：{ability.name}")


    def start(self):
        print("夜晚階段開始")
        self.game.check_passive_ability("night_phase")
        self.reset_daily_limited_actions()
        self.reset_ability_usage()
        self.reset_character_states()
        self.trigger_passive_abilities()
        print("夜晚階段結束")

    def on_start(self):
        print("夜晚階段開始")
    
    def on_end(self):
        print("夜晚階段結束，清除暫存數據")
        # 這裡可以清除行動記錄、計算效果等

if __name__ == "__main__":
    game = None  # 這裡應該傳入實際的 Game 物件
    night_phase = NightPhase(game)
    night_phase.start()
