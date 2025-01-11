# ability_phase_1.py

class AbilityPhase1:
    def __init__(self, character_manager, game, scriptwriter):
        self.character_manager = character_manager
        self.game = game
        self.scriptwriter = scriptwriter
        self.active_abilities = []

    def check_abilities(self):
        # 檢查哪些角色的能力可以啟用
        self.active_abilities = []
        for character in self.character_manager.get_all_characters():
            for ability in character.friendly_abilities:
                if self.can_use_ability(character, ability):
                    self.active_abilities.append((character, ability))
        self.highlight_active_abilities()

    def can_use_ability(self, character, ability):
        # 判斷角色的能力是否可以啟用
        if ability['trigger'](character) and not character.friendly_ability_usage[ability['name']]:
            if ability.get('target_required', False):
                for target in self.character_manager.get_all_characters():
                    if ability['target_condition'](target, character):
                        return True
            else:
                return True
        return False

    def highlight_active_abilities(self):
        # 高亮可啟用的能力
        print("以下角色的能力可以啟用:")
        for character, ability in self.active_abilities:
            print(f"{character.name} - {ability['name']}")

    def execute_ability(self, character, ability):
        # 執行角色的能力
        if (character, ability) in self.active_abilities:
            if ability.get('target_required', False):
                valid_targets = [target for target in self.character_manager.get_all_characters() if ability['target_condition'](target, character)]
                if valid_targets:
                    target = self.choose_target(valid_targets)
                    if self.ask_scriptwriter_for_approval(character, ability, target):
                        ability['effect'](target)
                        character.friendly_ability_usage[ability['name']] = True
                        print(f"{character.name} 使用了能力：{ability['name']} 對 {target.name}")
                    else:
                        print(f"劇本家否決了 {character.name} 的能力：{ability['name']}")
                else:
                    print("沒有有效的目標")
                    return
            else:
                if self.ask_scriptwriter_for_approval(character, ability):
                    ability['effect'](self.game)
                    character.friendly_ability_usage[ability['name']] = True
                    print(f"{character.name} 使用了能力：{ability['name']}")
                else:
                    print(f"劇本家否決了 {character.name} 的能力：{ability['name']}")
            self.check_abilities()
        else:
            print("該角色的能力無法啟用")

    def choose_target(self, valid_targets):
        # 選擇目標
        print("可選目標:")
        for i, target in enumerate(valid_targets):
            print(f"{i + 1}. {target.name}")
        choice = int(input("選擇目標編號: ")) - 1
        return valid_targets[choice]

    def ask_scriptwriter_for_approval(self, character, ability, target=None):
        # 詢問劇本家是否允許使用能力
        identity = self.scriptwriter.get_identity(character)
        if '友好無效' in identity.attribute:
            print("必須拒絕此友好能力啟用")
            input("點選確定繼續...")
            return False
        elif '友好無視' in identity.attribute:
            print("是否要拒絕此友好能力的啟用？")
            approval = input("劇本家是否允許（yes/no）？: ")
            return approval.lower() == 'yes'
        else:
            print("必須接受此友好能力啟用")
            input("點選確定繼續...")
            return True

    def start(self):
        self.check_abilities()
        while True:
            choice = input("選擇要啟用的角色能力或輸入 'end' 結束階段: ")
            if choice == 'end':
                break
            else:
                selected_character = self.get_character_by_name(choice)
                if selected_character:
                    self.choose_ability(selected_character)
                else:
                    print("無效的選擇")

    def get_character_by_name(self, name):
        for character in self.character_manager.get_all_characters():
            if character.name == name:
                return character
        return None

    def choose_ability(self, character):
        # 選擇角色的能力
        valid_abilities = [ability for ability in character.friendly_abilities if self.can_use_ability(character, ability)]
        if valid_abilities:
            print(f"{character.name} 的可用能力:")
            for i, ability in enumerate(valid_abilities):
                print(f"{i + 1}. {ability['name']}")
            choice = int(input("選擇能力編號: ")) - 1
            self.execute_ability(character, valid_abilities[choice])
        else:
            print("該角色沒有可用的能力")
