# game.py

class Player:
    def __init__(self, role):
        self.role = role

    def perform_role_action(self):
        if self.role == "偵探":
            self.detective_action()
        elif self.role == "劇本家":
            self.scriptwriter_action()

    def detective_action(self):
        print("偵探行動：調查案件")

    def scriptwriter_action(self):
        print("劇本家行動：設置情節")


class GameLoop:
    def __init__(self, character_manager):
        self.character_manager = character_manager
        self.action_phase = ActionPhase(self.character_manager)
        self.ability_phase_1 = AbilityPhase1(self.character_manager)
        self.ability_phase_2 = AbilityPhase2(self.character_manager)
        self.event_phase = EventPhase(self.character_manager)
        self.night_phase = NightPhase(self.character_manager)
        self.cycle_end_phase = CycleEnd(self.character_manager)

    def run(self):
        # 每個回合依序啟用各個階段
        self.action_phase.execute()
        self.ability_phase_1.execute()
        self.ability_phase_2.execute()
        self.event_phase.execute()
        self.night_phase.execute()

        # 判斷是否需要進入cycle_end階段
        if self.night_phase.is_last_day() or self.scriptwriter_triggered_end_condition():
            self.cycle_end()

    def cycle_end(self):
        result = self.cycle_end_phase.execute()
        
        if result == "detective_win":
            self.end_game("偵探勝利！")
        elif result == "scriptwriter_win":
            if self.cycle_end_phase.remaining_cycles() == 0:
                self.start_final_battle()
            else:
                self.ask_detective_for_final_battle()

    def start_final_battle(self):
        self.end_game("進入最後決戰！")
        # 在這裡調用final_battle.py的相關邏輯
        # self.final_battle = FinalBattle(self.character_manager)
        # self.final_battle.execute()
        print("遊戲結束，進行最後決戰（未實現）")

    def ask_detective_for_final_battle(self):
        response = messagebox.askyesno("最後決戰", "劇本家觸發了勝利條件，你要進入最後決戰嗎？")
        if response:
            self.start_final_battle()
        else:
            self.cycle_end_phase.decrement_cycles()
            print("輪迴數減少，繼續遊戲")
            self.run()

    def end_game(self, message):
        print(message)

    def scriptwriter_triggered_end_condition(self):
        # 判斷劇本家是否觸發了某些條件
        return False
