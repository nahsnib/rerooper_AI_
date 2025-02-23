
from database.Basecharacter import get_Basecharacter_by_id, FriendshipAbility
from database.RuleTable import Role
import random
import logging
from game_gui import GameGUI

class Character:
    def __init__(self, Ch_id, name, anxiety_threshold, initial_location, forbidden_area, attributes, friendship_abilities, 
                 special_ability=None, traits=None):
        self.Ch_id = Ch_id
        self.name = name
        self.anxiety_threshold = anxiety_threshold
        self.initial_location = initial_location
        self.forbidden_area = forbidden_area or []
        self.attributes = attributes
        self.friendship_abilities = friendship_abilities or []
        self.special_ability = special_ability
        self.role = Role()  # 初始化角色身分名稱
        self.pickup = False  # 是否為隨機選擇的角色

        # 浮動資訊
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.alive = True
        self.is_criminal = False
        self.event_crimes = []
        if self.initial_location == None:       # 設置當前地區為初始地區，若沒有則隨機選擇
            self.move_to_anywhere(random.choice(['醫院', '神社', '都市', '醫院']))
        else :
            self.current_location = self.initial_location
        self.guilty = 0

    def char_cycle_reset(self):
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        if self.Ch_id == 18: self.butterfly_effect
        if self.initial_location == None:
            self.move_to_anywhere(random.choice('醫院', '神社', '都市', '醫院'))
        else :
            self.current_location = self.initial_location
        self.alive = True
        self.is_criminal = False
        self.event_crimes = []
        self.reset_ability_usage()
        self.guilty = 0

    def scholar_effect(self, game,extra):
        self.friendship = 0
        self.anxiety = 0
        self.conspiracy = 0
        game.EX_gauge += extra

    def change_anxiety(self, amount):
        self.anxiety = max(0, self.anxiety + int(amount))  # 最低 0

    def change_friendship(self, amount):
        self.friendship = max(0, self.friendship + amount)  # 最低 0

    def change_conspiracy(self, amount):
        self.conspiracy = max(0, self.conspiracy + amount)  # 最低 0

    def move_to_anywhere(self, new_location):
        """ 玩家選擇角色要移動的地點 """
        if new_location not in (self.forbidden_area):
            self.current_location = new_location
        
    def move_vertical(self):
        location_map = {
            "醫院": "都市",
            "都市": "醫院",
            "學校": "神社",
            "神社": "學校"
        }
        new_location = location_map.get(self.current_location, self.current_location)
        print(f"{self.name} 嘗試從 {self.current_location} 移動到 {new_location}，禁制地點是 {self.forbidden_area}")
        if new_location not in (self.forbidden_area):
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
        if new_location not in (self.forbidden_area):
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
        if new_location not in (self.forbidden_area):
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

    def reveal_role(self,game):
        print(f"{self.name} 的身份是{self.role.name}")
        if self.name == '異質者' and game.time_manager.total_cycles == game.time_manager.remains_cycles:
            return print("異質者的友好能力在最初輪迴不可使用！")
        game.add_public_info(f" {self.name} 的身分是 {self.role.name}")

    def kill_character(self, game, target):
        """執行角色死亡，並檢查是否有刑警可阻止該次死亡"""
        if target.role.traits == ['不死']:
            return

        # 先尋找「刑警」角色
        police = None
        for character in game.character_manager.characters:
            if character.name == "刑警":
                police = character
                break  # 找到刑警後，立即停止搜尋

        # 如果沒有刑警，直接讓角色死亡
        if not police:
            target.alive = False
            return

        # 查找刑警的「刑警能力」(FA_id = 502)
        police_ability = next(
            (fa for fa in police.friendship_abilities if fa.FA_id == 502),
            None
        )

        # 檢查刑警是否符合條件
        if (
            police.alive and
            police.current_location == target.current_location and
            police.friendship >= 5 and  # 友好值 ≥ 5
            police_ability and police_ability.times_used == 0  # 能力未使用
        ):
            # 詢問玩家是否要發動能力
            if game.game_gui.ask_player(target, 502): 
                police_ability.times_used += 1  # 標記能力已使用
                # 進行 `friendship_ignore()` 判定
                if not self.friendship_ignore():
                    # 若沒有被拒絕，成功救援
                    print(f"刑警保護了{target.name}")
                    return  # 直接結束，不進行死亡處理

        # 若無法阻止，則角色死亡
        target.alive = False

    def butterfly_effect(self, game):
        """交由AI決定一個屬性+1"""
        choice = random.choice(["friendship", "anxiety", "conspiracy"]) #簡化版本，目前都選陰謀
        if choice == "friendship":
            self.change_friendship(1)
        elif choice == "anxiety":
            self.change_anxiety(1)
        elif choice == "conspiracy":
            self.change_conspiracy(1)

    def murder_effect(self, game):
        # 獲取當前地區的所有角色（不包含自身）
        characters_in_area = [char for char in game.get_characters_in_area(self.current_location) if char != self]

        # 若當前區域只剩一個其他角色，則執行殺害
        if len(characters_in_area) == 1:
            self.kill_character(game, characters_in_area[0])

    def friendship_ignore(self):
        """判斷角色的友好能力是否會被無效"""
        if '友好無效' in self.role.traits:
            print("能力被無效！")
            return True
        elif '友好無視' in self.role.traits:
            print("能力被無效！")
            return random.random() < 0.5
        else:
            return False  

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

    def initialize_characters(self, count_range=(10, 14), id_range=(1, 20)):
        """隨機選擇角色並初始化"""
        pickup_Ch_ids = random.sample(range(*id_range), random.randint(*count_range))
        
        for Ch_id in pickup_Ch_ids:
            base_char = next((char for char in self.character_db if char.Ch_id == Ch_id), None)  # 🔥 應該從 `character_db` 選取角色
            if base_char:
                character = self.initialize_character_by_id(base_char.Ch_id)  # 這裡應該創建新角色
                character.pickup = True
                self.characters.append(character)

        #print("✅ 已初始化角色: ", [char.name for char in self.characters])  # 確認角色是否正確選擇

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
