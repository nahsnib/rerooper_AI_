def load_character_database():
    return [
        {
            'name': '男學生',
            'anxiety_threshold': 2,
            'initial_location': '學校',
            'forbidden_area': None,
            'attribute': ['學生', '少年'],
            'friendly_abilities': [
                {
                    'name': '友好2：同地區的１名另外一個"學生"-1不安',
                    'trigger': lambda character: character.friendship >= 2,
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location and '學生' in target.attribute,
                    'effect': lambda target: target.change_anxiety(-1)
                }
            ]
        },
        {
            'name': '女學生',
            'anxiety_threshold': 3,
            'initial_location': '學校',
            'forbidden_area': None,
            'attribute': ['學生', '少女'],
            'friendly_abilities': [
                {
                    'name': '友好2：同地區的１名另外一個"學生"-1不安',
                    'trigger': lambda character: character.friendship >= 2,
                    'target_required': True,
                    'target_condition': lambda target, character: target.current_location == character.current_location and '學生' in target.attribute,
                    'effect': lambda target: target.change_anxiety(-1)
                }
            ]
        },
        {
            'name': '大小姐',
            'anxiety_threshold': 1,
            'initial_location': '學校',
            'forbidden_area': None,
            'attribute': ['學生', '少女'],
            'friendly_abilities': ['友好3：當此角色位於學校或都市時才能使用此能力。對同地區的1名角色放置+1友好'],
            'special_ability': None
        },
        {
            'name': '巫女',
            'anxiety_threshold': 2,
            'initial_location': '神社',
            'forbidden_area': '鬧區',
            'attribute': ['學生', '少女'],
            'friendly_abilities': [
                '友好3：當此角色位於神社時才能使用此能力。神社-1陰謀',
                '友好5：得知同地區的一名角色的身份（1輪迴限用1次）'
            ],
            'special_ability': None
        },
        {
            'name': '刑警',
            'anxiety_threshold': 3,
            'initial_location': '都市',
            'forbidden_area': None,
            'attribute': ['大人', '男性'],
            'friendly_abilities': [
                '友好4：得知此輪迴中，一個已發生的事件之犯人。（1輪迴限用1次）',
                '友好5：當同地區的角色死亡時可立即使用此能力，使該死亡無效。（1輪迴限用1次）'
            ],
            'special_ability': None
        },
        {
            'name': '上班族',
            'anxiety_threshold': 2,
            'initial_location': '都市',
            'forbidden_area': '學校',
            'attribute': ['大人', '男性'],
            'friendly_abilities': ['友好3：公開此角色的身份'],
            'special_ability': None
        },
        {
            'name': '情報販子',
            'anxiety_threshold': 3,
            'initial_location': '都市',
            'forbidden_area': None,
            'attribute': ['大人', '女性'],
            'friendly_abilities': ['友好5：指定規則X1或規則X2，腳本家公開被指定的規則。（1輪迴限用1次）'],
            'special_ability': None
        },
        {
            'name': '醫生',
            'anxiety_threshold': 2,
            'initial_location': '醫院',
            'forbidden_area': None,
            'attribute': ['大人', '男性'],
            'friendly_abilities': [
                '友好2：同地區另一名角色+1不安或者-1不安。若此角色擁有友好無視，則劇本家也可以在劇本家能力使用階段時使用此能力',
                '友好3：本輪迴中，住院病人解除移動限制'
            ],
            'special_ability': None
        },
        {
            'name': '住院病人',
            'anxiety_threshold': 2,
            'initial_location': '醫院',
            'forbidden_area': ['學校', '神社', '都市'],
            'attribute': ['少年'],
            'friendly_abilities': [],
            'special_ability': None
        },
        {
            'name': '班長',
            'anxiety_threshold': 2,
            'initial_location': '學校',
            'forbidden_area': None,
            'attribute': ['學生', '少女'],
            'friendly_abilities': ['友好2：偵探回收1張【1輪迴只能使用1次】的行動卡（1輪迴限用1次）'],
            'special_ability': None
        },
        {
            'name': '異世界人',
            'anxiety_threshold': 2,
            'initial_location': '神社',
            'forbidden_area': '醫院',
            'attribute': ['少女'],
            'friendly_abilities': [
                '友好4：殺害同地區的1名角色（1輪迴限用1次）',
                '友好5：復活同地區的1具屍體（1輪迴限用1次）'
            ],
            'special_ability': None
        },
        {
            'name': '神格',
            'anxiety_threshold': 3,
            'initial_location': '神社',
            'forbidden_area': None,
            'attribute': ['少年', '少女'],
            'friendly_abilities': [
                '友好3：得知一個事件的犯人（1輪迴限用1次）',
                '友好5：從同一地區的1名角色或板塊上-1陰謀'
            ],
            'special_ability': '此角色要在剩餘輪迴數為X時才會正式進入遊戲中。X由腳本家構築腳本時秘密決定'
        },
        {
            'name': '偶像',
            'anxiety_threshold': 2,
            'initial_location': '都市',
            'forbidden_area': None,
            'attribute': ['學生', '少女'],
            'friendly_abilities': [
                '友好3：同地區的1名另外一個角色-1不安',
                '友好4：同地區的1名角色+1友好'
            ],
            'special_ability': None
        },
        {
            'name': '記者',
            'anxiety_threshold': 2,
            'initial_location': '都市',
            'forbidden_area': None,
            'attribute': ['大人', '男性'],
            'friendly_abilities': [
                '友好2：對同地區另外一名角色+1不安',
                '友好2：對同地區另外一名角色或該地區+1陰謀'
            ],
            'special_ability': None
        },
        {
            'name': '耆老',
            'anxiety_threshold': 4,
            'initial_location': '都市',
            'forbidden_area': None,
            'attribute': ['大人', '男性'],
            'friendly_abilities': [
                '友好5：公開"領地"上的1名角色的身份（1輪迴限用1次）'
            ],
            'special_ability': '此角色使用身份能力時，也可以從"領地"為出發點。由劇本家在製作劇本時指定1個地區作為"領地"，須公開'
        },
        {
            'name': '護士',
            'anxiety_threshold': 3,
            'initial_location': '醫院',
            'forbidden_area': None,
            'attribute': ['大人', '女性'],
            'friendly_abilities': [
                '友好2：同地區另外一名角色-1不安，僅能對不安達到或超過不安臨界的角色使用。這個能力不會被"友好無視"或"友好無效"取消'
            ],
            'special_ability': None
        },
        {
            'name': '手下',
            'anxiety_threshold': 1,
            'initial_location': None,  # 初期地區由腳本家決定
            'forbidden_area': None,
            'attribute': ['大人', '男性'],
            'friendly_abilities': [
                '友好3：直到本輪迴結束，不會觸發此角色為犯人的事件'
            ],
            'special_ability': None
        },
        {
            'name': '學者',
            'anxiety_threshold': 2,
            'initial_location': '醫院',
            'forbidden_area': None,
            'attribute': ['大人', '男性'],
            'friendly_abilities': [
                '友好3：此角色的不安、友好、陰謀歸零。之後，若使用劇本中有使用"EX"的話，將該值增加或者減少1'
            ],
            'special_ability': '在輪迴開始時，腳本家可以對此角色+1不安、友好或陰謀（三選一）'
        },
        {
            'name': '幻象',
            'anxiety_threshold': 3,
            'initial_location': '神社',
            'forbidden_area': None,
            'attribute': ['虛構', '女性'],
            'friendly_abilities': [
                '友好3：將與此角色同地區的1名角色移動至任何地區（1輪迴限用1次）',
                '友好4：將此角色從遊戲版圖中移除，代表她不與任何角色相鄰，也不存在於任何一個地區'
            ],
            'special_ability': '不能在此角色上設置行動卡。設置在此角色所在地區的行動卡，會同時作用於此角色'
        }
    ]
