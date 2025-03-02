import random

class RuleTable:
    def __init__(self, id=0, name="不應該出現這串字", main_rules=None, sub_rules=None, events=None, roles=None, special_rules=None):
        self.id = id  
        self.name = name
        self.main_rules = main_rules if main_rules is not None else []
        self.sub_rules = sub_rules if sub_rules is not None else []
        self.events = events if events is not None else []
        self.roles = roles if roles is not None else []
        self.special_rules = special_rules if special_rules is not None else []

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
        #    for idx, ability in enumerate(role.active_RAs, start=1):
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
    
    def reveal_criminal(self, game):
        """ 揭曉犯人 """
        game.add_public_info(f" {self.name} 的犯人是 {self.criminal.name}")

    def __str__(self):
        return self.name  # 返回事件名稱

class Role:
    def __init__(self, id=0, name='普通人',limit = None ,traits=None,passive_RAs=None, active_RAs=None):
        self.id = id  # 新增的編號屬性
        self.name = name # 身分名稱
        self.limit = limit
        self.traits = traits if traits is not None else []  # 特性列表
        self.active_RAs = active_RAs if active_RAs is not None else []  # 能力列表
        self.passive_RAs = passive_RAs if passive_RAs is not None else []  # 能力列表

    def get_role_by_role_name(rule_table, role_name):
        """依序輸入選定主要規則表以及身分名稱，輸出身分"""
        return next(role for role in rule_table.roles if role.name == role_name)

    def gain_passive_ability(self,ruletable_id, ability_id):
            # 先判斷是哪一張規則表
            # 接著判斷是哪個角色能力
            # 正式擴充能力資料庫
        return next((ability for ability in RAs_BTX if ability.id == ability_id), None)

class Rule:
    def __init__(self, id, name, assign_roles,  passive_RAs):
        self.id = id  # 新增的編號屬性
        self.name = name  # 規則名稱
        self.passive_RAs = passive_RAs   # 特殊規則，以被動能力製作
        self.assign_roles = assign_roles  # 涉及的身分列表


class ActiveRoleAbility:
    def __init__(self, id, name, description, effect, target_condition, requires_target = False ,owner_name=None):
        self.id = id  # 能力的唯一編號
        self.name = name  # 能力名稱
        self.description = description  # 能力描述
        self.requires_target = requires_target  # 是否需要選擇目標
        self.effect = effect  # 能力效果函數
        self.target_condition = target_condition  # 是否需要選擇目標
        self.owner_name = owner_name if owner_name else ""  # 擁有者名稱
        self.usage = True # 是否可使用，預設可
        self.limit_use = False # 是否為輪迴限用，預設為非

    def use(self, user, target=None):
        """執行主動能力"""
        if self.requires_target and target is None:
            raise ValueError(f"{self.name} 需要指定一個目標")
        self.usage = False
        self.effect(user, target) if self.requires_target else self.effect(user)
        
    def get_ability(ruletable_id, ability_id):
        rule_tables = {1: RAs_BTX()}  # 可擴展不同的規則表
        return next((ability for ability in rule_tables.get(ruletable_id, []) if ability.id == ability_id), None)

class PassiveRoleAbility:
    def __init__(self, id, name, description, trigger_condition, effect, owner_name=None):
        self.id = id  # 能力的唯一編號
        self.name = name  # 能力名稱
        self.description = description  # 能力描述
        self.trigger_condition = trigger_condition  # 觸發條件函數
        self.effect = effect  # 能力效果函數
        self.owner_name = owner_name if owner_name else "" # 擁有者名稱

    def get_ability(ruletable_id, ability_id):
        rule_tables = {1: RAs_BTX()}  # 可擴展不同的規則表
        return next((ability for ability in rule_tables.get(ruletable_id, []) if ability.id == ability_id), None)


def main_rules_BTX():
    return[
    Rule(101, "殺人計畫", assign_roles=["關鍵人物", "殺手", "黑幕"],passive_RAs=[]),
    Rule(102, "被封印之物", assign_roles=["黑幕", "邪教徒"], passive_RAs=[PassiveRoleAbility.get_ability(1, 89641021)]),
    Rule(103, "和我簽下契約吧！", assign_roles=["關鍵人物"], passive_RAs=[PassiveRoleAbility.get_ability(1, 89641031), PassiveRoleAbility.get_ability(1, 89641032)]),
    Rule(104, "未來改變作戰", assign_roles=["邪教徒", "時間旅行者"],passive_RAs=[PassiveRoleAbility.get_ability(1, 89641041)]),
    Rule(105, "巨型定時炸彈", assign_roles=["魔女"],  passive_RAs=[PassiveRoleAbility.get_ability(1, 89641051)]),
    ]
def sub_rules_BTX():
    return[
    Rule(111,"友情小圈圈", assign_roles=["朋友","朋友", "誤導者"], passive_RAs=[]),
    Rule(112, "戀愛的模樣", assign_roles=["病嬌", "戀人"], passive_RAs=[]),
    Rule(113, "殺人魔潛伏", assign_roles=["朋友", "殺人魔"], passive_RAs=[]),
    Rule(114, "人心惶惶", assign_roles=["誤導者"],  passive_RAs=[PassiveRoleAbility.get_ability(1,89641141)]),
    Rule(115, "惡性譫妄病毒", assign_roles=["誤導者"], passive_RAs=[PassiveRoleAbility.get_ability(1,89641151)]),
    Rule(116, "因果之線", assign_roles=[], passive_RAs=[PassiveRoleAbility.get_ability(1,89641161)]),
    Rule(117, "不定因子", assign_roles=["因子"], passive_RAs=[]),
]
def events_BTX():
    return[ 
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
                victims[0].change_anxiety(game,2),
                victims[1].change_conspiracy(game,1)
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
                game.immediately_lose() if hospital.conspiracy > 1 else None
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
            victim.change_conspiracy(game, 1)
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
        effect=lambda game, criminal, victim: game.area_manager.fetch_area_by_name("神社").change_conspiracy(game, 1)
    )
]
def roles_BTX():
    return [
        Role(101, "關鍵人物", traits=[], passive_RAs=[
            PassiveRoleAbility.get_ability(1, 1011)
        ]),
        Role(102, "殺手", traits=["友好無視"], passive_RAs=[
            PassiveRoleAbility.get_ability(1, 1021),
            PassiveRoleAbility.get_ability(1, 1022),
        ]),
        Role(103, "黑幕", traits=["友好無視"], active_RAs=[
            ActiveRoleAbility.get_ability(1, 1031)
        ]),
        Role(104, "邪教徒", traits=["友好無效"]),
        Role(105, "魔女", traits=["友好無效"]),
        Role(106, "時間旅行者", traits=["不死"], passive_RAs=[
            PassiveRoleAbility.get_ability(1, 1061)
        ]),
        Role(107, "朋友", traits=[], passive_RAs=[
            PassiveRoleAbility.get_ability(1, 1071),
            PassiveRoleAbility.get_ability(1, 1072)
        ]),
        Role(108, "誤導者", traits=[], active_RAs=[
            ActiveRoleAbility.get_ability(1, 1081)
        ]),
        Role(109, "病嬌", traits=[], passive_RAs=[
            PassiveRoleAbility.get_ability(1, 1091),
            PassiveRoleAbility.get_ability(1, 1092)
        ]),
        Role(110, "戀人", traits=[], passive_RAs=[
            PassiveRoleAbility.get_ability(1, 1101)
        ]),
        Role(111, "殺人魔", traits=[], passive_RAs=[
            PassiveRoleAbility.get_ability(1, 1111)
        ]),
        Role(112, "因子", traits=["友好無視"], passive_RAs=[
            PassiveRoleAbility.get_ability(1, 1121)
        ], active_RAs=[
            ActiveRoleAbility.get_ability(1, 1122)
        ])
    ]
def RAs_BTX():
    return [
        PassiveRoleAbility(id=1011, name="The key",
            description="此角色死亡時，劇本家勝利，輪迴結束。",
            trigger_condition="on_death",
            effect=lambda game, owner: game.immediately_lose()
        ),
        PassiveRoleAbility(id=1021, name="The killer",
            description="夜晚階段時，如果自己陰謀>=4，劇本家勝利，輪迴結束。",
            trigger_condition="night_phase",
            effect=lambda game, owner: game.immediately_lose() if owner.conspiracy >= 4 else None
        ),
        PassiveRoleAbility(id=1022, name="Kill Key",
            description="夜晚階段時，如果與同地區有陰謀值>=2的關鍵人物，將其殺害。",
            trigger_condition="night_phase",
            effect=lambda game, owner: [
                owner.kill_character(game, key)
                for key in game.character_manager.get_characters_in_area(owner.current_location)
                if key.role.name == "關鍵人物" and key.conspiracy >= 2
            ]
        ),
        ActiveRoleAbility(id=1031, name="conspirator",
            description="同地區的一個角色或者該地區+1陰謀",
            requires_target=True,
            target_condition=lambda game, owner, target: target.current_location == owner.current_location or target.name == owner.current_location,
            effect=lambda game, target: target.change_conspiracy(game, 1)
        ),
        PassiveRoleAbility(id=1061, name="Time traveler",
            description="輪迴結束時，如果自己友好<=2，劇本家勝利，輪迴結束。",
            trigger_condition="cycle_end",
            effect=lambda game, owner: game.lose_flag() if owner.friendship < 3 else None
        ),
        PassiveRoleAbility(id=1071, name="The friend",
            description="輪迴結束時，如果未能存活，劇本家勝利，身分公開。",
            trigger_condition="cycle_end",
            effect=lambda game, owner: (
                owner.reveal_role(game),
                game.lose_flag() if not owner.alive else None
            )
        ),
        ActiveRoleAbility(id=1081, name="Misleader",
            description="同地區的一個角色+1不安",
            requires_target=True,
            target_condition=lambda game, owner, target: target.current_location == owner.current_location,
            effect=lambda game, target: target.change_anxiety(game, 1)
        ),
        PassiveRoleAbility(id=1072, name="everlasting friendship",
            description="輪迴開始時，如果身分已經公開，+1友好",
            trigger_condition="cycle_start",
            effect=lambda game, owner: owner.change_friendship(1) if owner.revealed else None
        ),
        PassiveRoleAbility(id=1091, name="Lover",
            description="死亡時，戀人+6不安",
            trigger_condition="on_death",
            effect=lambda game, owner: [
                lover.change_anxiety(game, 6)
                for lover in game.character_manager.characters
                if lover.role.name == "戀人" and lover.alive
            ]
        ),
        PassiveRoleAbility(id=1092, name="Yandere",
            description="夜晚時，如果自己不安>2且陰謀>0，則劇本家勝利，輪迴結束",
            trigger_condition="night_phase",
            effect=lambda game, owner: game.immediately_lose() if owner.conspiracy > 0 and owner.anxiety > 2 else None
        ),
        PassiveRoleAbility(id=1101, name="Lover",
            description="死亡時，病嬌+6不安",
            trigger_condition="on_death",
            effect=lambda game, owner: [
                lover.change_anxiety(game, 6)
                for lover in game.character_manager.characters
                if lover.role.name == "病嬌" and lover.alive
            ]
        ),
        PassiveRoleAbility(id=1111, name="Murder",
            description="夜晚時，若有任何角色與其獨處，殺害該角色",
            trigger_condition="night_phase",
            effect=lambda game, owner: owner.murder_effect(game)
        ),
        PassiveRoleAbility(id=1121, name="factor key",
            description="當學校的陰謀>1，獲得關鍵人物的能力",
            trigger_condition="area_conspiracy",
            effect=lambda game, owner: game.gain_passive_ability(owner, 1011) if game.area_manager.fetch_area_by_name('學校').conspiracy > 1 else None
        ),
        ActiveRoleAbility(id=1122, name="factor misleader",
            description="當都市的陰謀>1，獲得誤導者的能力",
            requires_target=True,
            target_condition=lambda game, owner, target: target.current_location == owner.current_location and game.area_manager.fetch_area_by_name('都市').conspiracy > 1 ,
            effect=lambda game, target: target.change_anxiety(game, 1)
        ),
        PassiveRoleAbility(id=89641021, name="Unseal",
            description="輪迴結束時，若神社陰謀>=2，主角敗北。",
            trigger_condition="cycle_end",
            effect=lambda game, owner: game.lose_flag() if game.area_manager.areas[2].conspiracy > 1 else None
            ),
        PassiveRoleAbility(id=89641031, name="Despair",
            description="輪迴結束時，若關鍵人物陰謀>=2，主角敗北。",
            trigger_condition="cycle_end",
            effect=lambda game, owner: [game.lose_flag() 
                for key in game.character_manager.characters  # 遍歷所有角色
                if key.role.name == "關鍵人物"  # 確保對方是關鍵人物
                and key.conspiracy >= 2  # 確保關鍵人物的陰謀值達到 2 以上
                ]
            ),
        PassiveRoleAbility(id=89641032, name="Mahoshoujou",
            description="關鍵人物一定是少女。",
            trigger_condition="assign_roles",
            effect=lambda game, owner: game.special_flag("madoka")
            ),
        PassiveRoleAbility(id=89641041, name="Stein;Gate",
            description="輪迴結束時，若本輪迴中事件「蝴蝶效應」有發生過，主角敗北。",
            trigger_condition="cycle_end",
            effect=lambda game, owner: [game.lose_flag() 
                for event in game.scheduled_events  # 遍歷所有事件
                if event.name == "蝴蝶效應" and event.happened # 找到蝴蝶效應，而且他有發生過
            ]),
        PassiveRoleAbility(id=89641051, name="HugeTimeBomb",
            description="輪迴結束時，若魔女的初期地區陰謀>=2，主角敗北。",
            trigger_condition="cycle_end",
            effect=lambda game, owner:[game.lose_flag() 
                for key in game.character_manager.characters  # 遍歷所有角色
                if key.role.name == "關鍵人物"  # 確保對方是關鍵人物
                and game.area_manager.get_area_by_name(key.initial_location).conspiracy>= 2  # 確保關鍵人物的初期地區的陰謀值達到 2 以上
            ]),
        PassiveRoleAbility(id=89641141, name="collective panic",
            description="每輪迴一次，腳本家可以在能力階段使任意地區+1陰謀。（現階段改成送給誤導者一個額外能力）",
            trigger_condition="assign_roles",
            effect=lambda game, owner:game.character_manager.collective_panic()
            ),
        PassiveRoleAbility(id=89641151, name="Delirium Virus",
            description="本遊戲中，普通人不安>2時，取得殺人魔的能力。",
            trigger_condition="assigh_roles",
            effect=lambda game, owner: game.character_manager.DeliriumVirus(game)
        ),
        PassiveRoleAbility(id=89641152, name="Murder by Delirium Virus",
            description="夜晚且不安>2時，若有任何角色與其獨處，殺害該角色",
            trigger_condition="night_phase",
            effect=lambda game, owner:[ owner.murder_effect(game) if owner.anxiety > 2 and owner.role.name =="普通人" else None]
        ),
        PassiveRoleAbility(id=89641161, name="LineOfReincarnation",
            description= "輪迴重啟後，前一輪迴友好>0的角色+2不安。",
            trigger_condition="cycle_start",
            effect=lambda game, owner: game.character_manager.line_of_reincarnation(game)
            ),
    ]


def load_rule_table():
# 創建規則表
    return [
        RuleTable(
            id=1,
            name=  "Basic Tragedy X",
            main_rules=main_rules_BTX(),
            sub_rules=sub_rules_BTX(),
            events= events_BTX(),
            roles=roles_BTX(),
            special_rules=[],
        ),
        RuleTable(
            id=2,
            name=  "Mystery Circle",
            main_rules=main_rules_BTX(),
            sub_rules=sub_rules_BTX(),
            events= events_BTX(),
            roles=roles_BTX(),
            special_rules=[],
        ),
        RuleTable(
            id=3,
            name=  "Weird Mythology",
            main_rules=main_rules_BTX(),
            sub_rules=sub_rules_BTX(),
            events= events_BTX(),
            roles=roles_BTX(),
            special_rules=[],
        )
    ]

