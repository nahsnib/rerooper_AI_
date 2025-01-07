

# 劇本家的行動列表
scriptwriter_actions = [
    Action("橫向移動", lambda character: character.move_horizontal()),
    Action("縱向移動", lambda character: character.move_vertical()),
    Action("斜角移動", lambda character: character.move_diagonal(), usage_limit=1),
    Action("不安+1", lambda character: character.change_anxiety(1), usage_limit=2),
    Action("陰謀+1", lambda target: target.change_conspiracy(1)),
    Action("陰謀+2", lambda target: target.change_conspiracy(2), usage_limit=1),
    Action("不安-1", lambda character: character.change_anxiety(-1)),
    Action("不安禁止", lambda character: character.prevent_anxiety_increase()),
    Action("友好禁止", lambda character: character.prevent_friendship_increase())
]

# 偵探的行動列表
detective_actions = [
    Action("橫向移動", lambda character: character.move_horizontal()),
    Action("縱向移動", lambda character: character.move_vertical()),
    Action("禁止移動", lambda character: character.prevent_movement(), usage_limit=1),
    Action("不安+1", lambda character: character.change_anxiety(1)),
    Action("不安-1", lambda character: character.change_anxiety(-1), usage_limit=1),
    Action("友好+1", lambda character: character.change_friendship(1)),
    Action("友好+2", lambda character: character.change_friendship(2), usage_limit=1),
    Action("禁止陰謀", lambda target: target.prevent_conspiracy_increase())
]

# 創建劇本家和偵探玩家
scriptwriter = Player("劇本家", scriptwriter_actions)
detective = Player("偵探", detective_actions)

# 創建遊戲板
board = Board()
board.characters = characters

# 劇本家選擇行動
scriptwriter_actions = scriptwriter.choose_actions(board)
print("劇本家選擇的行動:")
for action, target in scriptwriter_actions:
    print(f"{action.name} 對 {target.name}")

# 偵探選擇行動
detective_actions = detective.choose_actions(board)
print("偵探選擇的行動:")
for action, target in detective_actions:
    print(f"{action.name} 對 {target.name}")
