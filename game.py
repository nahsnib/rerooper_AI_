from game_phases.player_detective.player_detective_action_phase import PlayerDetectiveActionPhase
from game_phases.player_detective.player_detective_ability_phase import PlayerDetectiveAbilityPhase
from game_phases.player_detective.player_event_phase import EventPhase
from game_phases.player_detective.player_night_phase import NightPhase
from game_phases.player_detective.player_cycle_end import CycleEnd  # 引入 AICycleEnd 類
from scriptwriter.ai_gameset import AIGameSet
from common.character import CharacterManager
from common.board import GameBoard, TimeManager

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
    def __init__(self, character_manager, role, total_days, scheduled_events):
        self.character_manager = character_manager
        self.role = role
        self.day_counter = 1  # 初始化日期計數器
        self.remaining_cycles = 5  # 初始化剩餘輪迴數
        self.total_days = total_days
        self.scheduled_events = scheduled_events
        self.action_phase = None
        self.ability_phase = None
        self.event_phase = None
        self.night_phase = None
        self.cycle_end_phase = None
        self.ai_cycle_end = None  # 新增 AICycleEnd 實例
        self.setup_phases()

    def setup_phases(self):
        if self.role == "偵探":
            self.action_phase = PlayerDetectiveActionPhase(self.character_manager)
            self.ability_phase = PlayerDetectiveAbilityPhase(self.character_manager, self)
            self.event_phase = EventPhase(self.character_manager)
            self.night_phase = NightPhase(self.character_manager, self)
            self.cycle_end_phase = CycleEnd(self.character_manager, self)
            self.ai_cycle_end = CycleEnd(self, self.cycle_end_phase.rule_table)  # 初始化 AICycleEnd 實例
        elif self.role == "劇本家":
            # 將來可以在這裡添加 AI 劇本家的相應階段
            pass

    def run(self):
        while True:
            # 每個回合依序啟用各個階段
            self.action_phase.execute()
            self.ability_phase.start()
            self.event_phase.execute()
            self.night_phase.execute()

            # 判斷是否需要進入 cycle_end 階段
            if self.night_phase.is_last_day() or self.scriptwriter_triggered_end_condition():
                self.cycle_end()
            else:
                self.increment_day()

    def cycle_end(self):
        result = self.ai_cycle_end.execute()  # 使用 AICycleEnd 的 execute 方法
        
        if result == "detective_win":
            self.end_game("偵探勝利！")
        elif result == "scriptwriter_win":
            self.start_final_battle()

    def start_final_battle(self):
        self.end_game("進入最後決戰！")
        # 在這裡調用 final_battle.py 的相關邏輯
        # self.final_battle = FinalBattle(self.character_manager)
        # self.final_battle.execute()
        print("遊戲結束，進行最後決戰（未實現）")

    def end_game(self, message):
        print(message)

    def scriptwriter_triggered_end_condition(self):
        # 判斷劇本家是否觸發了某些條件
        return False

    def increment_day(self):
        self.day_counter += 1  # 增量日期計數器
        print(f"進入第 {self.day_counter} 天")

    def decrement_cycles(self):
        self.remaining_cycles -= 1

    def get_scheduled_events(self):
        return self.scheduled_events
