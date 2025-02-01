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

class PlayerFriendshipAbilityPhase:
    def __init__(self, character_manager, game, scriptwriter):
        self.character_manager = character_manager
        self.game = game
        self.scriptwriter = scriptwriter
        self.active_abilities = self.get_active_abilities()

    def get_active_abilities(self):
        active_abilities = []
        characters = self.character_manager.get_pickup_characters()  # 從 character_manager 取得角色列表
        for character in characters:
            for ability in character.friendly_abilities:
                if ability['trigger'](character) and not character.friendly_ability_usage.get(ability['name'], False):
                    active_abilities.append((character, ability))
        print(f"active_abilities after initialization: {active_abilities}")  # 添加打印語句
        return active_abilities

    def execute_ability(self, character, ability, target=None):
        # 執行角色的能力
        print(f"active_abilities: {self.active_abilities}")  # 添加打印語句
        if (character, ability) in self.active_abilities:
            if ability.get('target_required', False) and target:
                ability['effect'](target)
            else:
                ability['effect'](character)  # 確保增加陰謀值的是正在執行能力的角色
            character.friendly_ability_usage[ability['name']] = True
            self.active_abilities = [item for item in self.active_abilities if item != (character, ability)]  # 移除已使用的能力
            message = f"{character.name} 使用了能力：{ability['name']}"
            self.check_abilities()
        else:
            message = "該角色的能力無法啟用"
        return message

    def check_abilities(self):
        # 更新 active_abilities 列表
        self.active_abilities = self.get_active_abilities()

    def get_character_by_name(self, name):
        characters = self.character_manager.get_pickup_characters()  # 從 character_manager 取得角色列表
        for character in characters:
            if character.name == name:
                return character
        return None

    def check_friendship_ignore(self, character):
        # 使用通用函數來檢查友好能力是否會被無效或無視
        return check_friendship_ignore(character)