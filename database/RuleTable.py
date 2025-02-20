import random

class RuleTable:
    def __init__(self, id=0, name="不應該出現這串字", main_rules=None, sub_rules=None, events=None, roles=None, special_rules=None):
        self.id = id  # 新增的編號屬性
        self.name = name
        self.main_rules = main_rules  # 主規則列表
        self.sub_rules = sub_rules   # 副規則列表
        self.events =  events      # 事件列表
        self.roles = roles       # 身分列表
        self.special_rules = special_rules  # 特殊規則列表

    def add_main_rule(self, rule):
        self.main_rules.append(rule)

    def add_sub_rule(self, rule):
        self.sub_rules.append(rule)

    def add_event(self, event):
        self.events.append(event)

    def add_role(self, role):
        self.roles.append(role)

    def add_special_rule(self, rule):
        self.special_rules.append(rule)
    
    def display_rules(self):
        #print(f"規則表編號: {self.id}")
        #print(f"名稱: {self.name}")
        #print("主規則:")
        #for index, rule in enumerate(self.main_rules, start=1):
            #print(f"{index}. {rule.name}: {rule.description}")
        
        #print("副規則:")
        #for index, rule in enumerate(self.sub_rules, start=1):
            #print(f"{index}. {rule.name}: {rule.description}")
        
        #print("事件:")
        #for index, event in enumerate(self.events, start=1):
        #    print(f"{index}. {event.name}")
        
        #print("身分:")
        #for index, role in enumerate(self.roles, start=1):
        #    print(f"{index}. {role.name}")
        #    for idx, ability in enumerate(role.abilities, start=1):
        #        print(f"   ({ability.active}): {ability.description}")
        
        #print("特殊規則:")
        #for index, rule in enumerate(self.special_rules, start=1):
        #    print(f"{index}. {rule}")
        return

    def get_rule_table_by_id(rule_table_id):
        return next((char for char in load_rule_table() if char.id == rule_table_id), None)

class Event:
    def __init__(self, id, name, victim_required=False,victim_count = 1, victim_condition=None, effect=None):
        self.id = id  # 事件編號
        self.name = name  # 事件名稱
        self.victim_required = victim_required  # 是否有受害者
        self.victim_condition = victim_condition or (lambda game, criminal, victim: False)
        self.effect = effect if effect else lambda game, criminal, victim: None
        self.criminal = None  # 存角色物件，而不是名稱
        self.happened = False  # 事件是否發生
        self.date = None  # 事件發生日期，預設為 None
        self.victim_count = victim_count # 事件受害者數量，預設為 1

    
    def trigger(self, game, script_writer):
        """ 觸發事件 """
        if self.criminal_name:
            criminal = game.character_manager.get_character_by_name(self.criminal_name)
        else:
            criminal = None
        
        self.effect(criminal, game, script_writer)
        self.happened = True


    def reveal_criminal(self, game):
        """ 揭曉犯人 """
        game.add_public_info(f" {self.name} 的犯人是 {self.criminal.name}")

    def __str__(self):
        return self.name  # 返回事件名稱

class Role:
    def __init__(self, id, name,limit = None ,traits=None, abilities=None):
        self.id = id  # 新增的編號屬性
        self.name = name  # 身分名稱
        self.limit = limit
        self.traits = traits if traits is not None else []  # 特性列表
        self.abilities = abilities if abilities is not None else []  # 能力列表


    def add_trait(self, trait):
        self.traits.append(trait)

    def add_ability(self, ability):
        self.abilities.append(ability)

class Rule:
    def __init__(self, id, name, description, asign_roles, special_effect=None):
        self.id = id  # 新增的編號屬性
        self.name = name  # 規則名稱
        self.description = description  # 規則描述
        self.asign_roles = asign_roles  # 涉及的身分列表
        self.special_effect = special_effect  # 特殊效果函數

    def add_role(self, role):
        self.roles.append(role)

    def set_special_effect(self, effect):
        self.special_effect = effect

    def apply_special_effect(self, game):
        if self.special_effect:
            return self.special_effect(game)
        return False

class ActiveRoleAbility:
    def __init__(self, id, name, description, effect,owner_name, requires_target=False):
        self.id = id  # 能力的唯一編號
        self.name = name  # 能力名稱
        self.description = description  # 能力描述
        self.effect = effect  # 能力效果函數
        self.requires_target = requires_target  # 是否需要選擇目標
        self.owner_name = owner_name

    def use(self, user, target=None):
        """執行主動能力"""
        if self.requires_target and target is None:
            raise ValueError(f"{self.name} 需要指定一個目標")
        self.effect(user, target) if self.requires_target else self.effect(user)


class PassiveRoleAbility:
    def __init__(self, id, name, description, condition, effect, owner_name):
        self.id = id  # 能力的唯一編號
        self.name = name  # 能力名稱
        self.description = description  # 能力描述
        self.condition = condition  # 觸發條件函數
        self.effect = effect  # 能力效果函數
        self.owner_name = owner_name

    def check_and_trigger(self, game, character):
        """檢查條件，若符合則觸發能力"""
        if self.condition(game, character):
            self.effect(character)


def load_rule_table():
# 創建規則表
    return [
        RuleTable(
            id=1,
            name=  "Basic Tragedy X",
            main_rules=[
                Rule(101, "殺人計畫", None, asign_roles={"關鍵人物": 1, "殺手": 1, "黑幕": 1}),
                Rule(102, "被封印之物",None, asign_roles={"黑幕": 1, "邪教徒": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利")),
                Rule(103, "和我簽下契約吧！", "輪迴結束時，若關鍵人物陰謀>1，腳本家勝利。關鍵人物必須為少女", asign_roles={"關鍵人物": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利")),
                Rule(104, "未來改變作戰", "蝴蝶效應事件發生後，該輪迴結束時腳本家勝利。", asign_roles={"邪教徒": 1, "時間旅行者": 1}),
                Rule(105, "巨型定時炸彈", "魔女*1。輪迴結束時，若魔女的初期所在區域陰謀>1，腳本家勝利。", asign_roles={"魔女": 1}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利"))
            ],
            sub_rules=[
                Rule(111,"友情小圈圈", None, asign_roles={"朋友": 2, "誤導者": 1}),
                Rule(112, "戀愛的模樣", None, asign_roles={"病嬌": 1, "戀人": 1}),
                Rule(113, "殺人魔潛伏", None, asign_roles={"朋友": 1, "殺人魔": 1}),
                Rule(114, "人心惶惶", "每輪迴一次，腳本家可以在能力階段使任意地區+1陰謀。", asign_roles={}, special_effect=lambda game_state: game_state.add_conspiracy_points_to_any_area()),
                Rule(115, "惡性譫妄病毒", "本遊戲中，普通人不安>2時，變成殺人魔。", asign_roles={"誤導者": 1}, special_effect=lambda game_state: game_state.transform_normal_to_murderer()),
                Rule(116, "因果之線", "輪迴重啟後，前一輪迴友好>0的角色+2不安。", asign_roles={}, special_effect=lambda game_state: game_state.add_anxiety_to_characters_with_friendship_above(0, 2))
            ],
            events= [ 
                Event(
                    id=101,
                    name="殺人事件",
                    victim_required=True,
                    victim_condition=lambda game, criminal, victim: victim.alive and criminal.current_location == victim.current_location and criminal != victim,
                    effect=lambda game, criminal, victim: criminal.kill_character(game, victim)
                ),
                Event(
                    id=102,
                    name="流言蜚語",
                    victim_required=True,
                    victim_count = 2,
                    victim_condition=lambda game, criminal, victim: victim.alive,  # 任何受害者皆可
                    effect=lambda game, criminal, victims: (
                            victims[0].change_anxiety(2),
                            victims[1].change_conspiracy(1)
                        ) if len(victims) >= 2 else None  # 確保有足夠的受害者
                    ),

                Event(
                    id=103,
                    name="自殺",      
                    victim_required=False,              
                    effect=lambda game, criminal, victims: criminal.kill_character(game, criminal)
                ),
                Event(
                    id=104,
                    name="醫院事件",
                    victim_required = True,  # 需要篩選受害者（醫院內的角色）
                    victim_count = None,
                    victim_condition = lambda game, criminal, victim: victim.current_location == "醫院" and victim.alive,  # 限定地點
                    effect=lambda game, criminal, victims: (
                        (hospital := game.area_manager.fetch_area_by_name("醫院")) and  # 確保醫院區域存在
                        (
                            [criminal.kill_character(game, victim) for victim in victims]
                            if hospital.conspiracy > 0 else None,
                            game.win_cycle() if hospital.conspiracy > 1 else None
                        )
                    )
                ),
                Event(
                    id=105,
                    name="遠距殺人",
                    victim_required=True,
                    victim_condition=lambda game, criminal, victim: victim.conspiracy>1 and victim.alive,
                    effect=lambda game, criminal, victim: criminal.kill_character(game, victim)
                ),
                Event(
                    id=106,
                    name="失蹤",
                    victim_required=True,
                    victim_condition=lambda game, criminal, victim: victim == 'Area', # 特殊需求，指定地區為受害者
                    effect=lambda game, criminal, victim: (
                        criminal.move_to_anywhere(victim.name),
                        victim.change_conspiracy(1)
                    )
                ),
                Event(
                    id=107,
                    name="流傳",
                    victim_required=True,
                    victim_count = 2,
                    victim_condition=lambda game, criminal, victim: victim.alive,  # 任何受害者皆可
                    effect=lambda game, criminal, victims: (
                            victims[0].change_friendship(2),
                            victims[1].change_friendship(-2)
                        ) if len(victims) >= 2 else None  # 確保有足夠的受害者
                    ),
                Event(
                    id=108,
                    name="蝴蝶效應",
                    victim_required=True,
                    victim_condition=lambda game, criminal, victim: victim.alive and criminal.current_location == victim.current_location,
                    effect=lambda game, criminal, victim: victim.butterfly_effect(game)
                ),
                Event(
                    id=109,
                    name="褻瀆",
                    victim_required=False,
                    effect=lambda game, criminal, victim: game.area_manager.fetch_area_by_name("神社").change_conspiracy(1)
                )
            ],

            roles=[
                Role(101, "關鍵人物", traits=[],abilities=[
                        PassiveRoleAbility(
                        id=1011,
                        name="The key",
                        description="此角色死亡時，劇本家勝利，輪迴結束。",
                        condition="on_death",
                        effect=lambda game, owner: game.cycle_end("lose") 
                    )
                ]
                ),
                Role(2, "殺手",traits=["友好無視"], abilities=[
        Role_Ability(id=201, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(3, "黑幕",traits=["友好無視"], abilities=[
        Role_Ability(id=301, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(4, "邪教徒",traits=["友好無視"], abilities=[
        Role_Ability(id=401, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(5, "魔女",traits=["友好無視"], abilities=[
        Role_Ability(id=501, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(6, "時間旅行者",traits=["友好無視"], abilities=[
        Role_Ability(id=601, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(7, "朋友",traits=["友好無視"], abilities=[
        Role_Ability(id=701, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(8, "誤導者",traits=["友好無視"], abilities=[
        Role_Ability(id=801, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(9, "病嬌",traits=["友好無視"], abilities=[
        Role_Ability(id=901, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(10, "戀人",traits=["友好無視"], abilities=[
        Role_Ability(id=1001, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(11, "殺人魔",traits=["友好無視"], abilities=[
        Role_Ability(id=1101, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ]),
                Role(12, "因子",traits=["友好無視"], abilities=[
        Role_Ability(id=1201, name="不安增加", active= True, description="自己增加 1 點不安", effect=lambda character: character.change_anxiety(1), requires_target=False),
        
                ])
            ],
            special_rules=[],
        )
    ]

