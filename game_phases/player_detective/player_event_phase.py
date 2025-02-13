import random

from database.RuleTable import RuleTable
from common.character import CharacterManager
from scriptwriter.ai_gameset import AIGameSet
class EventPhase:
    def __init__(self, character_manager, rule_table, game_set, game):
        self.character_manager = character_manager
        self.rule_table = rule_table
        self.game_set = game_set
        self.game = game

    def main(self):
        today = self.game.time_manager.current_day
        events_today = [event for event in self.game.scheduled_events.values() if event.date == today]
        
        if not events_today:
            return self.end_phase()
        
        for event in events_today:
            for char in self.character_manager.characters:
                print(f"🧐 現有角色: '{char.name}' (類型: {type(char.name)})")

            criminal = self.character_manager.get_character_by_name(event.criminal_name)
            print(f"📌 事件 '{event.name}' 犯人名稱: '{event.criminal_name}' (類型: {type(event.criminal_name)})")
            print(f"🧐 找到角色: {criminal.name if criminal else '未找到'}")

            if not criminal:
                print(f"🚨 錯誤: 找不到事件 '{event.name}' 的犯人 '{event.criminal_name}'！")
                continue
            
            if not criminal.alive:
                print(f"📢 事件 '{event.name}' 未發生: 犯人 '{criminal.name}' 已死亡。")
                continue
            
            if criminal.anxiety < criminal.anxiety_threshold and criminal.guilty != 1:
                print(f"📢 事件 '{event.name}' 未發生: '{criminal.name}' 的不安 ({criminal.anxiety}) 低於臨界 ({criminal.anxiety_threshold})。")
                continue

            if criminal.guilty == -1:
                print(f"📢 事件 '{event.name}' 未發生: '{criminal.name}' 被效果排除犯案。")
                continue
            
            print(f"🔥 觸發事件: {event.name} | 犯人: {criminal.name}")
            event.effect(self.game)
            event.happened = True
        
        self.end_phase()
        

    def check_today_event(self):
        # 檢查今天是否有事件
        today = self.game.time_manager.current_day
        return self.game_set.scheduled_events.get(today, None)


    def is_event_triggered(self, criminal):
        # 判斷事件是否觸發
        if criminal and criminal.alive and criminal.anxiety >= criminal.anxiety_threshold:
            return True
        return False

    def execute_event(self, event, criminal):
        # 執行事件
        event.happened = True
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

    def end_phase(self):
        print("事件階段結束")
        input("點選確定繼續...")

if __name__ == "__main__":
    # 測試用例
    character_manager = CharacterManager()
    rule_table = RuleTable()
    game_set = AIGameSet()
    game = None  # 假設有一個 Game 物件

    ai_phase = EventPhase(character_manager, rule_table, game_set, game)
    ai_phase.start()
