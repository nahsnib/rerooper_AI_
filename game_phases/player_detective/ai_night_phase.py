class NightPhase:
    def __init__(self, character_manager, rule_table, game):
        self.character_manager = character_manager
        self.rule_table = rule_table
        self.game = game

    def reset_daily_limited_actions(self):
        # 重置每日限制的行動
        for character in self.character_manager.get_all_characters():
            for action in character.actions:
                if action.is_daily_limited:
                    action.reset()
                    print(f"重置 {character.name} 的每日限制行動：{action.name}")

    def reset_character_states(self):
        # 重置角色的每日狀態
        for character in self.character_manager.get_all_characters():
            character.reset_daily_states()
            print(f"重置 {character.name} 的每日狀態")

    def execute_night_events(self):
        # 執行夜晚階段的特定行動或事件
        night_events = self.rule_table.get_night_events()
        for event in night_events:
            if event['trigger'](self.game):
                event['effect'](self.game)
                print(f"執行夜晚事件：{event['name']}")

    def start(self):
        print("夜晚階段開始")
        self.reset_daily_limited_actions()
        self.reset_character_states()
        self.execute_night_events()
        print("夜晚階段結束")
        self.increment_day()

    def increment_day(self):
        # 增量日期計數器
        self.game.day_counter += 1
        print(f"進入第 {self.game.day_counter} 天")

if __name__ == "__main__":
    # 測試用例
    character_manager = CharacterManager()
    rule_table = RuleTable()
    game = None  # 假設有一個 Game 物件

    night_phase = NightPhase(character_manager, rule_table, game)
    night_phase.start()
