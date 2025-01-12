import random

from database.RuleTable import RuleTable
from common.character import CharacterManager
from gameset import GameSet

class AiEventPhase:
    def __init__(self, character_manager, rule_table, game_set, game):
        self.character_manager = character_manager
        self.rule_table = rule_table
        self.game_set = game_set
        self.game = game

    def start(self):
        today_event = self.check_today_event()
        if not today_event:
            self.show_message("今日無事件")
            return
        
        criminal = self.get_event_criminal(today_event)
        if not self.is_event_triggered(criminal):
            self.show_message("未達事件發生條件，事件不發生")
            return
        
        self.execute_event(today_event, criminal)

    def check_today_event(self):
        # 檢查今天是否有事件
        return self.game_set.get_today_event()

    def get_event_criminal(self, event):
        # 獲取事件犯人
        return self.character_manager.get_character_by_name(event['criminal'])

    def is_event_triggered(self, criminal):
        # 判斷事件是否觸發
        if criminal and criminal.alive and criminal.anxiety >= criminal.anxiety_threshold:
            return True
        return False

    def execute_event(self, event, criminal):
        # 執行事件
        if not event.get('target_required', False):
            self.apply_event_effects(event)
            self.show_message(f"事件 {event['name']} 發生")
        else:
            valid_targets = [target for target in self.character_manager.get_all_characters() if event['target_condition'](target, criminal)]
            if valid_targets:
                target = self.choose_target(valid_targets)
                self.apply_event_effects(event, target)
                self.show_message(f"事件 {event['name']} 發生，目標: {target.name}")
            else:
                self.show_message(f"事件 {event['name']} 發生，但無有效目標")

    def apply_event_effects(self, event, target=None):
        # 應用事件效果
        effects = self.rule_table.get_event_effects(event['name'])
        for effect in effects:
            if target:
                effect(target)
            else:
                effect(self.game)

    def choose_target(self, valid_targets):
        # AI 選擇一個合理的目標
        return random.choice(valid_targets)

    def show_message(self, message):
        # 顯示訊息給偵探方
        print(message)
        input("點選確定繼續...")

if __name__ == "__main__":
    # 測試用例
    character_manager = CharacterManager()
    rule_table = RuleTable()
    game_set = GameSet()
    game = None  # 假設有一個 Game 物件

    ai_phase = AiEventPhase(character_manager, rule_table, game_set, game)
    ai_phase.start()
