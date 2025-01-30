import tkinter as tk
from tkinter import ttk, messagebox
from common.character import CharacterManager, friendship_ignore  # 引入 CharacterManager 和 friendship_ignore 函數

def check_friendship_ignore(character):
    """
    檢查角色的友好能力是否會被無效或無視。
    
    參數:
        character: 需要檢查的角色對象。
        
    返回:
        (bool, str): (是否無效或無視, 原因描述)
    """
    ignore, reason = friendship_ignore(character)
    return not ignore, reason

class PlayerDetectiveAbilityPhase:
    def __init__(self, character_manager, game, scriptwriter):
        self.character_manager = character_manager
        self.game = game
        self.scriptwriter = scriptwriter
        self.active_abilities = []

    def check_abilities(self):
        # 檢查哪些角色的能力可以啟用
        self.active_abilities = []
        for character in self.character_manager.characters:
            for ability in character.friendly_abilities:
                if self.can_use_ability(character, ability):
                    self.active_abilities.append((character, ability))

    def can_use_ability(self, character, ability):
        # 判斷角色的能力是否可以啟用
        if not character.alive:
            return False  # 角色必須是存活的

        if ability.get('active', False) and ability['trigger'](character) and not character.friendly_ability_usage[ability['name']]:
            if ability.get('limit_use', False) and character.friendly_ability_usage[ability['name']] == 'used':
                return False  # 能力已在此輪迴中使用過
            
            if ability.get('target_required', False):
                for target in self.character_manager.characters:
                    if target.alive or ability['name'] == '復活同地區的一具屍體':
                        if 'target_condition' in ability and ability['target_condition'](target, character):
                            return True
            else:
                return True
        return False
    
    def use_classleader_ability(self, character, ability, target):
        # 處理特殊能力的使用邏輯
        if ability['name'] == '友好2：偵探回收1張【1輪迴只能使用1次】的行動卡（1輪迴限用1次）':
            if ability['trigger'](character) and not character.friendly_ability_usage[ability['name']]:
                if target and target.alive:
                    self.game.detective_recover_action_card()
                    character.friendly_ability_usage[ability['name']] = 'used'
                    return True
        return False

    def detective_recover_action_card(self):
        # 偵探回收一張限用行動卡的邏輯
        for action_card in self.game.action_cards:
            if action_card['limit_use'] and action_card['used']:
                action_card['used'] = False
                return action_card['name']
        return None
    
    def execute_ability(self, character, ability, target=None):
        # 執行角色的能力
        if (character, ability) in self.active_abilities:
            if ability.get('target_required', False) and target:
                ability['effect'](target)
                character.friendly_ability_usage[ability['name']] = True
                message = f"{character.name} 使用了能力：{ability['name']} 對 {target.name}"
            else:
                ability['effect'](self.game)
                character.friendly_ability_usage[ability['name']] = True
                message = f"{character.name} 使用了能力：{ability['name']}"
            self.check_abilities()
        else:
            message = "該角色的能力無法啟用"
        return message

    def get_character_by_name(self, name):
        for character in self.character_manager.characters:
            if character.name == name:
                return character
        return None

    def check_friendship_ignore(self, character):
        # 使用通用函數來檢查友好能力是否會被無效或無視
        return check_friendship_ignore(character)