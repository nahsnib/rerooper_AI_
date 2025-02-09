from common.character import Character
from common.area_and_date import TimeManager, Area
from database.RuleTable import RuleTable
from common.player import Player

class Game:
    def __init__(self, total_days, total_cycles, character_manager, scheduled_events, areas):
        self.rule_table = RuleTable()
        self.selected_main_rule = self.rule_table.main_rules
        self.selected_sub_rules = self.rule_table.sub_rules
        self.time_manager = TimeManager(total_days, total_cycles)
        self.scheduled_events = scheduled_events
        self.character_manager = character_manager  # 🔥 儲存 character_manager
        self.areas = [Area(3,"都市"), Area(4,"學校"), Area(1,"醫院"), Area(2,"神社")]  # 命名更清楚
        
        self.EX_gauge = 0  # EX 槽

        self.occurred_events = {}
        self.public_information = []  # 存儲公開資訊（字串格式）
        # 初始化玩家
        self.players = {
            "偵探": Player("偵探", self.get_detective_actions()),
            "劇本家": Player("劇本家", self.get_scriptwriter_actions())
        }

    def get_detective_actions(self):
        """獲取偵探可用的行動"""
        from common.action import detective_actions  # 確保從 action.py 讀取
        return detective_actions

    def get_scriptwriter_actions(self):
        """獲取劇本家可用的行動"""
        from common.action import scriptwriter_actions
        return scriptwriter_actions

    def add_public_info(self, info):
        """新增公開資訊，避免重複"""
        if info not in self.public_information:
            self.public_information.append(info)

    def daily_reset_actions(self):
        """夜晚時，重置所有玩家的每日行動"""
        for player in self.players.values():
            player.daily_reset_actions()

    def cycle_reset_actions(self):
        """輪迴結束時，重置所有玩家的行動"""
        for player in self.players.values():
            player.cycle_reset_actions()
