
from common.area_and_date import TimeManager
from database.RuleTable import RuleTable
from common.player import load_players
from ai.scriptwriter_ai import Scriptwriter_AI

class Game:
    def __init__(self,selected_rule_table, selected_main_rule,selected_sub_rules, 
                character_manager, scheduled_events,time_manager, area_manager,passive_abilities):
        self.selected_rule_table = selected_rule_table
        self.selected_main_rule = selected_main_rule
        self.selected_sub_rules = selected_sub_rules
        self.scriptwriter_win_this_cycle = False

        self.character_manager = character_manager  # 🔥 儲存 character_manager
        self.scheduled_events = scheduled_events
        self.time_manager = time_manager
        self.area_manager = area_manager  # 讓 `areas` 由外部傳入，提高靈活性
        self.passive_abilities = passive_abilities



        self.game_gui = None  # 預設為 None，初始化時再設定
        self.EX_gauge = 0  # EX 槽
        self.happened_events = {}
        self.public_information = []  # 存儲公開資訊（字串格式）

        
        # 初始化玩家，並傳入 `game` 參考
        self.players = load_players()

        # 初始化劇本家AI
        self.scriptwriter_AI = Scriptwriter_AI(self)

    def get_area_by_id(self, area_id):
        return self.area_manager.fetch_area_by_id(area_id)

    def get_area_by_name(self, name):
        return self.area_manager.fetch_area_by_name(name)
        
    def set_gui(self, game_gui):
        """初始化 GUI 介面"""
        self.game_gui = game_gui

    def add_public_info(self, info):
        """新增公開資訊，避免重複"""
        if info not in self.public_information:
            self.public_information.append(info)
            self.game_gui.update_public_information()

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

    def gain_passive_ability(self,char, ability_id):
        # 從全局能力表或某個能力管理系統獲取該能力
        new_ability = RuleTable.get_passive_ability(ability_id)
        
        if new_ability:
            new_ability.owner = char  # 設定擁有者
            self.passive_abilities.append(new_ability)  # 加入角色的被動能力清單
            
         # 確保該能力的 condition 存在於 game.passive_abilities 字典中
        if new_ability.condition in self.passive_abilities:
            self.passive_abilities[new_ability.condition].append(new_ability)
            
    def get_characters_in_area(self, area):
        return [char for char in self.character_manager.characters if char.current_location == area]

    def daily_reset_actions(self):
        """夜晚時，重置所有玩家的每日行動"""
        for player in self.players.values():
            player.daily_reset_actions()

    def cycle_reset_actions(self):
        """輪迴結束時，重置所有玩家的行動"""
        for player in self.players.values():
            player.cycle_reset_actions()
