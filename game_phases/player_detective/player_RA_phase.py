import random

class PlayerRAPhase:
    def __init__(self, game):
        self.game = game
        self.phase_type = "RA"

    def execute(self):
        while True:
            active_abilities = self.get_active_abilities()  # 每次迴圈更新
            if not active_abilities:
                self.on_end()  
                break  # 沒有可用能力就結束

            best_choice = None
            best_value = -float("inf")

            for character, ability in active_abilities:
                value = self.evaluate_ability(character, ability)
                if value > best_value:
                    best_value = value
                    best_choice = (character, ability)

            if best_choice:
                character, ability = best_choice
                target = self.select_best_target(character, ability) if ability.requires_target else None
                message = self.execute_ability(character, ability, target)
                print(message)

    def get_active_abilities(self):
        return [
            (character, ability)
            for character in self.game.character_manager.characters
            for ability in character.role.active_RAs 
            if ability and ability.usage
        ]

    def execute_ability(self, character, ability, target=None):
        if ability.usage:  # 確保能力可用
            ability.effect(self.game, target if ability.requires_target else character)
            ability.usage = False  # 標記能力已經使用
            return f"{character.name} 使用了身分能力：{ability.name}"
        return "該角色的身分能力無法啟用"

    def evaluate_ability(self, character, ability):
        return random.random()  # 這裡可以擴展成更複雜的評估邏輯

    def select_best_target(self, character, ability):
        if ability.id == 89641142:
            targets = self.game.area_manager.areas 
        # 測試中，黑幕暫時不影響地點
        else:
            targets = self.game.character_manager.characters
        return random.choice(targets)  

    def on_start(self):
        print("RA階段開始")

    def on_end(self):
        print("RA階段結束，清除暫存數據")
        self.game.phase_manager.advance_phase()
