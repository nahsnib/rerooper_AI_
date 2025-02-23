from scriptwriter.ai_gameset import AIGameSet
from common.character import CharacterManager
from game import Game
from game_phases.player_detective.player_RA_phase import PlayerRAPhase
import random

def main():
    
    # 1️⃣ 產生遊戲設定
    gameset = AIGameSet()
    
    # 2️⃣ 使用 AIGameSet 的數據建立 Game 物件
    game = Game(
        selected_rule_table = gameset.selected_rule_table,  # 選規則表
        selected_main_rule = gameset.selected_main_rule,    # 選主規則
        selected_sub_rules = gameset.selected_sub_rules,    # 選副規則

        character_manager = gameset.character_manager,      # 人
        scheduled_events = gameset.scheduled_events,        # 事件
        time_manager = gameset.time_manager,                # 時間
        area_manager = gameset.area_manager,                # 地區
        passive_abilities = gameset.passive_abilities       # 物件導向的被動能力列表
    )
    
    
    # 初始化角色能力階段
    role_ability_phase = PlayerRAPhase(game)

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