class BaseCharacter:
    def __init__(self, id, name, anxiety_threshold, initial_location, forbidden_area, attributes, friendly_abilities, special_ability=None):
        self.id = id  # 新增的編號屬性
        self.name = name  # 角色名稱
        self.anxiety_threshold = anxiety_threshold  # 不安臨界值
        self.initial_location = initial_location  # 初始位置
        self.forbidden_area = forbidden_area  # 禁止進入的區域
        self.attributes = attributes  # 角色屬性
        self.friendly_abilities = friendly_abilities  # 友好能力
        self.special_ability = special_ability  # 特殊能力

    def use_ability(self, ability_name, target=None):
            ability = next((a for a in self.friendly_abilities if a['name'] == ability_name), None)
            if ability and not self.friendly_ability_usage[ability_name]:
                if ability['target_required']:
                    if target and (target.alive or ability_name == '復活同地區的一具屍體'):
                        ability['effect'](self, target)
                        self.friendly_ability_usage[ability_name] = 'used' if ability.get('limit_use', False) else True
                else:
                    ability['effect'](self)
                    self.friendly_ability_usage[ability_name] = 'used' if ability.get('limit_use', False) else True
                    
def load_character_database():
    return [
        BaseCharacter(
            id=1,
            name='男學生',
            anxiety_threshold=2,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少年'],
            friendly_abilities=[
                {
                    'id': 1,
                    'name': '友好2：同地區的１名另外一個"學生"-1不安',
                    'trigger': lambda character: character.friendship >= 2,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location and '學生' in target.attributes,
                    'effect': lambda target: target.change_anxiety(-1),
                    'limit_use': False  
                }
            ]
        ),
        BaseCharacter(
            id=2,
            name='女學生',
            anxiety_threshold=3,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendly_abilities=[
                {
                    'id': 2,
                    'name': '友好2：同地區的１名另外一個"學生"-1不安',
                    'trigger': lambda character: character.friendship >= 2,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location and '學生' in target.attributes,
                    'effect': lambda target: target.change_anxiety(-1),
                    'limit_use': False
                }
            ]
        ),
        BaseCharacter(
            id=3,
            name='大小姐',
            anxiety_threshold=1,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendly_abilities=[
                {
                    'id': 3,
                    'name': '友好3：當此角色位於學校或都市時才能使用此能力。對同地區的1名角色放置+1友好',
                    'trigger': lambda character: character.friendship >= 3 and character.current_location in ['學校', '都市'],
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target: target.change_friendliness(1),
                    'limit_use': False
                }
            ]
        ),
        BaseCharacter(
            id=4,
            name='巫女',
            anxiety_threshold=2,
            initial_location='神社',
            forbidden_area='鬧區',
            attributes=['學生', '少女'],
            friendly_abilities=[
                {
                    'id': 4,
                    'name': '友好3：當此角色位於神社時才能使用此能力。神社-1陰謀',
                    'trigger': lambda character: character.friendship >= 3 and character.current_location == '神社',
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda area: area.change_conspiracy(-1),
                    'limit_use': False
                },
                {
                    'id': 5,
                    'name': '友好5：得知同地區的一名角色的身份（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 5,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target: target.reveal_identity(),
                    'limit_use': True # 限用能力
                }
            ]
        ),
        BaseCharacter(
            id=5,
            name='刑警',
            anxiety_threshold=3,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendly_abilities=[
                {
                    'id': 6,
                    'name': '友好4：得知此輪迴中，一個已發生的事件之犯人。（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 4,
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda game: game.reveal_event_culprit(),
                    'limit_use': True # 限用能力

                },
                {
                    'id': 7,
                    'name': '友好5：當同地區的角色死亡時可立即使用此能力，使該死亡無效。（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 5,
                    'active': False, # 被動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.is_dead and target.current_location == character.current_location,
                    'effect': lambda target: target.revive(),
                    'limit_use': True # 限用能力
                }
            ]
        ),
        BaseCharacter(
            id=6,
            name='上班族',
            anxiety_threshold=2,
            initial_location='都市',
            forbidden_area='學校',
            attributes=['大人', '男性'],
            friendly_abilities=[
                {
                    'id': 8,
                    'name': '友好3：公開此角色的身份',
                    'trigger': lambda character: character.friendship >= 3,
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda character: print(f"{character.name} 的身份已公開"),
                    'limit_use': False
                }
            ]
        ),
        BaseCharacter(
            id=7,
            name='情報販子',
            anxiety_threshold=3,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '女性'],
            friendly_abilities=[
                {
                    'id': 9,
                    'name': '友好5：指定規則X1或規則X2，腳本家公開被指定的規則。（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 5,
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda game: game.reveal_rule(),
                    'limit_use': True # 限用能力
                }
            ]
        ),
        BaseCharacter(
            id=8,
            name='醫生',
            anxiety_threshold=2,
            initial_location='醫院',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendly_abilities=[
                {
                    'id': 10,
                    'name': '友好2：同地區另一名角色+1不安或者-1不安。若此角色的身分擁有特性友好無視、友好無效，則劇本家也可以在劇本家能力使用階段時使用此能力',
                    'trigger': lambda character: character.friendship >= 2,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target: target.change_anxiety(1),  # 或者 -1，取決於劇本家的選擇,
                    'limit_use': False
                },
                {
                    'id': 11,
                    'name': '友好3：本輪迴中，住院病人解除移動限制',
                    'trigger': lambda character: character.friendship >= 3,
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda game: game.remove_patient_restriction(),
                    'limit_use': False
                }
            ]
        ),
        BaseCharacter(
            id=9,
            name='住院病人',
            anxiety_threshold=2,
            initial_location='醫院',
            forbidden_area=['學校', '神社', '都市'],
            attributes=['少年'],
            friendly_abilities=[],
            special_ability=None
        ),
        BaseCharacter(
            id=10,
            name='班長',
            anxiety_threshold=2,
            initial_location='學校',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendly_abilities=[
                {
                    'id': 12,
                    'name': '友好2：偵探回收1張【1輪迴只能使用1次】的行動卡（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 2,
                    'active': True, # 主動能力
                    'target_required': True,
                    'effect': lambda game: game.detective_recover_action_card(),
                    'limit_use': True # 限用能力
                }
            ]
        ),
        BaseCharacter(
            id=11,
            name='異世界人',
            anxiety_threshold=2,
            initial_location='神社',
            forbidden_area='醫院',
            attributes=['少女'],
            friendly_abilities=[
                {
                    'id': 13,
                    'name': '友好4：殺害同地區的1名角色（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 4,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target, game: target.handle_death("友好能力 - 異世界人", game),
                    'limit_use': True # 限用能力
                },
                {
                    'id': 14,
                    'name': '友好5：復活同地區的1具屍體（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 5,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.is_dead and target.current_location == character.current_location,
                    'effect': lambda target: target.revive(),
                    'limit_use': True # 限用能力
                }
            ]
        ),
        BaseCharacter(
            id=12,
            name='神格',
            anxiety_threshold=3,
            initial_location='神社',
            forbidden_area=None,
            attributes=['少年', '少女'],
            friendly_abilities=[
                {
                    'id': 15,
                    'name': '友好3：得知一個事件的犯人（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 3,
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda game: game.reveal_event_culprit(),
                    'limit_use': True # 限用能力
                },
                {
                    'id': 16,
                    'name': '友好5：從同一地區的1名角色或地區上-1陰謀',
                    'trigger': lambda character: character.friendship >= 5,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target: target.change_conspiracy(-1),
                    'limit_use': False
                }
            ],
            special_ability='此角色要在剩餘輪迴數為X時才會正式進入遊戲中。X由腳本家構築腳本時秘密決定'
        ),
        BaseCharacter(
            id=13,
            name='偶像',
            anxiety_threshold=2,
            initial_location='都市',
            forbidden_area=None,
            attributes=['學生', '少女'],
            friendly_abilities=[
                {
                    'id': 17,
                    'name': '友好3：同地區的1名另外一個角色-1不安',
                    'trigger': lambda character: character.friendship >= 3,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target: target.change_anxiety(-1),
                    'limit_use': False
                },
                {
                    'id': 18,
                    'name': '友好4：同地區的1名角色+1友好',
                    'trigger': lambda character: character.friendship >= 4,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target: target.change_friendliness(1),
                    'limit_use': False
                }
            ]
        ),
        BaseCharacter(
            id=14,
            name='記者',
            anxiety_threshold=2,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendly_abilities=[
                {
                    'id': 19,
                    'name': '友好2：對同地區另外一名角色+1不安',
                    'trigger': lambda character: character.friendship >= 2,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target: target.change_anxiety(1),
                    'limit_use': False
                },
                {
                    'id': 20,
                    'name': '友好2：對同地區另外一名角色或該地區+1陰謀',
                    'trigger': lambda character: character.friendship >= 2,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target, area=None: target.change_conspiracy(1) if target else area.change_conspiracy(1),
                    'limit_use': False
                }
            ]
        ),
        BaseCharacter(
            id=15,
            name='耆老',
            anxiety_threshold=4,
            initial_location='都市',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendly_abilities=[
                {
                    'id': 21,
                    'name': '友好5：公開"領地"上的1名角色的身份（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 5,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.territory,
                    'effect': lambda target: target.reveal_identity(),
                    'limit_use': True # 限用能力
                }
            ],
            special_ability='此角色使用身份能力時，也可以從"領地"為出發點。由劇本家在製作劇本時指定1個地區作為"領地"，須公開'
        ),
        BaseCharacter(
            id=16,
            name='護士',
            anxiety_threshold=3,
            initial_location='醫院',
            forbidden_area=None,
            attributes=['大人', '女性'],
            friendly_abilities=[
                {
                    'id': 22,
                    'name': '友好2：同地區另外一名角色-1不安，僅能對不安達到或超過不安臨界的角色使用。這個能力不會被"友好無視"或"友好無效"取消',
                    'trigger': lambda character: character.friendship >= 2,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location and target.anxiety >= target.anxiety_threshold,
                    'effect': lambda target: target.change_anxiety(-1),
                    'limit_use': False
                }
            ]
        ),
        BaseCharacter(
            id=17,
            name='手下',
            anxiety_threshold=1,
            initial_location=None,  # 初期地區由腳本家決定
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendly_abilities=[
                {
                    'id': 23,
                    'name': '友好3：直到本輪迴結束，不會觸發此角色為犯人的事件',
                    'trigger': lambda character: character.friendship >= 3,
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda character: character.prevent_culprit_events(),
                    'limit_use': False
                }
            ]
        ),
        BaseCharacter(
            id=18,
            name='學者',
            anxiety_threshold=2,
            initial_location='醫院',
            forbidden_area=None,
            attributes=['大人', '男性'],
            friendly_abilities=[
                {
                    'id': 24,
                    'name': '友好3：此角色的不安、友好、陰謀歸零。之後，若使用劇本中有使用"EX"的話，將該值增加或者減少1',
                    'trigger': lambda character: character.friendship >= 3,
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda character: character.reset_attributes(),
                    'limit_use': False
                }
            ],
            special_ability='在輪迴開始時，腳本家可以對此角色+1不安、友好或陰謀（三選一）'
        ),
        BaseCharacter(
            id=19,
            name='幻象',
            anxiety_threshold=3,
            initial_location='神社',
            forbidden_area=None,
            attributes=['虛構', '女性'],
            friendly_abilities=[
                {
                    'id': 25,
                    'name': '友好3：將與此角色同地區的1名角色移動至任何地區（1輪迴限用1次）',
                    'trigger': lambda character: character.friendship >= 3,
                    'active': True, # 主動能力
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location,
                    'effect': lambda target, new_area: target.move_to(new_area),
                    'limit_use': True # 限用能力
                },
                {
                    'id': 26,
                    'name': '友好4：將此角色從遊戲版圖中移除，代表她不與任何角色相鄰，也不存在於任何一個地區',
                    'trigger': lambda character: character.friendship >= 4,
                    'active': True, # 主動能力
                    'target_required': False,
                    'effect': lambda character: character.remove_from_board(),
                    'limit_use': False
                }
            ],
            special_ability='不能在此角色上設置行動卡。設置在此角色所在地區的行動卡，會同時作用於此角色'
        )
    ]
