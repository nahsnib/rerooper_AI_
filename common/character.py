
from database.Basecharacter import get_Basecharacter_by_id, FriendshipAbility
#from common.area_and_date import areas, hospital, shrine, city, school # 導入地區
import random
import logging
from game_gui import GameGUI

def friendship_ignore(character):
    """
    判斷角色的友好能力是否會被無效或無視
    :param character: 角色實例
    :return: (bool, str) 第一個值表示友好能力是否被無效或可能被無視，第二個值是判定結果的描述
    """
    if '友好無效' in character.traits:
        logging.info("友好能力無效")
        return (True, "友好能力無效")
    elif '友好無視' in character.traits:
        result = random.choice([True, False])
        if result:
            logging.info("友好能力無效")
            return (True, "友好能力無效")
        else:
            logging.info("友好能力有效")
            return (False, "友好能力有效")
    logging.info("友好能力有效")
    return (False, "友好能力有效")


class Character:
    def __init__(self, Ch_id, name, anxiety_threshold, initial_location, forbidden_area, attributes, friendship_abilities, special_ability=None, role_abilities=None,
     traits=None):
        self.Ch_id = Ch_id
        self.name = name
        self.anxiety_threshold = anxiety_threshold
        self.initial_location = initial_location
        self.forbidden_area = forbidden_area if forbidden_area is not None else []  # 確保為列表
        self.attributes = attributes
        self.friendship_abilities = friendship_abilities or []
        self.special_ability = special_ability
        self.traits = traits or []  # 初始化特性屬性
        self.role_name = "普通人"  # 初始化角色身分名稱
        self.role_abilities = role_abilities or []  # 確保初始化 role_abilities
        self.pickup = False  # 是否為隨機選擇的角色

        self.name = name.strip()  # 確保沒有前後空格
        print(f"🆕 角色初始化: '{self.name}'")

        # 浮動資訊
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.alive = True
        self.is_criminal = False
        self.event_crimes = []
        self.current_location = initial_location  # 設置當前地區
        self.friendship_ability_usage = {ability.name: False for ability in self.friendship_abilities}
        self.role_ability_usage = {ability['name']: False for ability in self.role_abilities}

    def reset(self):
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = self.initial_location
        self.alive = True
        self.is_criminal = False
        self.event_crimes = []
        self.reset_ability_usage()

    def scholar_effect(self, owner):
        owner.friendship = 0
        owner.anxiety = 0
        owner.conspiracy = 0

    def change_anxiety(self, amount):
        self.anxiety = max(0, self.anxiety + amount)  # 最低 0

    def change_friendship(self, amount):
        self.friendship = max(0, self.friendship + amount)  # 最低 0

    def change_conspiracy(self, amount):
        self.conspiracy = max(0, self.conspiracy + amount)  # 最低 0

    def move(self, location):
        if self.alive and location != self.forbidden_area:
            self.current_location = location

    def move_anywhere(self):
        new_location = self.current_location
        if self.current_location == "醫院":
            new_location = "都市"
        elif self.current_location == "都市":
            new_location = "醫院"
        elif self.current_location == "學校":
            new_location = "神社"
        elif self.current_location == "神社":
            new_location = "學校"
        
        if new_location not in (self.forbidden_area or []):
            self.current_location = new_location

        #暫時先用垂直移動取代
        #if is_player:
        #    self.show_move_anywhere_dialog()
        #else:
        #    # AI 隨機選擇新地區
        #    new_area = random.choice(list(areas.values()))
        #    self.perform_move(new_area)

    def move_vertical(self):
        location_map = {
            "醫院": "都市",
            "都市": "醫院",
            "學校": "神社",
            "神社": "學校"
        }
        new_location = location_map.get(self.current_location, self.current_location)
        print(f"{self.name} 嘗試從 {self.current_location} 移動到 {new_location}，禁制地點是 {self.forbidden_area}")
        if new_location not in (self.forbidden_area or []):
            self.current_location = new_location

    def move_horizontal(self):
        location_map = {
            "醫院": "神社",
            "神社": "醫院",
            "學校": "都市",
            "都市": "學校"
        }
        new_location = location_map.get(self.current_location, self.current_location)
        print(f"{self.name} 嘗試從 {self.current_location} 移動到 {new_location}，禁制地點是 {self.forbidden_area}")
        if new_location not in (self.forbidden_area or []):
            self.current_location = new_location
        
    def move_diagonal(self):
        location_map = {
            "醫院": "學校",
            "學校": "醫院",
            "都市": "神社",
            "神社": "都市" 
        }
        new_location = location_map.get(self.current_location, self.current_location)
        print(f"{self.name} 嘗試從 {self.current_location} 移動到 {new_location}，禁制地點是 {self.forbidden_area}")
        if new_location not in (self.forbidden_area or []):
            self.current_location = new_location
            
            
    def add_event_crime(self, event_name):
        self.is_criminal = True
        self.event_crimes.append(event_name)

    def can_use_ability(self, ability_name):
        return (ability_name not in self.friendship_ability_usage or not self.friendship_ability_usage[ability_name]) and \
               (ability_name not in self.role_ability_usage or not self.role_ability_usage[ability_name])

    def reset_ability_usage(self):
        for ability in self.friendship_ability_usage:
            self.friendship_ability_usage[ability] = False
        for ability in self.role_ability_usage:
            self.role_ability_usage[ability] = False

    def reveal_identity(self):
        self.identity_revealed = True
        print(f"{self.name} 的身份已公開")

    def kill_character(self, character):
        # 角色死亡前，檢查是否有刑警在同地區
        for potential_savior in self.characters:
            if potential_savior.current_location == character.current_location and "刑警" in potential_savior.attributes:
                decision = GameGUI.ask_user(f"{potential_savior.name} 可以使用能力拯救 {character.name}，是否發動？")
                if decision:
                    result = potential_savior.rescue_ability(character)
                    self.log_event(result)
                    return  # 終止死亡處理

        # 若無法拯救，則正式死亡
        character.alive = False
        self.log_event(f"{character.name} 已死亡。")


    def is_key_person(self):
        # 假設有一個方法來判定角色是否是關鍵人物
        return "關鍵人物" in self.traits

    def police_effect(self, game):
        if not game.occurred_events:
            return "目前沒有已發生的事件。"
    
        event_list = "\n".join([f"{event}: {culprit}" for event, culprit in game.occurred_events.items()])
        return f"已發生的事件與犯人：\n{event_list}"

    def rescue_effect(self, target):
        if target.alive == False:
            target.alive = True
            return f"{self.name} 使用了能力，使 {target.name} 復活！"
        return f"{target.name} 並沒有死亡，無法使用能力。"

    def __str__(self):
        return f"Character({self.name}, Anxiety: {self.anxiety}, Conspiracy: {self.conspiracy}, Friendship: {self.friendship}, Location: {self.current_location}, Alive: {self.alive}, Event Crimes: {self.event_crimes})"


class CharacterManager():
    def __init__(self,character_db):
        self.characters = []
        self.character_db = character_db  # 存入角色資料庫

    def add_character(self, character):
        self.characters.append(character)

    def get_pickup_characters(self):
        return [character for character in self.characters if character.pickup]
    
    def get_character_by_name(self, name):
        """根據名稱查找角色"""
        return next((char for char in self.characters if char.name == name), None)

    def initialize_characters(self, count_range=(10, 14), id_range=(1, 19)):
        """隨機選擇角色並初始化"""
        pickup_Ch_ids = random.sample(range(*id_range), random.randint(*count_range))
        
        for Ch_id in pickup_Ch_ids:
            base_char = next((char for char in self.character_db if char.Ch_id == Ch_id), None)  # 🔥 應該從 `character_db` 選取角色
            if base_char:
                character = self.initialize_character_by_id(base_char.Ch_id)  # 這裡應該創建新角色
                character.pickup = True
                self.characters.append(character)

        print("✅ 已初始化角色: ", [char.name for char in self.characters])  # 確認角色是否正確選擇


    def initialize_character_by_id(self,Ch_id):
        base_character = get_Basecharacter_by_id(Ch_id)
        if not base_character:
            raise ValueError(f"Character with ID {Ch_id} not found")

        return Character(
            Ch_id=base_character.Ch_id,
            name=base_character.name,
            anxiety_threshold=base_character.anxiety_threshold,
            initial_location=base_character.initial_location,
            forbidden_area=base_character.forbidden_area,
            attributes=base_character.attributes,
            friendship_abilities=base_character.friendship_abilities,
            special_ability=base_character.special_ability
    )
    def get_valid_targets(self, fa: FriendshipAbility, all_characters):
        """篩選符合該友好能力目標條件的角色"""
        if not fa.target_required:
            return []  # 如果不需要目標，則直接返回空清單

        return [
            target for target in all_characters
            if target is not self  # 不能選擇自己
            and target.is_alive  # 不能選擇死亡角色
            and fa.target_condition(target, self)  # 必須符合技能條件
        ]



if __name__ == "__main__":
    character_manager = CharacterManager()
