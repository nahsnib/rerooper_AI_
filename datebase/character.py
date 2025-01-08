class Character:
    def __init__(self, name, anxiety_threshold, initial_location, forbidden_area, attribute, friendly_abilities=None, special_ability=None):
        # 固定資訊
        self.name = name
        self.anxiety_threshold = anxiety_threshold
        self.initial_location = initial_location
        self.forbidden_area = forbidden_area
        self.attribute = attribute
        self.special_ability = special_ability
        self.friendly_abilities = friendly_abilities or []

        # 浮動資訊
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None

    def reset(self):
        self.anxiety = 0
        self.conspiracy = 0
        self.friendship = 0
        self.current_location = self.initial_location
        self.alive = True
        self.is_criminal = False
        self.secret_identity = None

    def move_horizontal(self):
        print(f"{self.name} 橫向移動")

    def move_vertical(self):
        print(f"{self.name} 縱向移動")

    def move_diagonal(self):
        print(f"{self.name} 斜角移動")

    def change_anxiety(self, amount):
        self.anxiety += amount
        print(f"{self.name} 的不安變為 {self.anxiety}")

    def change_conspiracy(self, amount):
        self.conspiracy += amount
        print(f"{self.name} 的陰謀變為 {self.conspiracy}")

    def change_friendship(self, amount):
        self.friendship += amount
        print(f"{self.name} 的友好變為 {self.friendship}")

    def prevent_anxiety_increase(self):
        print(f"{self.name} 的不安增加被禁止")

    def prevent_friendship_increase(self):
        print(f"{self.name} 的友好增加被禁止")

    def prevent_movement(self):
        print(f"{self.name} 的移動被禁止")

    def prevent_conspiracy_increase(self):
        print(f"{self.name} 的陰謀增加被禁止")

    def __str__(self):
        return f"Character({self.name}, Anxiety: {self.anxiety}, Conspiracy: {self.conspiracy}, Friendship: {self.friendship}, Location: {self.current_location}, Alive: {self.alive})"


class Action:
    def __init__(self, name, effect, usage_limit=None):
        self.name = name
        self.effect = effect
        self.usage_limit = usage_limit
        self.times_used = 0

    def can_use(self):
        if self.usage_limit is None:
            return True
        return self.times_used < self.usage_limit

    def use(self):
        if self.can_use():
            self.times_used += 1
            return True
        return False

    def reset(self):
        self.times_used = 0

    def __str__(self):
        return f"Action({self.name}, Used: {self.times_used}/{self.usage_limit})"


class Player:
    def __init__(self, role, actions):
        self.role = role
        self.actions = actions

    def choose_actions(self, board):
        chosen_actions = []
        for action in self.actions:
            if action.can_use():
                target = self.select_target(board)
                if action.use():
                    chosen_actions.append((action, target))
        return chosen_actions

    def select_target(self, board):
        return board.characters[0]

    def use_abilities(self, board):
        pass


class Board:
    def __init__(self):
        self.characters = []

    def display(self):
        for character in self.characters:
            print(character)


# 創建角色庫
characters = []

# 添加角色到角色庫

characters.append(Character(
    name="男學生",
    anxiety_threshold=2,
    initial_location="學校",
    forbidden_area=None,
    attribute=["學生", "少年"],
    friendly_abilities=["友好2：同地區的１名另外一個\"學生\"-1不安"]
))

characters.append(Character(
    name="女學生",
    anxiety_threshold=3,
    initial_location="學校",
    forbidden_area=None,
    attribute=["學生", "少女"],
    friendly_abilities=["友好2：同地區的１名另外一個\"學生\"-1不安"]
))

characters.append(Character(
    name="大小姐",
    anxiety_threshold=1,
    initial_location="學校",
    forbidden_area=None,
    attribute=["學生", "少女"],
    friendly_abilities=["友好3：當此角色位於學校或都市時才能使用此能力。對同地區的１名角色放置+1友好"]
))

characters.append(Character(
    name="巫女",
    anxiety_threshold=2,
    initial_location="神社",
    forbidden_area="鬧區",
    attribute=["學生", "少女"],
    friendly_abilities=[
        "友好3：當此角色位於神社時才能使用此能力。神社-1陰謀",
        "友好5：得知同地區的一名角色的身分（１輪迴限用１次）"
    ]
))

characters.append(Character(
    name="刑警",
    anxiety_threshold=3,
    initial_location="都市",
    forbidden_area=None,
    attribute=["大人", "男性"],
    friendly_abilities=[
        "友好4：得知此輪迴中，一個已發生的事件之犯人。（１輪迴限用１次）",
        "友好5：當同地區的角色死亡時可立刻使用此能力，使該死亡無效。（１輪迴限用１次）"
    ]
))

characters.append(Character(
    name="上班族",
    anxiety_threshold=2,
    initial_location="都市",
    forbidden_area="學校",
    attribute=["大人", "男性"],
    friendly_abilities=["友好3：公開此角色的身分"]
))

characters.append(Character(
    name="情報販子",
    anxiety_threshold=3,
    initial_location="都市",
    forbidden_area=None,
    attribute=["大人", "女性"],
    friendly_abilities=["友好5：指定規則Ｘ１或規則Ｘ２，腳本家公開被指定的規則。（１輪迴限用１次）"]
))

characters.append(Character(
    name="醫生",
    anxiety_threshold=2,
    initial_location="醫院",
    forbidden_area=None,
    attribute=["大人", "男性"],
    friendly_abilities=[
        "友好2：同地區另一名角色+1不安或者-1不安。若此角色擁有友好無視，則劇本家也可以在劇本家能力使用階段時使用此能力",
        "友好3：本輪迴中，住院病人解除移動限制"
    ]
))

characters.append(Character(
    name="住院病人",
    anxiety_threshold=2,
    initial_location="醫院",
    forbidden_area=["學校", "神社", "都市"],
    attribute=["少年"],
    friendly_abilities=[]
))

characters.append(Character(
    name="班長",
    anxiety_threshold=2,
    initial_location="學校",
    forbidden_area=None,
    attribute=["學生", "少女"],
    friendly_abilities=["友好2：偵探回收１張［１輪迴只能使用１次］的行動卡（１輪迴限用１次）"]
))

characters.append(Character(
    name="異世界人",
    anxiety_threshold=2,
    initial_location="神社",
    forbidden_area="醫院",
    attribute=["少女"],
    friendly_abilities=[
        "友好4：殺害同地區的１名角色（１輪迴限用１次）",
        "友好5：復活同地區的１具屍體（１輪迴限用１次）"
    ]
))

characters.append(Character(
    name="神格",
    anxiety_threshold=3,
    initial_location="神社",
    forbidden_area=None,
    attribute=["少年", "少女"],
    friendly_abilities=[
        "特性：此角色要在剩餘輪迴數為X時才會正式進入遊戲中。X由腳本家構築腳本時祕密決定",
        "友好3：得知一個事件的犯人（１輪迴限用１次）",
        "友好5：從同一地區的１名角色或板塊上-1陰謀"
    ]
))

characters.append(Character(
    name="偶像",
    anxiety_threshold=2,
    initial_location="都市",
    forbidden_area=None,
    attribute=["學生", "少女"],
    friendly_abilities=[
        "友好3：同地區的１名另一個角色-1不安",
        "友好4：同地區的１名角色+1友好"
    ]
))

characters.append(Character(
    name="記者",
    anxiety_threshold=2,
    initial_location="都市",
    forbidden_area=None,
    attribute=["大人", "男性"],
    friendly_abilities=[
        "友好2：對同地區另一名角色+1不安",
        "友好2：對同地區另一名角色或該地區+1陰謀"
    ]
))

characters.append(Character(
    name="耆老",
    anxiety_threshold=4,
    initial_location="都市",
    forbidden_area=None,
    attribute=["大人", "男性"],
    friendly_abilities=[
        "特性：此角色使用身分能力時，也可以從'領地'為出發點。由劇本家在製作劇本時指定１個地區作為'領地'，須公開",
        "友好5：公開'領地'上的１名角色的身分（１輪迴限用１次）"
    ]
))

characters.append(Character(
    name="護士",
    anxiety_threshold=3,
    initial_location="醫院",
    forbidden_area=None,
    attribute=["大人", "女性"],
    friendly_abilities=["友好2：同地區另外一名角色-1不安，僅能對不安達到或超過不安臨界的角色使用。這個能力不會被'友好無視'或'友好無效'取消"]
))

characters.append(Character(
    name="手下",
    anxiety_threshold=1,
    initial_location=None,  # 初期地區由劇本家決定
    forbidden_area=None,
    attribute=["大人", "男性"],
    friendly_abilities=["友好3：直到本輪迴結束，不會觸發此角色為犯人的事件"]
))

characters.append(Character(
    name="學者",
    anxiety_threshold=2,
    initial_location="醫院",
    forbidden_area=None,
    attribute=["大人", "男性"],
    friendly_abilities=[
        "特性：在輪迴開始時，腳本家可以對此角色+1不安、友好或陰謀（三選一）",
        "友好3：此角色的不安、友好、陰謀歸零。之後，若使用劇本中有使用'EX'的話，將該值增加或者減少１"
    ]
))

characters.append(Character(
    name="幻想",
    anxiety_threshold=3,
    initial_location="神社",
    forbidden_area=None,
    attribute=["虛構", "女性"],
    friendly_abilities=[
        "特性：不能在此角色上設置行動卡。設置在此角色所在地區的行動卡，會同時作用於此角色",
        "友好3：將與此角色同地區的1名角色移動至任意地區（１輪迴限用１次）",
        "友好4：將此角色從遊戲版圖中移除，代表他不與任何角色相鄰，也不存在於任何一個地區"
    ]
))

# 打印角色庫中的所有角色
for character in characters:
    print(character)
# 這裡省略了其他角色的添加，類似於上述代碼添加其他角色




