class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player("劇本家"), Player("偵探")]
        self.current_player_index = 0
        self.rounds = 0
        self.days_per_round = 0
        self.events = []
        self.rules = []

    def start(self):
        self.construct_scenario()
        while not self.is_over():
            self.play_round()
            if self.check_victory():
                break

    def construct_scenario(self):
        # 劇本構築邏輯
        pass

    def play_round(self):
        for day in range(self.days_per_round):
            self.play_day()
            if self.is_final_day(day):
                break

    def play_day(self):
        print("日出，一天的開始")
        self.board.display()
        
        # 劇本家行動選擇
        scriptwriter_actions = self.players[0].choose_actions(self.board)

        # 偵探行動選擇
        detective_actions = self.players[1].choose_actions(self.board)

        # 行動結算
        self.board.resolve_actions(scriptwriter_actions, detective_actions)
        
        # 偵探能力階段
        self.players[1].use_abilities(self.board)

        # 劇本家能力階段
        self.players[0].use_abilities(self.board)

        # 事件階段
        self.board.trigger_events(self.events)

        print("夜晚階段，一天結束")

    def is_final_day(self, day):
        # 檢查是否為最終日
        return day == self.days_per_round - 1

    def check_victory(self):
        # 檢查勝利條件
        return False

    def is_over(self):
        # 檢查遊戲是否結束
        return False
