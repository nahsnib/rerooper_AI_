import tkinter as tk
from tkinter import messagebox
from database.Basecharacter import load_character_database
#from common.area_and_date import areas, hospital, shrine, city, school # 導入地區
import random
import logging

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

def show_friendship_ignore(character):
    ignore, reason = friendship_ignore(character)
    message = f"角色: {character.name}\n結果: {reason}"
    show_message(message)

def show_message(message):
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口
    messagebox.showinfo("友好能力檢查結果", message)
    root.destroy()

class Character:
    def __init__(self, id, name, anxiety_threshold, initial_location, forbidden_area, attributes, friendly_abilities, special_ability=None, role_abilities=None, traits=None, role_name=None):
        self.id = id
        self.name = name
        self.anxiety_threshold = anxiety_threshold
        self.initial_location = initial_location
        self.forbidden_area = forbidden_area
        self.attributes = attributes
        self.friendly_abilities = friendly_abilities or []
        self.role_abilities = role_abilities or []  # 確保初始化 role_abilities
        self.special_ability = special_ability
        self.traits = traits or []  # 初始化特性屬性
        self.role_name = role_name  # 初始化角色身分名稱

        # 浮動資訊
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.alive = True
        self.is_criminal = False
        self.event_crimes = []
        self.current_location = initial_location  # 設置當前地區
        self.secret_identity = None
        self.friendly_ability_usage = {ability['name']: False for ability in self.friendly_abilities}
        self.role_ability_usage = {ability['name']: False for ability in self.role_abilities}

    def reset(self):
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = self.initial_location
        self.alive = True
        self.is_criminal = False
        self.event_crimes = []
        self.secret_identity = None
        self.reset_ability_usage()

    def move(self, location):
        if self.alive and location != self.forbidden_area:
            self.current_location = location

    def change_anxiety(self, amount):
        self.anxiety += amount

    def change_conspiracy(self, amount):
        self.conspiracy += amount

    def change_friendship(self, amount):
        self.friendship += amount

    def move_anywhere(self):
        new_location = self.current_location
        if self.current_location == "醫院":
            new_location = "鬧區"
        elif self.current_location == "鬧區":
            new_location = "醫院"
        elif self.current_location == "學校":
            new_location = "神社"
        elif self.current_location == "神社":
            new_location = "學校"
        
        if new_location != self.forbidden_area:
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
            "醫院": "鬧區",
            "鬧區": "醫院",
            "學校": "神社",
            "神社": "學校"
        }
        new_location = location_map.get(self.current_location, self.current_location)

        if new_location != self.forbidden_area:
            self.current_location = new_location

    def move_horizontal(self):
        location_map = {
            "醫院": "神社",
            "神社": "醫院",
            "學校": "鬧區",
            "鬧區": "學校"
        }
        new_location = location_map.get(self.current_location, self.current_location)

        if new_location != self.forbidden_area:
            self.current_location = new_location

    def move_diagonal(self):
        location_map = {
            "醫院": "學校",
            "學校": "醫院",
            "鬧區": "神社",
            "神社": "鬧區" 
        }
        new_location = location_map.get(self.current_location, self.current_location)

        if new_location != self.forbidden_area:
            self.current_location = new_location
            
            
    def add_event_crime(self, event_name):
        self.is_criminal = True
        self.event_crimes.append(event_name)

    def use_friendly_ability(self, ability_name, target=None):
        for ability in self.friendly_abilities:
            if ability['name'] == ability_name:
                if not self.friendly_ability_usage[ability_name] and ability['trigger'](self):
                    if ability['target_required']:
                        if target and ability['target_condition'](target, self):
                            ability['effect'](target)
                            self.friendly_ability_usage[ability_name] = True
                            print(f"{self.name} 使用了能力：{ability_name} 對 {target.name}")
                            return
                        else:
                            print(f"無效的目標：{target.name} 不符合條件")
                            return
                    else:
                        ability['effect'](self)
                        self.friendly_ability_usage[ability_name] = True
                        print(f"{self.name} 使用了能力：{ability_name}")
                        return
                else:
                    print(f"{self.name} 的友好度不足以使用能力：{ability_name} 或今天已使用過")
                    return
        print(f"{self.name} 沒有這個友好能力：{ability_name}")

    def use_role_ability(self, ability_name, target=None):
        for ability in self.role_abilities:
            if ability['name'] == ability_name:
                if not self.role_ability_usage[ability_name]:
                    if ability['target_required']:
                        if target and ability['target_condition'](target, self):
                            ability['effect'](target)
                            self.role_ability_usage[ability_name] = True
                            print(f"{self.name} 使用了身分能力：{ability_name} 對 {target.name}")
                            return
                        else:
                            print(f"無效的目標：{target.name} 不符合條件")
                            return
                    else:
                        ability['effect'](self)
                        self.role_ability_usage[ability_name] = True
                        print(f"{self.name} 使用了身分能力：{ability_name}")
                        return
                else:
                    print(f"{self.name} 今天已使用過身分能力：{ability_name}")
                    return
        print(f"{self.name} 沒有這個身分能力：{ability_name}")

    def can_use_ability(self, ability_name):
        return (ability_name not in self.friendly_ability_usage or not self.friendly_ability_usage[ability_name]) and \
               (ability_name not in self.role_ability_usage or not self.role_ability_usage[ability_name])

    def reset_ability_usage(self):
        for ability in self.friendly_ability_usage:
            self.friendly_ability_usage[ability] = False
        for ability in self.role_ability_usage:
            self.role_ability_usage[ability] = False

    def reveal_identity(self):
        self.identity_revealed = True
        print(f"{self.name} 的身份已公開")

    def handle_death(self, cause, game):
        """
        處理角色死亡的邏輯
        :param cause: 死亡原因，可以是事件、身分能力、友好能力等
        :param game: 遊戲實例，用於檢查和通知相關角色和玩家
        """
        if not self.alive:
            return  # 角色已經死亡，無需重複處理

        self.alive = False
        print(f"{self.name} 死亡，原因：{cause}")

        # 觸發刑警的友好能力
        for character in game.character_manager.get_all_characters():
            if character.role == "刑警" and character.current_location == self.current_location:
                if character.can_use_ability("阻止死亡"):
                    # 詢問玩家是否要發動刑警的友好能力
                    user_input = input(f"{character.name} 可以阻止 {self.name} 的死亡，是否發動能力？(y/n): ")
                    if user_input.lower() == 'y':
                        ignore, reason = friendship_ignore(character)
                        print(reason)
                        if not ignore:
                            character.use_friendly_ability("阻止死亡", self)
                            self.alive = True
                            print(f"{character.name} 阻止了 {self.name} 的死亡")
                            return

        # 檢查是否為關鍵人物的死亡
        if self.is_key_person():
            print(f"關鍵人物 {self.name} 死亡，輪迴立即結束")
            game.end_cycle()

        # 其他死亡處理邏輯
        # ...

    def is_key_person(self):
        # 假設有一個方法來判定角色是否是關鍵人物
        return "關鍵人物" in self.traits

    def __str__(self):
        return f"Character({self.name}, Anxiety: {self.anxiety}, Conspiracy: {self.conspiracy}, Friendship: {self.friendship}, Location: {self.current_location}, Alive: {self.alive}, Event Crimes: {self.event_crimes})"



class CharacterManager(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.characters = []
        self.selected_character = None
        self.selected_ability = None

        self.character_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.character_listbox.grid(row=0, column=0, sticky="nsew")
        self.character_listbox.bind("<<ListboxSelect>>", self.on_character_select)

        self.character_details = tk.Label(self, text="請選擇一個角色")
        self.character_details.grid(row=0, column=1, sticky="nsew")

        self.actions_frame = tk.Frame(self)
        self.actions_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.load_characters()
        self.update_listbox()

    def load_characters(self):
        characters_data = load_character_database()
        self.characters = []
        for char_data in characters_data:
            character = Character(**char_data.__dict__)  # 使用角色的字典來初始化
            self.characters.append(character)
        return self.characters

    def update_listbox(self):
        self.character_listbox.delete(0, tk.END)
        for character in self.characters:
            self.character_listbox.insert(tk.END, f"{character.id}: {character.name}")

    def on_character_select(self, event):
        selection = self.character_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_character = self.characters[index]
            self.update_character_details()

    def update_character_details(self):
        if self.selected_character:
            details = (f"名稱: {self.selected_character.name}\n"
                       f"位置: {self.selected_character.current_location}\n"
                       f"不安: {self.selected_character.anxiety}\n"
                       f"陰謀: {self.selected_character.conspiracy}\n"
                       f"友好: {self.selected_character.friendship}\n"
                       f"死亡: {'是' if not self.selected_character.alive else '否'}\n"
                       f"事件犯人: {', '.join(self.selected_character.event_crimes)}")
            self.character_details.config(text=details)

            # 更新行動和能力
            self.update_actions_and_abilities()

    def update_actions_and_abilities(self):
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        actions_label = tk.Label(self.actions_frame, text="可用行動與能力")
        actions_label.pack()

        # 顯示角色的友好能力和身分能力
        for ability in self.selected_character.friendly_abilities + self.selected_character.role_abilities:
            ability_name = ability['name']
            if self.selected_character.can_use_ability(ability_name):
                ability_button = tk.Button(self.actions_frame, text=ability_name, command=lambda a=ability_name: self.select_ability(a))
                ability_button.pack()
            else:
                ability_button = tk.Button(self.actions_frame, text=ability_name, state=tk.DISABLED)
                ability_button.pack()





if __name__ == "__main__":
    root = tk.Tk()
    root.title("角色管理")
    character_manager = CharacterManager(root)
    character_manager.pack(expand=True, fill=tk.BOTH)
    root.mainloop()