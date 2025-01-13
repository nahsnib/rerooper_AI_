class AICycleEnd:
    def __init__(self, game, rule_table):
        self.game = game
        self.rule_table = rule_table

    def check_scriptwriter_victory_conditions(self):
        # 檢查劇本家的勝利條件是否達成
        if self.rule_table.check_victory_conditions(self.game):
            return True

        # 檢查特殊效果
        for rule in self.rule_table.main_rules + self.rule_table.sub_rules:
            if rule.special_effect and rule.special_effect(self.game):
                return True

        return False

    def display_message(self, message):
        # 顯示訊息給玩家
        print(message)
        input("點選確定繼續...")

    def prompt_final_battle(self):
        # 提示玩家是否進入最終決戰
        response = input("是否要進入最後決戰？（yes/no）: ")
        return response.lower() == 'yes'

    def reset_game_board(self):
        # 重置遊戲版面
        self.game.reset_to_gameset()

    def execute(self):
        if self.check_scriptwriter_victory_conditions():
            self.display_message("劇本家的勝利！")
            if self.game.get_remaining_cycles() == 0:
                self.display_message("結束輪迴，進入最終決戰")
                return
            else:
                if self.prompt_final_battle():
                    self.display_message("結束輪迴，進入最終決戰")
                    return
                else:
                    self.game.decrement_cycles()
                    self.reset_game_board()
                    self.display_message("輪迴數減少，重置遊戲版面")
        else:
            self.display_message("玩家以偵探身分取得遊戲勝利！")
            self.game.restart()
