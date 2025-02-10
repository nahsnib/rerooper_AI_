class CycleEnd:
    def __init__(self, game, rule_table):
        self.game = game
        self.rule_table = rule_table

    def check_scriptwriter_victory_conditions(self):
        """檢查劇本家是否達成勝利條件"""
        if self.rule_table.check_victory_conditions(self.game):
            return True
        
        for rule in self.rule_table.main_rules + self.rule_table.sub_rules:
            if rule.apply_special_effect(self.game):
                return True
        
        return False

    def display_message(self, message):
        """顯示訊息給玩家"""
        print(message)
        input("點選確定繼續...")

    def prompt_final_battle(self):
        """詢問玩家是否進入最終決戰"""
        response = input("是否要進入最後決戰？（yes/no）: ")
        return response.lower() == 'yes'

    def cycle_reset(self):
        """執行輪迴重置機制"""
        self.game.day = 1
        
        for event in self.game.event_manager.events:
            event.reset()
        
        for character in self.game.character_manager.get_all_characters():
            character.cycle_reset()
        
        for area in self.game.area_manager.areas:
            area.cycle_reset()
        
        self.game.rule_table.reset_limited_abilities()
        
        self.display_message("輪迴已重置，遊戲回到初始狀態。")

    def execute(self):
        """執行 CycleEnd 階段"""
        # 檢查關鍵人物是否死亡
        for character in self.game.character_manager.get_all_characters():
            if character.name == "關鍵人物" and not character.alive:
                character.use_ability("犧牲的代價", self.game)

        # 劇本家勝利檢查
        if self.check_scriptwriter_victory_conditions():
            self.display_message("劇本家的勝利！")
            return "scriptwriter_win"
        
        # 檢查剩餘輪迴數
        if self.game.get_remaining_cycles() == 0:
            self.display_message("進入最終決戰！")
            return "final_battle"
        
        # 詢問偵探玩家是否提前進入最終決戰
        if self.prompt_final_battle():
            self.display_message("進入最終決戰！")
            return "final_battle"
        
        # 減少輪迴數並執行輪迴重置
        self.game.decrement_cycles()
        self.cycle_reset()
        
        return "cycle_reset"
