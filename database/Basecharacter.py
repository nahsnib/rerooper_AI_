import random

class BaseCharacter:
    def __init__(self, Ch_id, name, anxiety_threshold, initial_location, forbidden_area, attributes, friendship_abilities, special_ability=None):
        self.Ch_id = Ch_id  # 新增的編號屬性
        self.name = name  # 角色名稱
        self.anxiety_threshold = anxiety_threshold  # 不安臨界值
        self.initial_location = initial_location  # 初始位置
        self.forbidden_area = forbidden_area  # 禁止進入的區域
        self.attributes = attributes  # 角色屬性
        self.friendship_abilities = friendship_abilities  # 友好能力
        self.special_ability = special_ability  # 特殊能力

    def use_ability(self, name, target=None):
            ability = next((a for a in self.friendship_abilities if a[name] == name), None)
            if ability and not self.friendship_ability_usage[name]:
                if ability['target_required']:
                    if target and (target.alive or name == '復活同地區的一具屍體'):
                        ability['effect'](self, target)
                        self.friendship_ability_usage[name] = 'used' if ability.get('limit_use', False) else True
                else:
                    ability['effect'](self)
                    self.friendship_ability_usage[name] = 'used' if ability.get('limit_use', False) else True



class FriendshipAbility:
    def __init__(self, FA_id,owner_name, name, required_friendship, 
                 active = True, target_condition = None, effect = None, limit_use=False,require_extra_selection=False):
        self.FA_id = FA_id
        self.owner_name = owner_name
        self.name = name
        self.required_friendship = required_friendship
        self.active = active        #都預設為主動能力
        self.target_condition = target_condition
        self.effect = effect

        self.limit_use = limit_use
        self.require_extra_selection = require_extra_selection  # 是否需要額外選擇

        self.daily_used = False     # 今天是否用過，預設0
        self.times_used = 0         # 本輪迴使用次數，預設0

    def is_available(self, owner):
        """檢查這個能力是否可用"""
        if self.limit_use and self.times_used >= 1:
            #print(f"⚠️ {self.name} 發動失敗，已達使用上限！")
            return False
        elif owner.friendship < self.required_friendship:
            #print(f"{self.name} 發動失敗，友好度不足)
            return False
        elif self.daily_used:
            #print(f"{self.name} 發動失敗，本日已經使用過")
            return False
        else:
            return True 
    
    def get_owner_by_name(self, game):
        return next((c for c in game.character_manager.characters if c.name == self.owner_name), None)

      
    def use(self, game, target, extra):
        owner = self.get_owner_by_name(game)       
        self.times_used += 1  
        self.daily_used = True
        if self.owner_name != '護士' and self.owner_name != '異質者': # 除了護士、異質者的友好能力，其他友好能力都要判定友好無視或友好無效
            if owner.friendship_ignore(): return 
        self.effect(game, owner, target, extra)  # 確保 effect 被執行


               

def load_Basecharacters():
    return [
        BaseCharacter(Ch_id=1, name='男學生',
            anxiety_threshold=2,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少年'],
            friendship_abilities=[
                FriendshipAbility(                
                    FA_id= 101,
                    name= '男學生：同地區的１名另外一個"學生"-1不安',
                    owner_name='男學生',
                    required_friendship= 2,
                    target_condition= lambda target, owner: target != owner and target.current_location == owner.current_location and '學生' in target.attributes,
                    effect=lambda game, owner, target,extra: target.change_anxiety(-1),
                )
            ]
        ),
        BaseCharacter(Ch_id=2, name='女學生',
            anxiety_threshold=3,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 201,
                    name= '女學生：同地區的１名另外一個"學生"-1不安',
                    owner_name='女學生',
                    required_friendship=  2,
                    target_condition= lambda target, owner: target != owner and target.current_location == owner.current_location and '學生' in target.attributes,
                    effect=lambda game, owner, target, extra: target.change_anxiety(-1),
                )
            ]
        ),
        BaseCharacter(Ch_id=3, name='大小姐',
            anxiety_threshold=1,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 301,
                    name= '大小姐：當此角色位於學校或都市時才能使用此能力。對同地區的1名角色放置+1友好',
                    owner_name='大小姐',
                    required_friendship= 3 ,
                    target_condition= lambda target, owner: target.current_location == owner.current_location and target.current_location in ['學校', '都市'],
                    effect=lambda game, owner, target, extra: target.change_friendship(1),
                )
            ]
        ),
        BaseCharacter(Ch_id=4, name='巫女',
            anxiety_threshold=2,
            initial_location='神社',
            forbidden_area=['都市'],
            attributes=['學生', '少女'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 401,
                    name= '巫女：當此角色位於神社時才能使用此能力。神社-1陰謀',
                    owner_name='巫女',
                    required_friendship=  3 ,
                    target_condition= lambda target, owner: target == '神社',
                    effect=lambda game, owner, target, extra: game.area_manager.areas[2].change_conspiracy(-1),
                ),
                FriendshipAbility(
                    FA_id= 402,
                    name= '巫女：得知同地區的一名角色的身份（1輪迴限用1次）',
                    owner_name='巫女',
                    required_friendship=  5,
                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect=lambda game, owner, target, extra: target.reveal_role(game),
                    limit_use= True # 限用能力
                )
            ]
        ),
        BaseCharacter(Ch_id=5, name='刑警',
            anxiety_threshold=3,
            initial_location='醫院',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendship_abilities=[ #目前難以設計，先略過。
                FriendshipAbility(
                    FA_id= 501,
                    owner_name='刑警',
                    name= '刑警：得知此輪迴中，一個已發生的事件之犯人。（1輪迴限用1次）',
                    required_friendship=  4,
                    target_condition= lambda target, owner: target == '事件',
                    effect=lambda game, owner, target, extra: target.reveal_criminal(game),
                    limit_use= True, # 限用能力
                    ),
                FriendshipAbility(
                    FA_id= 502,
                    owner_name='刑警',
                    name= '刑警：當同地區的角色死亡時可立即使用此能力，使該死亡無效。（1輪迴限用1次）',
                    required_friendship=  5,
                    active= False, # 被動能力
                    target_condition= lambda target, owner: None,                    
                    effect= lambda owner, target: None,
                    limit_use= True # 限用能力
                )
            ]
        ),
        BaseCharacter(Ch_id=6, name='上班族',
            anxiety_threshold=2,
            initial_location='都市',
            forbidden_area=['學校'],
            attributes=['大人', '男性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 601,
                    name= '上班族：公開此角色的身份',
                    owner_name='上班族',
                    required_friendship=  3,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target == owner,
                    effect=lambda game, owner, target, extra: target.reveal_role(game),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(Ch_id=7, name='情報販子',
            anxiety_threshold=3,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '女性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id=701,
                    owner_name="情報販子",
                    name="情報販子：公開一條副規則。（1輪迴限用1次）",
                    required_friendship=5,
                    active=True,  # 主動能力
                    target_condition=lambda target, owner: target == owner,
                    effect=lambda game, owner, target, extra: game.reveal_sub_rule(),  
                    limit_use=True  # 限用能力
                )
            ]
        ),
        BaseCharacter(Ch_id=8, name='醫生',
            anxiety_threshold=2,
            initial_location='醫院',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id=801,
                    owner_name='醫生',
                    name='醫生：同地區另一名角色+1不安或者-1不安。',
                    required_friendship=2,
                    active=True,  # 主動能力
                    target_condition=lambda target, owner: target.current_location == owner.current_location and target != owner,
                    effect=lambda game, owner, target, extra: target.change_anxiety(extra),  
                    limit_use=False,
                    require_extra_selection = True  # 需要額外選擇
                ),

                FriendshipAbility(
                    FA_id=802,
                    owner_name='醫生',
                    name='醫生：本輪迴中，住院病人解除移動限制',
                    required_friendship=3,
                    active=True,  # 主動能力
                    target_condition=lambda target, owner: target.name == '住院病人',
                    effect=lambda game, owner, target, extra: setattr(target, 'forbidden_location', []),  # 修正 effect
                    limit_use=False
                )

            ]
        ),
        BaseCharacter(Ch_id=9, name='住院病人',
            anxiety_threshold=2,
            initial_location='醫院',
            forbidden_area=['學校', '神社', '都市'],
            attributes=['少年'],
            friendship_abilities=[],
            special_ability=None
        ),
        BaseCharacter(Ch_id=10, name='班長',
            anxiety_threshold=2,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendship_abilities=[ 
                FriendshipAbility(
                    FA_id=1001,
                    owner_name='班長',
                    name='班長：偵探重置1張【1輪迴只能使用1次】的行動（1輪迴限用1次）',
                    required_friendship=2,
                    active=True,  # 主動能力
                    target_condition=lambda target, owner: target == '行動',  # 特殊條件，選擇行動使用次數為 1 且已使用過的行動
                    effect=lambda game, owner, target, extra: target.reset_action(),  # 修正 effect
                    limit_use=True,  # 限用能力
                )
            ]
        ),
        BaseCharacter(Ch_id=11, name='異世界人',
            anxiety_threshold=2,
            initial_location='神社',
            forbidden_area=['醫院'],
            attributes=['少女'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1101,
                    owner_name='異世界人',
                    name= '異世界人：殺害同地區的1名角色（1輪迴限用1次）',
                    required_friendship=  4,
                    active= True, # 主動能力

                    target_condition= lambda target, owner:  target != owner and target.current_location == owner.current_location,
                    effect=lambda game, owner, target, extra: owner.kill_character(game,target),
                    limit_use= True # 限用能力
                ),
                FriendshipAbility(
                    FA_id= 1102,
                    owner_name='異世界人',
                    name= '異世界人：復活同地區的1具屍體（1輪迴限用1次）',
                    required_friendship=  5,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect=lambda game, owner, target, extra: setattr(target, 'alive', True),
                    limit_use= True # 限用能力
                )
            ]
        ),
        BaseCharacter(Ch_id=12, name='神格',
            anxiety_threshold=3,
            initial_location='神社',
            forbidden_area=None,
            attributes=['少年', '少女'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1201,
                    owner_name='神格',
                    name= '神格：得知一個事件的犯人（1輪迴限用1次）',
                    required_friendship=  3,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target == '事件', # 特殊條件，選擇事件為類別
                    effect=lambda game, owner, target, extra: target.reveal_criminal(game),
                    limit_use= True, # 限用能力
                ),
                FriendshipAbility(
                    FA_id= 1202,
                    owner_name='神格',
                    name= '神格：從同一地區的1名角色或地區上-1陰謀',
                    required_friendship=  5,
                    active= True, # 主動能力
                    target_condition = lambda target, owner: (target.current_location == owner.current_location) 
                        or ( target.name == owner.current_location),
                    effect=lambda game, owner, target, extra: target.change_conspiracy(-1),
                    limit_use= False,
                )
            ],
            special_ability='此角色要在剩餘輪迴數為X時才會正式進入遊戲中。X由腳本家構築腳本時秘密決定'#目前難以設計，先略過。
        ),
        BaseCharacter(Ch_id=13, name='偶像',
            anxiety_threshold=2,
            initial_location='都市',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1301,
                    owner_name='偶像',
                    name= '偶像：同地區的1名另外一個角色-1不安',
                    required_friendship=  3,
                    active= True, # 主動能力
                    target_condition= lambda target, owner:  target != owner and target.current_location == owner.current_location,
                    effect=lambda game, owner, target, extra: target.change_anxiety(-1),
                    limit_use= False
                ),
                FriendshipAbility(
                    FA_id= 1302,
                    owner_name='偶像',
                    name= '偶像：同地區的1名角色+1友好',
                    required_friendship=  4,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target != owner and target.current_location == owner.current_location,
                    effect=lambda game, owner, target, extra: target.change_friendship(1),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(Ch_id=14, name='記者',
            anxiety_threshold=2,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1401,
                    owner_name='記者',
                    name= '記者：對同地區另外一名角色+1不安',
                    required_friendship=  2,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target != owner and target.current_location == owner.current_location,
                    effect=lambda game, owner, target, extra: target.change_anxiety(1),
                    limit_use= False
                ),
                FriendshipAbility(
                    FA_id= 1402,
                    owner_name='記者',
                    name= '記者：對同地區另外一名角色或該地區+1陰謀',
                    required_friendship=  2,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: ( target != owner and target.current_location == owner.current_location
                    ) or target.name == owner.current_location,
                    effect=lambda game, owner, target, extra: target.change_conspiracy(1),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(Ch_id=15, name='耆老',
            anxiety_threshold=4,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1501,
                    owner_name='耆老',
                    name= '耆老：公開"領地"上的1名角色的身份（1輪迴限用1次）',
                    required_friendship=  5,
                    active= True, # 主動能力
                    #因為難以設計，暫時用別的取代target_condition= lambda target, owner:target.alive and target != owner and (target.current_location == owner.current_location or target.current_location == owner.territory),
                    target_condition= lambda target, owner: target != owner and target.current_location == owner.current_location,
                    effect=lambda game, owner, target, extra: target.reveal_role(game),
                    limit_use= True # 限用能力
                )
            ],
            special_ability='此角色使用身份能力時，也可以從"領地"為出發點。由劇本家在製作劇本時指定1個地區作為"領地"，須公開'
        ),
        BaseCharacter(Ch_id=16, name='護士',
            anxiety_threshold=3,
            initial_location='醫院',
            forbidden_area=None,
            attributes=['大人', '女性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1601,
                    owner_name='護士',
                    name= '護士：同地區另外一名角色-1不安，僅能對不安達到或超過不安臨界的角色使用。這個能力不會被"友好無視"或"友好無效"取消',
                    required_friendship=  2,
                    active= True, # 主動能力
                    target_condition= lambda target, owner:  target != owner and target.current_location == owner.current_location and target.anxiety >= target.anxiety_threshold,
                    effect=lambda game, owner, target, extra: target.change_anxiety(-1),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(Ch_id=17, name='手下',
            anxiety_threshold=1,
            initial_location=None,  # 初期地區由腳本家決定
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1701,
                    owner_name='手下',
                    name= '手下：直到本輪迴結束，不會觸發此角色為犯人的事件',
                    required_friendship=  3,
                    target_condition= lambda target, owner: target == owner,
                    effect=lambda game, owner, target, extra: setattr(target, 'guilty', -1),  # 修正 effect
                )
            ]
        ),
        BaseCharacter(Ch_id=18, name='學者',
            anxiety_threshold=2,
            initial_location='醫院',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1801,
                    owner_name='學者',
                    name= '學者：此角色的不安、友好、陰謀歸零。之後，若使用劇本中有使用"EX"的話，將該值增加或者減少1',
                    required_friendship=  3,
                    target_condition= lambda target, owner: target == owner,
                    effect=lambda game, owner, target, extra: owner.scholar_effect(game, extra),
                    require_extra_selection = True  # 需要額外選擇
                )
            ],
            special_ability='在輪迴開始時，腳本家可以對此角色+1不安、友好或陰謀（三選一）'
        ),
        BaseCharacter(Ch_id=19, name='幻象',
            anxiety_threshold=3, 
            initial_location='神社', 
            forbidden_area=None, 
            attributes=['虛構', '女性'], 
            friendship_abilities=[
                FriendshipAbility(
                    FA_id=1901,
                    owner_name='幻象',
                    name='幻象：將與此角色同地區的1名角色移動至任何地區（1輪迴限用1次）',
                    required_friendship=3,
                    target_condition=lambda target, owner: target.current_location == owner.current_location,
                    effect=lambda game, owner, target, extra: target.move_to_anywhere(extra),
                    limit_use=True,  # 限用能力
                    require_extra_selection = True  # 需要額外選擇
                ),
                FriendshipAbility(
                    FA_id= 1902,
                    owner_name='幻象',
                    name= '幻象：將此角色從遊戲版圖中移除，代表她不與任何角色相鄰，也不存在於任何一個地區',
                    required_friendship=  4,
                    target_condition= lambda target, owner: target == owner,
                    effect=lambda game, owner, target, extra: setattr(target, 'current_location', None),
                )
            ],
            special_ability='不能在此角色上設置行動卡。設置在此角色所在地區的行動卡，會同時作用於此角色'
        ),
        BaseCharacter(Ch_id=20, name='異質者',
            anxiety_threshold=3, 
            initial_location='學校', 
            forbidden_area=None, 
            attributes=['學生', '少年'], 
            friendship_abilities=[
                FriendshipAbility(
                    FA_id=2001,
                    owner_name='異質者',
                    name='異質者：公開此角色的身份；這個能力不能在第一輪迴使用，這個能力不能被友好無視或者友好無效',
                    required_friendship=3,
                    target_condition= lambda target, owner: target == owner,
                    effect=lambda game, owner, target, extra: target.reveal_role(game),
                )
            ],
            special_ability='劇本構築時，這個角色的身份，必須從主規則、副規則賦予的身分以外，挑選並得到一個身份'
        )
    ]



def get_Basecharacter_by_id(Ch_id):
    return next((char for char in load_Basecharacters() if char.Ch_id == Ch_id), None)

def get_FriendshipAbility_by_id(FA_id):
    return next((ability for char in load_Basecharacters() for ability in char.friendship_abilities if ability.FA_id == FA_id), None)