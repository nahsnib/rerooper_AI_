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
    def __init__(self, FA_id,owner_name, name, required_friendship, active, target_condition, effect, limit_use,):
        self.FA_id = FA_id
        self.owner_name = owner_name
        self.name = name
        self.required_friendship = required_friendship
        self.active = active
        self.target_condition = target_condition
        self.effect = effect
        self.times_used = 0
        self.limit_use = limit_use
        self.daily_used = False

    def is_available(self, character):
        """檢查這個能力是否可用"""
        if self.limit_use and self.times_used >= 1:
            print(f"⚠️ {self.name} 發動失敗，已達使用上限！")
            return False
        # ✅ 增加 daily_used 檢查
        return character.friendship >= self.required_friendship and not self.daily_used and self.active
    
    def get_owner_by_name(self, game):
        return next((c for c in game.character_manager.characters if c.name == self.owner_name), None)

    def can_use(self, user, target):
        """檢查能力是否可以使用"""
        return self.target_condition(target, user)
       
    def use(self, game, target):
        owner = self.get_owner_by_name(game)
        if owner is None:
            print(f"⚠️ 發動失敗！找不到擁有者 {self.owner_name}")
            return False

        if self.can_use(owner, target):
            self.times_used += 1  
            self.daily_used = True

            if not self.friendship_ignore(owner):
                return False

            # ✅ 執行 effect
            self.effect(owner, target)  # 確保 effect 被執行

            # 🔍 觀察 `target` 在發動後的狀態

            return True
        else:
            print(f"⚠️ {self.name} 發動失敗，目標不符合條件！")
            return False



    def friendship_ignore(self, owner):
        """判定角色的特性是否影響友好能力"""
        if '友好無效' in owner.traits:
            print(f"⚠️ {owner.name} 被無效，無法發動！")
            return False  # 能力完全無效
        elif '友好無視' in owner.traits:
            if random.random() < 0.5:  # 50% 機率讓能力無效
                print(f"⚠️ {owner.name} 被無效，無法發動！")
                return False
        return True  # 能力可以正常發動
               

def load_Basecharacters():
    return [
        BaseCharacter(
            Ch_id=1,
            name='男學生',
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
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target != owner and target.current_location == owner.current_location and '學生' in target.attributes,
                    effect= lambda owner, target: target.change_anxiety(-1),
                    limit_use= False  
                )
            ]
        ),
        BaseCharacter(
            Ch_id=2,
            name='女學生',
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
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target != owner and target.current_location == owner.current_location and '學生' in target.attributes,
                    effect= lambda owner, target: target.change_anxiety(-1),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(
            Ch_id=3,
            name='大小姐',
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
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target.current_location == owner.current_location and  target.current_location == '學校' or '都市',
                    effect= lambda owner, target: target.change_friendliness(1),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(
            Ch_id=4,
            name='巫女',
            anxiety_threshold=2,
            initial_location='神社',
            forbidden_area='都市',
            attributes=['學生', '少女'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 401,
                    name= '巫女：當此角色位於神社時才能使用此能力。神社-1陰謀',
                    owner_name='巫女',
                    required_friendship=  3 ,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: owner.current_location == '神社' and target == '神社',
                    effect=   lambda area: area.change_conspiracy(-1),
                    limit_use= False
                ),
                FriendshipAbility(
                    FA_id= 402,
                    name= '巫女：得知同地區的一名角色的身份（1輪迴限用1次）',
                    owner_name='巫女',
                    required_friendship=  5,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect= lambda owner, target: target.reveal_identity(),
                    limit_use= True # 限用能力
                )
            ]
        ),
        BaseCharacter(
            Ch_id=5,
            name='刑警',
            anxiety_threshold=3,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendship_abilities=[ #目前難以設計，先略過。
                    FriendshipAbility(
                    FA_id= 501,
                    owner_name='刑警',
                    name= '刑警：得知此輪迴中，一個已發生的事件之犯人。（1輪迴限用1次）',
                    required_friendship=  4,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target == owner,
                    effect= lambda owner, target: owner.police_effect(),
                    limit_use= True # 限用能力
                    )
                
                #FriendshipAbility(
                #    FA_id= 502,
                #    owner_name='刑警',
                #    name= '刑警：當同地區的角色死亡時可立即使用此能力，使該死亡無效。（1輪迴限用1次）',
                #    required_friendship=  5,
                #    active= False, # 被動能力
                #    target_condition= lambda target, owner: target.is_dead and target.current_location == owner.current_location,
                #     
                #    effect= lambda owner, target: target.revive(),
                #    limit_use= True # 限用能力
                #)
            ]
        ),
        BaseCharacter(
            Ch_id=6,
            name='上班族',
            anxiety_threshold=2,
            initial_location='都市',
            forbidden_area='學校',
            attributes=['大人', '男性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 601,
                    name= '上班族：公開此角色的身份',
                    owner_name='上班族',
                    required_friendship=  3,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target == owner,
                    effect= None, #目前難以設計，先略過。
                    #effect= lambda owner: print(f"{owner.name} 的身份已公開"),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(
            Ch_id=7,
            name='情報販子',
            anxiety_threshold=3,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '女性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id=701,
                    owner_name="情報販子",
                    name="情報販子：指定規則X1或規則X2，腳本家公開被指定的規則。（1輪迴限用1次）",
                    required_friendship=5,
                    active=True,  # 主動能力
                    target_condition=lambda target, owner: target == owner,
                    effect = lambda game: game.reveal_sub_rule(),  # 使用我們新寫的函數
                    limit_use=True  # 限用能力
                )
            ]
        ),
        BaseCharacter(
            Ch_id=8,
            name='醫生',
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
                    effect=lambda game_gui, target: target.anxiety_ctrl(game_gui),  
                    limit_use=False
                ),

                FriendshipAbility(
                    FA_id=802,
                    owner_name='醫生',
                    name='醫生：本輪迴中，住院病人解除移動限制',
                    required_friendship=3,
                    active=True,  # 主動能力
                    target_condition=lambda target, owner: target.name == '住院病人',
                    effect=lambda game, target: setattr(target, 'forbidden_location', []),  # 修正 effect
                    limit_use=False
                )

            ]
        ),
        BaseCharacter(
            Ch_id=9,
            name='住院病人',
            anxiety_threshold=2,
            initial_location='醫院',
            forbidden_area=['學校', '神社', '都市'],
            attributes=['少年'],
            friendship_abilities=[],
            special_ability=None
        ),
        BaseCharacter(
            Ch_id=10,
            name='班長',
            anxiety_threshold=2,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendship_abilities=[ #目前難以設計，先略
                FriendshipAbility(
                    FA_id=1001,
                    owner_name='班長',
                    name='班長：偵探重置1張【1輪迴只能使用1次】的行動（1輪迴限用1次）',
                    required_friendship=2,
                    active=True,  # 主動能力
                    target_condition=lambda target, owner: target == owner,
                    effect=lambda game_gui, player: reset_chosen_action(game_gui, player),
                    limit_use=True  # 限用能力
                )
            ]
        ),
        BaseCharacter(
            Ch_id=11,
            name='異世界人',
            anxiety_threshold=2,
            initial_location='神社',
            forbidden_area='醫院',
            attributes=['少女'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1101,
                    owner_name='異世界人',
                    name= '異世界人：殺害同地區的1名角色（1輪迴限用1次）',
                    required_friendship=  4,
                    active= True, # 主動能力

                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect= lambda target, game: target.handle_death("友好能力 - 異世界人", game),
                    limit_use= True # 限用能力
                ),
                FriendshipAbility(
                    FA_id= 1102,
                    owner_name='異世界人',
                    name= '異世界人：復活同地區的1具屍體（1輪迴限用1次）',
                    required_friendship=  5,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target.is_dead and target.current_location == owner.current_location,
                    effect= lambda owner, target: target.revive(),
                    limit_use= True # 限用能力
                )
            ]
        ),
        BaseCharacter(
            Ch_id=12,
            name='神格',
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
                    target_condition= None,
                    effect= lambda game: game.reveal_event_culprit(),
                    limit_use= True # 限用能力
                ),
                FriendshipAbility(
                    FA_id= 1202,
                    owner_name='神格',
                    name= '神格：從同一地區的1名角色或地區上-1陰謀',
                    required_friendship=  5,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect= lambda owner, target: target.change_conspiracy(-1),
                    limit_use= False
                )
            ],
            special_ability='此角色要在剩餘輪迴數為X時才會正式進入遊戲中。X由腳本家構築腳本時秘密決定'#目前難以設計，先略過。
        ),
        BaseCharacter(
            Ch_id=13,
            name='偶像',
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
                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect= lambda owner, target: target.change_anxiety(-1),
                    limit_use= False
                ),
                FriendshipAbility(
                    FA_id= 1302,
                    owner_name='偶像',
                    name= '偶像：同地區的1名角色+1友好',
                    required_friendship=  4,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect= lambda owner, target: target.change_friendliness(1),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(
            Ch_id=14,
            name='記者',
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
                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect= lambda owner, target: target.change_anxiety(1),
                    limit_use= False
                ),
                FriendshipAbility(
                    FA_id= 1402,
                    owner_name='記者',
                    name= '記者：對同地區另外一名角色或該地區+1陰謀',
                    required_friendship=  2,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: (
                        hasattr(target, 'current_location') and target.current_location == owner.current_location
                    ) or target == owner.current_location,
                    effect= lambda owner, target: target.change_conspiracy(1),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(
            Ch_id=15,
            name='耆老',
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
                    target_condition= lambda target, owner: target.current_location == owner.territory,
                    effect= lambda owner, target: target.reveal_identity(),
                    limit_use= True # 限用能力
                )
            ],
            special_ability='此角色使用身份能力時，也可以從"領地"為出發點。由劇本家在製作劇本時指定1個地區作為"領地"，須公開'
        ),
        BaseCharacter(
            Ch_id=16,
            name='護士',
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
                    target_condition= lambda target, owner: target.current_location == owner.current_location and target.anxiety >= target.anxiety_threshold,
                    effect= lambda owner, target: target.change_anxiety(-1),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(
            Ch_id=17,
            name='手下',
            anxiety_threshold=1,
            initial_location='都市',  # 初期地區由腳本家決定，但暫時先設定為都市，方便測試
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1701,
                    owner_name='手下',
                    name= '手下：直到本輪迴結束，不會觸發此角色為犯人的事件',
                    required_friendship=  3,
                    active= True, # 主動能力
                    target_condition= None,
                    effect= lambda owner: owner.prevent_culprit_events(),
                    limit_use= False
                )
            ]
        ),
        BaseCharacter(
            Ch_id=18,
            name='學者',
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
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target == owner,
                    effect=lambda owner, target: target.scholar_effect(owner),
                    limit_use= False
                )
            ],
            special_ability='在輪迴開始時，腳本家可以對此角色+1不安、友好或陰謀（三選一）'
        ),
        BaseCharacter(
            Ch_id=19,
            name='幻象',
            anxiety_threshold=3, 
            initial_location='神社', 
            forbidden_area=None, 
            attributes=['虛構', '女性'], 
            friendship_abilities=[
                FriendshipAbility(
                    FA_id= 1901,
                    owner_name='幻象',
                    name= '幻象：將與此角色同地區的1名角色移動至任何地區（1輪迴限用1次）',
                    required_friendship=  3,
                    active= True, # 主動能力
                    target_condition= lambda target, owner: target.current_location == owner.current_location,
                    effect= lambda target, new_area: target.move_to(new_area),
                    limit_use= True # 限用能力
                ),
                FriendshipAbility(
                    FA_id= 1902,
                    owner_name='幻象',
                    name= '幻象：將此角色從遊戲版圖中移除，代表她不與任何角色相鄰，也不存在於任何一個地區',
                    required_friendship=  4,
                    active= True, # 主動能力
                    target_condition= None,
                    effect= lambda owner: owner.remove_from_board(),
                    limit_use= False
                )
            ],
            special_ability='不能在此角色上設置行動卡。設置在此角色所在地區的行動卡，會同時作用於此角色'
        )
    ]



def get_Basecharacter_by_id(Ch_id):
    return next((char for char in load_Basecharacters() if char.Ch_id == Ch_id), None)

def get_FriendshipAbility_by_id(FA_id):
    return next((ability for char in load_Basecharacters() for ability in char.friendship_abilities if ability.FA_id == FA_id), None)