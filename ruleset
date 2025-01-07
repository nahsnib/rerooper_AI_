class RuleSet:
    def __init__(self, name, events, identities, main_roles, sub_roles, main_rules, sub_rules):
        self.name = name
        self.events = events
        self.identities = identities
        self.main_roles = main_roles
        self.sub_roles = sub_roles
        self.main_rules = main_rules
        self.sub_rules = sub_rules

    def __str__(self):
        return f"RuleSet({self.name})"

    def display(self):
        print(f"規則表: {self.name}")
        print("事件表:")
        for key, value in self.events.items():
            print(f"  {key}: {value}")
        print("\n身分:")
        for key, value in self.identities.items():
            print(f"  {key}: {value}")
        print("\n主要角色:")
        for key, value in self.main_roles.items():
            print(f"  {key}: {value}")
        print("\n次要角色:")
        for key, value in self.sub_roles.items():
            print(f"  {key}: {value}")
        print("\n主規則:")
        for key, value in self.main_rules.items():
            print(f"  {key}: {value}")
        print("\n副規則:")
        for key, value in self.sub_rules.items():
            print(f"  {key}: {value}")

# 創建 Basic Tragedy X 的規則表
events = {
    "A": "殺人事件：犯人殺害同地區的另外一位角色。",
    "B": "流言蜚語：選擇兩名角色，分別+2不安、+1陰謀",
    "C": "自殺：犯人死亡",
    "D": "醫院事件：若「醫院」的陰謀數>0，所有在該處的角色死亡；若「醫院」的陰謀數>1，腳本家勝利，輪迴結束",
    "E": "遠距殺人：殺害一個陰謀數>1的角色。",
    "F": "失蹤：犯人移動到其他地區，並且該地區+1陰謀。",
    "G": "流傳：將某一角色的-2友好，另一名角色+2友好。",
    "H": "蝴蝶效應：指定與犯人同一區域的任一角色，不安、友好或陰謀擇一+1",
    "I": "褻瀆：神社+2陰謀"
}

identities = {
    "2-1-1": "關鍵人物：（被動）此角色死亡時腳本家勝利，輪迴結束",
    "2-1-2": "殺手：特性友好無視。（被動）夜晚階段時，殺害同地區且陰謀>1的關鍵人物；（被動）夜晚階段時，如果這個角色陰謀>3，腳本家勝利，輪迴結束",
    "2-1-3": "黑幕：特性友好無視。（主動）同地區另外一個角色（或該地區）+1陰謀",
    "2-1-4": "邪教徒：特性友好無效。（被動）行動解決階段，處理完移動卡後，將該地區偵探方設置的「陰謀禁止」無效化（無論是針對角色或地區）",
    "2-1-5": "時間旅行者：（被動）絕對不會死亡。（被動）最後一天的夜晚階段，如果此角色友好<2，腳本家勝利，輪迴結束",
    "2-1-6": "魔女：特性友好無效",
    "2-2-1": "朋友：上限為2。（被動）輪迴結束時。如果這個角色已經死亡，腳本家勝利，但必須公開此身分。（被動）此角色的身分只要公開過，之後的輪迴開始時+1友好。",
    "2-2-2": "誤導者：上限為1。（主動）能力發動階段，腳本家可以使同地區任一角色+1不安。",
    "2-2-3": "戀人：（被動）死亡時情人+6不安",
    "2-2-4": "情人：（被動）死亡時戀人+6不安。（被動）夜晚階段，若此角色不安>3且陰謀>0，腳本家勝利，輪迴結束",
    "2-2-5": "殺人魔：（被動）夜晚階段，殺害與他獨處的角色",
    "2-2-6": "因子：特性友好無視。（被動）若學校陰謀>1，取得誤導者的能力；若鬧區陰謀>1，取得關鍵人物的能力。"
}

main_roles = {
    "3-1": "殺人計畫：關鍵人物*1、殺手*1、黑幕*1。",
    "3-2": "被封印之物：黑幕*1、邪教徒*1。輪迴結束時，如果神社陰謀>1，腳本家勝利",
    "3-3": "和我簽下契約吧！：關鍵人物*1。輪迴結束時，若關鍵人物陰謀>1，腳本家勝利。關鍵人物必須為少女。",
    "3-4": "未來改變作戰：邪教徒*1，時間旅行者*1。蝴蝶效應事件發生後，該輪迴結束時，腳本家勝利。",
    "3-5": "巨型定時炸彈：魔女*1。輪迴結束時，若魔女的初期所在區域陰謀>1，腳本家勝利。"
}

sub_roles = {
    "4-1": "友情小圈圈：朋友*2，誤導者*1",
    "4-2": "戀愛的模樣：戀人*1，情人*1",
    "4-3": "殺人魔潛伏：朋友*1，殺人魔*1",
    "4-4": "人心惶惶：每輪迴一次，腳本家可以在能力階段使任意地區+1陰謀。",
    "4-5": "惡性譫妄病毒：誤導者*1。本遊戲中，普通人不安>2時，變成殺人魔。",
    "4-6": "因果之線：無指定身分。輪迴重啟後，前一輪迴友好>0的角色+2不安。",
    "4-7": "不定因子：因子*1"
}

# 創建 Basic Tragedy X 規則表實例
basic_tragedy_x = RuleSet(
    name="Basic Tragedy X",
    events=events,
    identities=identities,
    main_roles=main_roles,
    sub_roles=sub_roles,
    main_rules=main_roles,
    sub_rules=sub_roles
)

# 顯示 Basic Tragedy X 規則表
basic_tragedy_x.display()
