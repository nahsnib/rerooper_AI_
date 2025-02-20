import random

from database.RuleTable import RuleTable
from common.character import CharacterManager
from scriptwriter.ai_gameset import AIGameSet

class EventPhase:
    def __init__(self, game):
        self.game = game

    def main(self):
        today = self.game.time_manager.current_day
        events_today = [event for event in self.game.scheduled_events.values() if event.date == today]
        
        if not events_today:
            return self.end_phase()
        
        for event in events_today:
            criminal = self.game.character_manager.get_character_by_name(event.criminal_name)
            
            if not criminal or not criminal.alive:
                continue
            
            if criminal.anxiety < criminal.anxiety_threshold and criminal.guilty != 1:
                continue
            
            if criminal.guilty == -1:
                continue
            
            print(f"🔥 觸發事件: {event.name} | 犯人: {criminal.name}")
            self.execute_event(event, criminal)
        
        self.end_phase()
        
    def execute_event(self, event, criminal):
        event.happened = True
        
        if not event.victim_required:
            event.effect(self.game, criminal, [])
            self.show_message(f"事件 {event.name} 發生")
            return
        
        valid_targets = [victim for victim in self.game.character_manager.get_pickup_characters() if event.victim_condition(self.game,criminal, victim)]
        if event.id == 106: #失蹤事件改以地區為受害者
            valid_targets = [self.game.area_manager.fetch_area_by_name("醫院"), 
                             self.game.area_manager.fetch_area_by_name("神社"), 
                             self.game.area_manager.fetch_area_by_name("都市"),
                              self.game.area_manager.fetch_area_by_name("學校")]
        if event.victim_count is None:
            victims = valid_targets  # 所有符合條件的角色
        else:
            if len(valid_targets) < event.victim_count:
                self.show_message(f"事件 {event.name} 發生，但有效目標不足 {event.victim_count} 人")
                return
            victims = self.game.scriptwriter_AI.choose_victims(event, valid_targets, event.victim_count)
        
        if event.victim_count == 1 and victims:  # 只選取第一個受害者
            event.effect(self.game, criminal, victims[0])
        else:
            event.effect(self.game, criminal, victims)
        self.show_message(f"事件 {event.name} 發生，目標: {', '.join([v.name for v in victims])}")
        
    def show_message(self, message):
        print(message)
        input("點選確定繼續...")

    def end_phase(self):
        print("事件階段結束")
        input("點選確定繼續...")
