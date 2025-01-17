class AICycleEnd:
    def __init__(self, game, rule_table):
        self.game = game
        self.rule_table = rule_table

    def check_scriptwriter_victory_conditions(self):
        # 檢查劇本家的勝利條件是否達成
        if self.rule_table.check_victory_conditions(self.game):
            return True

        # 檢查主規則和副規則的特殊效果
        for rule in self.rule_table.main_rules + self.rule_table.sub_rules:
            if rule.apply_special_effect(self.game):
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
        # 檢查所有角色的死亡狀況
        for character in self.game.character_manager.get_all_characters():
            if character.name == "關鍵人物" and not character.alive:
                # 如果關鍵人物死亡，觸發其能力
                character.use_ability("犧牲的代價", self.game)
        
        if self.check_scriptwriter_victory_conditions():
            self.display_message("劇本家的勝利！")
            if self.game.get_remaining_cycles() == 0:
                self.display_message("結束輪迴，進入最終決戰")
                return "scriptwriter_win"
            else:
                if self.prompt_final_battle():
                    self.display_message("結束輪迴，進入最終決戰")
                    return "scriptwriter_win"
                else:
                    self.game.decrement_cycles()
                    self.reset_game_board()
                    self.display_message("輪迴數減少，重置遊戲版面")
        else:
            self.display_message("玩家以偵探身分取得遊戲勝利！")
            self.game.restart()
            return "detective_win"
