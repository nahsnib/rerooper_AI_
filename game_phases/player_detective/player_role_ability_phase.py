from common.character import CharacterManager  # 引入 CharacterManager

class PlayerRoleAbilityPhase:
    def __init__(self, character_manager, game):
        self.character_manager = character_manager
        self.game = game
        self.active_abilities = self.get_active_abilities()

    def get_active_abilities(self):
        active_abilities = []
        characters = self.character_manager.get_pickup_characters()
        for character in characters:
            if character.pickup:  # 只考慮被選中的角色
                for ability in character.role_abilities:
                    if not character.role_ability_usage.get(ability.name, False):
                        active_abilities.append((character, ability))
        print(f"active_abilities after initialization: {active_abilities}")
        return active_abilities

    def execute_ability(self, character, ability, target=None):
        if (character, ability) in self.active_abilities:
            initial_state = self.get_character_state(character)
            if ability.requires_target and target:
                ability.effect(target)
            else:
                ability.effect(character)
            character.role_ability_usage[ability.name] = True
            self.active_abilities = [item for item in self.active_abilities if item != (character, ability)]
            final_state = self.get_character_state(character)
            message = (f"{character.name} 使用了身分能力：{ability.name} (編號：{ability.id})\n"
                       f"使用前狀態: {initial_state}\n"
                       f"使用後狀態: {final_state}")
            self.check_abilities()
        else:
            message = "該角色的身分能力無法啟用"
        print(message)
        return message

    def get_character_state(self, character):
        return {
            "anxiety": character.anxiety,
            "friendlship": character.friendship,
            "conspiracy": character.conspiracy,
            "location": character.current_location
        }

    def check_abilities(self):
        self.active_abilities = self.get_active_abilities()