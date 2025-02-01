import random
from common.action import scriptwriter_actions, detective_actions
from common.character import Character
from common.area_and_date import areas

class PlayerDetectiveActionPhase:
    def __init__(self, character_manager):
        self.character_manager = character_manager
        self.scriptwriter_selections = []
        self.detective_selections = []

    def AI_Action(self):
        characters = self.character_manager.get_pickup_characters()
        if characters is None:
            raise ValueError("Characters could not be loaded.")

        available_targets = [character.name for character in characters] + [area.name for area in areas.values()]
        chosen_targets = random.sample(available_targets, 3)

        self.scriptwriter_selections.clear()
        for target in chosen_targets:
            action = random.choice(scriptwriter_actions)
            self.scriptwriter_selections.append({"target": target, "action": action})

    def get_scriptwriter_targets(self):
        return [selection["target"] for selection in self.scriptwriter_selections]

    def Player_Action(self, selections):
        if len(selections) != 3:
            raise ValueError("Exactly three selections are required.")
        self.detective_selections = selections

    def check_validity(self):
        all_selections = self.scriptwriter_selections + self.detective_selections
        targets = [selection["target"] for selection in all_selections]
        actions = [selection["action"].name for selection in all_selections]

        if len(set(targets)) != len(targets):
            return False

        if actions.count("禁止陰謀") > 1:
            return False

        return True

    def execute_actions(self):
        all_selections = self.scriptwriter_selections + self.detective_selections
        for selection in all_selections:
            target_name = selection["target"]
            action = selection["action"]
            target = self.get_target_by_name(target_name)
            if target and action:
                action.effect(target)  # 確保行動效果應用到目標
        print("行動執行完畢")

    def get_target_by_name(self, name):
        characters = self.character_manager.get_pickup_characters()
        if characters is None:
            raise ValueError("Characters could not be loaded.")
        for character in characters:
            if character.name == name and character.pickup:
                return character
        for area in areas.values():
            if area.name == name:
                return area
        return None

    def end_phase(self):
        self.scriptwriter_selections.clear()
        self.detective_selections.clear()