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
        self.areas = areas  # 讓 `areas` 由外部傳入，提高靈活性

        self.EX_gauge = 0  # EX 槽
        self.happened_events = {}
        self.public_information = []  # 存儲公開資訊（字串格式）

        # 初始化玩家，並傳入 `game` 參考
        self.players = {
            "偵探": Player("偵探"),
            "劇本家": Player("劇本家")
        }


        
    def add_public_info(self, info):
        """新增公開資訊，避免重複"""
        if info not in self.public_information:
            self.public_information.append(info)

    def reveal_sub_rule(self):
        """依序揭露副規則，每次揭露一條，最多兩條"""
        if not hasattr(self, "revealed_sub_rules"):
            self.revealed_sub_rules = []  # 初始化已公開規則列表

        sub_rules = self.selected_sub_rules  # 取得副規則列表

        # 確保 `sub_rules` 是 `Rule` 類別的列表
        if not isinstance(sub_rules, list):
            raise TypeError("selected_sub_rules 必須是一個列表")

        rule_names = [rule.name for rule in sub_rules]  # 取得所有副規則的名稱

        # 如果還有未公開的規則，則公開下一條
        if len(self.revealed_sub_rules) < len(rule_names):
            next_rule = rule_names[len(self.revealed_sub_rules)]
            self.revealed_sub_rules.append(next_rule)  # 記錄已公開的規則
            self.add_public_info(f"情報販子揭露了一條副規則：{next_rule}")  # 加入公開訊息


    def daily_reset_actions(self):
        """夜晚時，重置所有玩家的每日行動"""
        for player in self.players.values():
            player.daily_reset_actions()

    def cycle_reset_actions(self):
        """輪迴結束時，重置所有玩家的行動"""
        for player in self.players.values():
            player.cycle_reset_actions()
