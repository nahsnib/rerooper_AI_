import random

class PlayerRAPhase:
    def __init__(self, character_manager, game):
        self.character_manager = character_manager
        self.game = game
        self.active_abilities = self.get_active_abilities()

    def get_active_abilities(self):
        active_abilities = []
        characters = self.character_manager.characters()
        for character in characters:        
            for ability in character.active_role_abilities:
                if not character.role_ability_usage.get(ability.name, False):
                    active_abilities.append((character, ability))
        return active_abilities

    def execute_ability(self, character, ability, target=None):
        if (character, ability) in self.active_abilities:
            if ability.requires_target and target:
                ability.effect(target)
            else:
                ability.effect(character)
            character.role_ability_usage[ability.name] = True
            self.active_abilities = [item for item in self.active_abilities if item != (character, ability)]
            return f"{character.name} 使用了身分能力：{ability.name}"
        return "該角色的身分能力無法啟用"

    def scriptwriter_ai_execute(self):
        """
        劇本家自動執行角色能力，隨機選擇可用的能力或結束階段。
        """
        while True:
            # 加入 "END PHASE" 選項，確保劇本家最終會結束
            choices = self.active_abilities + [(None, "END PHASE")]
            character, ability = random.choice(choices)
            
            if ability == "END PHASE":
                print("劇本家選擇結束 RA Phase")
                break
            
            # 嘗試找到一個合法的目標（若能力需要）
            target = None
            if ability.requires_target:
                valid_targets = [char for char in self.character_manager.characters() if ability.target_condition(self.game, char)]
                if valid_targets:
                    target = random.choice(valid_targets)
                else:
                    continue  # 若無有效目標，跳過該能力
            
            result = self.execute_ability(character, ability, target)
            print(result)
        
        print("RA Phase 結束")
