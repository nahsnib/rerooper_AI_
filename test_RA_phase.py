from scriptwriter.ai_gameset import AIGameSet
from common.character import CharacterManager
from game import Game
from game_phases.player_detective.player_role_ability_phase import PlayerRoleAbilityPhase
import random

def main():
    character_manager = CharacterManager()
    ai_gameset = AIGameSet(character_manager)

    # 設定角色並顯示
    characters = ai_gameset.characters
    for character in characters:
        character.pickup = True  # 確保角色被選中
        character_manager.add_character(character)

    # 顯示角色資訊
    for character in character_manager.get_characters():
        print(f"角色生成: {character.name}, 初始位置: {character.initial_location}")

    # 初始化遊戲
    game = Game(
        total_days=ai_gameset.total_days,
        total_cycles=ai_gameset.total_cycles,
        characters=ai_gameset.characters,
        scheduled_events=ai_gameset.scheduled_events,
        areas=ai_gameset.character_db
    )
    
    # 初始化角色能力階段
    role_ability_phase = PlayerRoleAbilityPhase(character_manager, game)

    # 模擬角色能力階段
    simulate_role_ability_phase(role_ability_phase)

def simulate_role_ability_phase(role_ability_phase):
    print("開始角色能力階段")
    active_abilities = role_ability_phase.get_active_abilities()

    while active_abilities:
        best_choice = None
        best_value = -float("inf")

        for character, ability in active_abilities:
            value = evaluate_ability(character, ability, role_ability_phase)
            if value > best_value:
                best_value = value
                best_choice = (character, ability)

        if best_choice:
            character, ability = best_choice
            if ability.requires_target:
                target = select_best_target(character, ability, role_ability_phase)
            else:
                target = None

            message = role_ability_phase.execute_ability(character, ability, target)
            print(message)

        active_abilities = role_ability_phase.get_active_abilities()

    print("角色能力階段結束")

def evaluate_ability(character, ability, role_ability_phase):
    # 評估每個能力的價值，可以根據遊戲狀態和角色能力的效果來計算
    # 這裡我們簡單地返回隨機值，實際上應該根據具體邏輯來計算
    return random.random()

def select_best_target(character, ability, role_ability_phase):
    # 選擇最佳目標，可以根據遊戲狀態和角色能力的效果來選擇
    # 這裡我們簡單地返回第一個角色，實際上應該根據具體邏輯來選擇
    return role_ability_phase.character_manager.get_characters()[0]

if __name__ == "__main__":
    main()