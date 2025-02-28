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

class Rule:
    def __init__(self, id, name, description, assign_roles, special_effect=None):
        self.id = id  # 新增的編號屬性
        self.name = name  # 規則名稱
        self.description = description  # 規則描述
        self.assign_roles = assign_roles  # 涉及的身分列表
        self.special_effect = special_effect  # 特殊效果函數


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
        

class PassiveRoleAbility:
    def __init__(self, id, name, description, trigger_condition, effect, owner_name=None):
        self.id = id  # 能力的唯一編號
        self.name = name  # 能力名稱
        self.description = description  # 能力描述
        self.trigger_condition = trigger_condition  # 觸發條件函數
        self.effect = effect  # 能力效果函數
        self.owner_name = owner_name if owner_name else "" # 擁有者名稱

    def get_passive_ability(ability_id):
        return next((ability for ability in load_rule_table() if ability.id == ability_id), None)

main_rules_BTX=[
    Rule(101, "殺人計畫", None, assign_roles={"關鍵人物", "殺手", "黑幕"}),
    Rule(102, "被封印之物",None, assign_roles={"黑幕", "邪教徒"}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利")),
    Rule(103, "和我簽下契約吧！", "輪迴結束時，若關鍵人物陰謀>1，腳本家勝利。關鍵人物必須為少女", assign_roles={"關鍵人物"}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利")),
    Rule(104, "未來改變作戰", "蝴蝶效應事件發生後，該輪迴結束時腳本家勝利。", assign_roles={"邪教徒", "時間旅行者"}),
    Rule(105, "巨型定時炸彈", "輪迴結束時，若魔女的初期所在區域陰謀>1，腳本家勝利。", assign_roles={"魔女"}, special_effect=lambda game_state: game_state.end_loop("腳本家勝利"))
],
sub_rules_BTX=[
    Rule(111,"友情小圈圈", None, assign_roles={"朋友","朋友", "誤導者"}),
    Rule(112, "戀愛的模樣", None, assign_roles={"病嬌", "戀人"}),
    Rule(113, "殺人魔潛伏", None, assign_roles={"朋友", "殺人魔"}),
    Rule(114, "人心惶惶", "每輪迴一次，腳本家可以在能力階段使任意地區+1陰謀。", assign_roles={"誤導者"}, special_effect=lambda game_state: game_state.add_conspiracy_points_to_any_area()),
    Rule(115, "惡性譫妄病毒", "本遊戲中，普通人不安>2時，變成殺人魔。", assign_roles={"誤導者"}, special_effect=lambda game_state: game_state.transform_normal_to_murderer()),
    Rule(116, "因果之線", "輪迴重啟後，前一輪迴友好>0的角色+2不安。", assign_roles={"因子"}, special_effect=lambda game_state: game_state.add_anxiety_to_characters_with_friendship_above(0, 2))
]
events_BTX=[ 
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
                game.death_flag() if hospital.conspiracy > 1 else None
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
],
roles_BTX=[
    Role(101, "關鍵人物", traits=[],passive_RAs=[
        PassiveRoleAbility(
            id=1011,
            name="The key",
            description="此角色死亡時，劇本家勝利，輪迴結束。",
            trigger_condition="on_death",
            effect=lambda game, owner: game.cycle_end("lose") 
            )
        ]
    ),
    Role(102, "殺手",traits=["友好無視"], passive_RAs=[
        PassiveRoleAbility(
            id=1021,
            name="The killer",
            description="夜晚階段時，如果自己陰謀>=4，劇本家勝利，輪迴結束。",
            trigger_condition="night_phase",
            effect=lambda game, owner: game.cycle_end("lose") if owner.conspiracy >= 4 else None
            ),          
        PassiveRoleAbility(
            id=1022,
            name="Kill Key",
            description="夜晚階段時，如果與同地區有陰謀值>=2的關鍵人物，將其殺害。",
            trigger_condition="night_phase",
            effect=lambda game, owner: [
                owner.kill_character(game, key)
                for key in game.character_manager.get_characters_in_area(owner.current_location)  # 遍歷該地區所有角色
                if key.role.name == "關鍵人物"  # 確保對方是關鍵人物
                and key.conspiracy >= 2  # 確保關鍵人物的陰謀值達到 2 以上
                ]
            )
        ]
    ),
    Role(103, "黑幕",traits=["友好無視"], active_RAs=[
        ActiveRoleAbility(
            id=1031,
            name="conspirator",
            description="同地區的一個角色或者該地區+1陰謀",
            requires_target = True,
            target_condition=lambda game, owner, target: target.current_location == owner.current_location or target.name == owner.current_location,
            effect=lambda game, target: target.change_conspiracy(game, 1) 
            )
        ]
    ),
    Role(104, "邪教徒",traits=["友好無效"]),
    Role(105, "魔女",traits=["友好無效"]),
    Role(106, "時間旅行者",traits=["不死"], passive_RAs=[
        PassiveRoleAbility(
            id=1061,
            name="Time traveler",
            description="輪迴結束時，如果自己友好<=2，劇本家勝利，輪迴結束。",
            trigger_condition="cycle_end",
            effect=lambda game, owner: game.cycle_end("lose") if owner.conspiracy > 3 else None
            )
        ]
    ),
    Role(107, "朋友",traits=[], passive_RAs=[
        PassiveRoleAbility(
            id=1071,
            name="The friend",
            description="輪迴結束時，如果未能存活，劇本家勝利，身分公開。",
            trigger_condition="cycle_end",
            effect=lambda game, owner: (
                owner.reveal_role(),  # 確保角色公開身份
                game.cycle_end("lose") if not owner.alive else None  # 若未存活則敗北
            )
        ),
        PassiveRoleAbility(
            id=1072,
            name="everlasting friendship",
            description="輪迴開始時，如果身分已經公開，+1友好",
            trigger_condition="cycle_start",
            effect=lambda game, owner: owner.change_friendship(1) if owner.revealed else None
        )
    ]
    ),
    Role(108, "誤導者",traits=[], active_RAs=[
            ActiveRoleAbility(
                id=1081,
                name="disturber",
                description="同地區的一個角色+1不安",
                requires_target = True,
                target_condition=lambda game, owner, target:target.current_location == owner.current_location,
                effect=lambda game, target: target.change_anxiety(1) 
                )
            ]
        ),
    Role(109, "病嬌",traits=[], passive_RAs=[
        PassiveRoleAbility(
            id=1091,
            name="Lover",
            description="死亡時，戀人+6不安",
            trigger_condition="on_death",
            effect=lambda game, owner: [
                lover.anxiety(6)
                for lover in game.character_manager.characters  # 遍歷所有角色
                if lover.role.name == "戀人"  # 確保對方是戀人
                and lover.alive
                ]
        ),
        PassiveRoleAbility(
            id=1092,
            name="Yandere",
            description="夜晚時，如果自己不安>2且陰謀>0，則劇本家勝利，輪迴結束",
            trigger_condition="night_phase",
            effect=lambda game, owner: game.cycle_end("lose") if owner.conspiracy > 0 and owner.anxiety>2  else None          
            )
        ]
        ),
    Role(110, "戀人",traits=[], passive_RAs=[
        PassiveRoleAbility(
            id=1101,
            name="Lover",
            description="死亡時，病嬌+6不安",
            trigger_condition="on_death",
            effect=lambda game, owner: [
                lover.anxiety(6)
                for lover in game.character_manager.characters  # 遍歷所有角色
                if lover.role.name == "病嬌"  # 確保對方是病嬌
                and lover.alive
            ]
            )]
        ),
    Role(111, "殺人魔",traits=[], passive_RAs=[
        PassiveRoleAbility(
            id=1111,
            name="Murder",
            description="夜晚時，若有任何角色與其獨處，殺害該角色",
            trigger_condition="night_phase",
            effect=lambda game, owner: owner.murder_effect(game)
        )]
        ),
    Role(112, "因子",traits=["友好無視"], passive_RAs=[
        PassiveRoleAbility(
            id=1121,
            name="factor_key",
            description="當學校的陰謀>1，獲得關鍵人物的能力",
            trigger_condition="area_conspiracy",
            effect=lambda game, owner: game.gain_passive_ability(owner,1011) if game.area_manager.fecth_area_by_name('學校').conspiracy >1 else None                
        )],
        active_RAs=[
        ActiveRoleAbility(
            id=1122,
            name="factor_disturber",
            description="如果都市的陰謀>1，對同地區的一名角色+1不安",
            target_condition=lambda game, owner, target: owner.current_location==target.current and game.area_maneager.fecth_area_by_name('都市').conspiracy >1,
            effect=lambda game, owner, target: target.change_anxiety(1) 
        ),
    ])    ]


def load_rule_table():
# 創建規則表
    return [
        RuleTable(
            id=1,
            name=  "Basic Tragedy X",
            main_rules=main_rules_BTX,
            sub_rules=sub_rules_BTX,
            events= events_BTX,
            roles=roles_BTX,
            special_rules=[],
        ),
        RuleTable(
            id=2,
            name=  "Mystery Circle",
            main_rules=main_rules_BTX,
            sub_rules=sub_rules_BTX,
            events= events_BTX,
            roles=roles_BTX,
            special_rules=[],
        ),
        RuleTable(
            id=3,
            name=  "Weird Mythology",
            main_rules=main_rules_BTX,
            sub_rules=sub_rules_BTX,
            events= events_BTX,
            roles=roles_BTX,
            special_rules=[],
        )
    ]

