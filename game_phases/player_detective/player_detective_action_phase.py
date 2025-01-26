import tkinter as tk
from tkinter import ttk, messagebox
import random
from common.action import Action, scriptwriter_actions, detective_actions
from common.character import Character
from common.area_and_date import Area, hospital, shrine, city, school, areas
from common.area_and_date import get_area_by_id, display_all_areas

class PlayerDetectiveActionPhase:
    def __init__(self, character_manager, role, targets, actions):
        self.character_manager = character_manager
        self.role = role
        self.targets = targets
        self.actions = actions
        self.selected_targets = []
        self.scriptwriter_selections = []  # 劇本家的選擇
        self.detective_selections = []  # 偵探的選擇

    def execute(self):
        # 劇本家選擇行動
        self.scriptwriter_choose_targets_and_actions()
        
        # 偵探選擇行動
        # 偵探選擇行動現在由 GUI 控制，這裡不再創建新窗口
        # self.detective_choose_targets_and_actions()

        # 結算所有行動
        self.resolve_actions()

    def scriptwriter_choose_targets_and_actions(self):
        characters = self.character_manager.load_characters()
        if characters is None:
            raise ValueError("Characters could not be loaded.")

        available_targets = [character.name for character in characters] + [area.name for area in areas.values()]
        chosen_targets = random.sample(available_targets, 3)

        for target in chosen_targets:
            action = random.choice(scriptwriter_actions)
            self.scriptwriter_selections.append({"target": target, "action": action})

    def get_scriptwriter_targets(self):
        return [selection["target"] for selection in self.scriptwriter_selections]

    def receive_detective_selection(self, selected_targets):
        self.detective_selections = selected_targets
        if self.check_validity():
            self.execute_actions()
            return True
        return False

    def confirm_selection(self, selected_targets):
        self.selected_targets = selected_targets
        if self.check_validity():
            self.detective_selections = self.selected_targets
            self.execute_actions()
            return True
        return False    
    
    def get_target_by_name(self, name):
        characters = self.character_manager.load_characters()
        if characters is None:
            raise ValueError("Characters could not be loaded.")
        for character in characters:
            if character.name == name:
                return character
        for area in areas.values():
            if area.name == name:
                return area
        return None
        

    def execute_actions(self):
        all_actions = self.scriptwriter_selections + self.detective_selections
        for selection in all_actions:
            target_name = selection["target"]
            action = selection["action"]
            target = self.get_target_by_name(target_name)
            if target and action:
                action.effect(target)
        

    def resolve_actions(self):
        all_actions = self.scriptwriter_selections + self.detective_selections
        forbidden_actions = [13, 14, 15, 9, 10, 18]  # 禁止移動 ABC, 不安禁止, 友好禁止, 禁止陰謀
        forbidden_targets = set()

        for selection in all_actions:
            action = selection["action"]
            if action.id in forbidden_actions:
                forbidden_targets.add(selection["target"])

        for selection in all_actions:
            target_name = selection["target"]
            action = selection["action"]
            if target_name not in forbidden_targets:
                target = self.get_target_by_name(target_name)
                action.effect(target)

    def check_validity(self):
        targets = [item["target"] for item in self.detective_selections]
        actions = [item["action"].name for item in self.detective_selections]
        if len(set(targets)) != len(targets):
            return False
        if actions.count("禁止陰謀") > 1:
            return False
        return True