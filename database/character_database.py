# database/character_database.py

class Character:
    def __init__(self, name, anxiety_threshold, initial_location, forbidden_area, attribute, friendly_abilities=None, special_ability=None, hidden_abilities=None):
        # 固定資訊
        self.name = name
        self.anxiety_threshold = anxiety_threshold
        self.initial_location = initial_location
        self.forbidden_area = forbidden_area
        self.attribute = attribute
        self.special_ability = special_ability
        self.friendly_abilities = friendly_abilities or []
        self.hidden_abilities = hidden_abilities or []

        # 浮動資訊
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None
        self.abilities_used = []

    def reset(self):
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = self.initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None
        self.abilities_used.clear()

    def move(self, location):
        if self.alive and location != self.forbidden_area:
            self.current_location = location

    def change_anxiety(self, amount):
        self.anxiety += amount

    def change_conspiracy(self, amount):
        self.conspiracy += amount

    def change_friendship(self, amount):
        self.friendship += amount

    def use_ability(self, ability, target=None):
        if ability in self.friendly_abilities:
            # 根據能力的不同實現相應的邏輯
            if ability == "友好2：同地區的１名另外一個\"學生\"-1不安" and target:
                target.change_anxiety(-1)
            # 添加更多能力的實現邏輯
            self.abilities_used.append(ability)
            print(f"{self.name} 使用了能力：{ability}")
        else:
            print(f"{self.name} 沒有這個能力：{ability}")

    def use_hidden_ability(self, ability, target=None):
        if ability in self.hidden_abilities:
            # 根據隱藏能力的不同實現相應的邏輯
            print(f"{self.name} 使用了隱藏能力：{ability}，通知劇本家")
            self.abilities_used.append(ability)
            # 這裡可以添加邏輯來通知劇本家
        else:
            print(f"{self.name} 沒有這個隱藏能力：{ability}")

    def can_use_ability(self, ability):
        return ability not in self.abilities_used

    def __str__(self):
        return f"Character({self.name}, Anxiety: {self.anxiety}, Conspiracy: {self.conspiracy}, Friendship: {self.friendship}, Location: {self.current_location}, Alive: {self.alive})"

def load_character_database():
    return [
        {
            'name': '男學生',
            'anxiety_threshold': 2,
            'initial_location': '學校',
            'forbidden_area': None,
            'attribute': ['學生', '少年'],
            'friendly_abilities': ['友好2：同地區的1名另外一個"學生"-1不安'],
            'special_ability': None
        },
        {
            'name': '女學生',
            'anxiety_threshold': 3,
            'initial_location': '學校',
            'forbidden_area': None,
            'attribute': ['學生', '少女'],
            'friendly_abilities': ['友好2：同地區的1名另外一個"學生"-1不安'],
            'special_ability': None
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
