from common.character import CharacterManager # 引入 CharacterManager 



class PlayerRoleAbilityPhase:
    def __init__(self, character_manager, game, scriptwriter):
        self.character_manager = character_manager
        self.game = game
        self.scriptwriter = scriptwriter
        self.active_abilities = self.get_active_abilities()

    def get_active_abilities(self):
        active_abilities = []
        characters = self.character_manager.get_characters()
        for character in characters:
            if character.pickup:  # 只考慮被選中的角色
                for ability in character.friendly_abilities:
                    if ability['trigger'](character) and not character.friendly_ability_usage.get(ability['name'], False):
                        active_abilities.append((character, ability))
        print(f"active_abilities after initialization: {active_abilities}")
        return active_abilities

    def execute_ability(self, character, ability, target=None):
        if (character, ability) in self.active_abilities:
            if ability.get('target_required', False) and target:
                ability['effect'](target)
            else:
                ability['effect'](character)
            character.identity_ability_usage[ability['name']] = True
            self.active_abilities = [item for item in self.active_abilities if item != (character, ability)]
            message = f"{character.name} 使用了身分能力：{ability['name']}"
            self.check_abilities()
        else:
            message = "該角色的身分能力無法啟用"
        return message

    def check_abilities(self):
        self.active_abilities = self.get_active_abilities()