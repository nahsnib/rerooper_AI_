import random
import time

from database.RuleTable import RuleTable
from common.character import CharacterManager

class AiScriptwriterAbilityPhase:
    def __init__(self, character_manager, rule_table, game, max_operations=10, time_limit=30):
        self.character_manager = character_manager
        self.rule_table = rule_table
        self.game = game
        self.active_abilities = []
        self.max_operations = max_operations
        self.time_limit = time_limit

    def load_active_abilities(self):
        # 讀取所有角色的主動能力
        for character in self.character_manager.get_all_characters():
            if character.alive:
                for identity in character.identities:
                    abilities = self.rule_table.get_abilities(identity)
                    for ability in abilities:
                        if ability['type'] == 'active' and not character.ability_usage[ability['name']]:
                            self.active_abilities.append((character, ability))

    def choose_ability_and_execute(self, operation_count, start_time):
        # AI 劇本家選擇並執行能力
        for character, ability in self.active_abilities:
            if operation_count >= self.max_operations or time.time() - start_time >= self.time_limit:
                print("達到最大操作次數或時間限制，結束回合")
                return

            # 隨機選擇是否使用這個能力
            if random.choice([True, False]):
                if ability.get('target_required', False):
                    valid_targets = [target for target in self.character_manager.get_all_characters() if ability['target_condition'](target, character)]
                    if valid_targets:
                        target = self.choose_target(valid_targets)
                        ability['effect'](target)
                        character.ability_usage[ability['name']] = True
                        print(f"{character.name} 使用了能力：{ability['name']} 對 {target.name}")
                        operation_count += 1
                    else:
                        character.ability_usage[ability['name']] = True
                else:
                    ability['effect'](self.game)
                    character.ability_usage[ability['name']] = True
                    print(f"{character.name} 使用了能力：{ability['name']}")
                    operation_count += 1

    def choose_target(self, valid_targets):
        # AI 選擇一個合理的目標
        return random.choice(valid_targets)

    def start(self):
        self.load_active_abilities()
        operation_count = 0
        start_time = time.time()
        self.choose_ability_and_execute(operation_count, start_time)

if __name__ == "__main__":
    # 測試用例
    character_manager = CharacterManager()
    rule_table = RuleTable()
    game = None  # 假設有一個 Game 物件

    ai_phase = AiScriptwriterAbilityPhase(character_manager, rule_table, game)
    ai_phase.start()
