# rule_table.py

class RuleTable:
    def __init__(self, name):
        self.name = name
        self.main_rules = []  # 主規則列表
        self.sub_rules = []   # 副規則列表
        self.events = []      # 事件列表
        self.roles = []       # 身分列表
        self.special_rules = []  # 特殊規則列表

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
        print("主規則:")
        for index, rule in enumerate(self.main_rules, start=1):
            print(f"{index}. {rule.name}: {rule.description}")
        
        print("副規則:")
        for index, rule in enumerate(self.sub_rules, start=1):
            print(f"{index}. {rule.name}: {rule.description}")
        
        print("事件:")
        for index, event in enumerate(self.events, start=1):
            print(f"{index}. {event.name}: {event.effect}")
        
        print("身分:")
        for index, role in enumerate(self.roles, start=1):
            print(f"{index}. {role.name}")
            for idx, ability in enumerate(role.abilities, start=1):
                print(f"  {idx}. {ability.name} ({ability.type}): {ability.description}")
        
        print("特殊規則:")
        for index, rule in enumerate(self.special_rules, start=1):
            print(f"{index}. {rule}")


class Event:
    def __init__(self, name, effect):
        self.name = name  # 事件名稱
        self.effect = effect  # 事件效果函數


class Role:
    def __init__(self, name, traits=None, abilities=None):
        self.name = name  # 身分名稱
        self.traits = traits if traits is not None else []  # 特性列表
        self.abilities = abilities if abilities is not None else []  # 能力列表

    def add_trait(self, trait):
        self.traits.append(trait)

    def add_ability(self, ability):
        self.abilities.append(ability)


class Rule:
    def __init__(self, name, description, special_conditions=None, roles=None):
        self.name = name  # 規則名稱
        self.description = description  # 規則描述
        self.special_conditions = special_conditions if special_conditions is not None else []  # 特殊條件列表
        self.roles = roles if roles is not None else []  # 涉及的身分列表

    def add_special_condition(self, condition):
        self.special_conditions.append(condition)

    def add_role(self, role):
        self.roles.append(role)


class Ability:
    def __init__(self, name, type, description, effect):
        self.name = name  # 能力名稱
        self.type = type  # 能力類型 (主動 或 被動)
        self.description = description  # 能力描述
        self.effect = effect  # 能力效果函數


# 建立範例規則表
rule_table = RuleTable("Basic Tragedy X")


// 定義主要規則表 Basic Tragedy X
const BasicTragedyX = {
    name: "Basic Tragedy X",
    events: [
        {
            name: "殺人事件",
            effect: (culprit, area) => {
                const target = area.getRandomCharacterExcept(culprit); // 隨機選擇同地區的其他角色
                if (target) {
                    target.die();
                    console.log(`${culprit.name} 殺害了 ${target.name}`);
                }
            }
        },
        {
            name: "流言蜚語",
            effect: (culprit, area, scriptWriter) => {
                const targets = scriptWriter.chooseTwoCharacters(); // 腳本家選擇兩個角色
                targets[0].addAnxiety(2);
                targets[1].addConspiracyPoints(1);
                console.log(`${targets[0].name} +2 不安, ${targets[1].name} +1 陰謀`);
            }
        },
        {
            name: "自殺",
            effect: (culprit) => {
                culprit.die();
                console.log(`${culprit.name} 自殺`);
            }
        },
        {
            name: "醫院事件",
            effect: (area, scriptWriter) => {
                if (area.conspiracyPoints > 0) {
                    area.characters.forEach(character => character.die());
                    console.log(`醫院事件觸發，所有角色死亡`);
                }
                if (area.conspiracyPoints > 1) {
                    console.log(`醫院陰謀數量超過1，腳本家勝利，輪迴結束`);
                    scriptWriter.winCycle();
                }
            }
        },
        {
            name: "遠距殺人",
            effect: (scriptWriter) => {
                const target = scriptWriter.chooseCharacterWithCondition(
                    char => char.conspiracyPoints > 1
                );
                if (target) {
                    target.die();
                    console.log(`${target.name} 被遠距殺害`);
                }
            }
        },
        {
            name: "失蹤",
            effect: (culprit, area, scriptWriter) => {
                const newArea = scriptWriter.chooseAreaExcept(area);
                culprit.moveTo(newArea);
                newArea.addConspiracyPoints(1);
                console.log(`${culprit.name} 移動到 ${newArea.name}, 該地區 +1 陰謀`);
            }
        },
        {
            name: "流傳",
            effect: (culprit, scriptWriter) => {
                const [target1, target2] = scriptWriter.chooseTwoCharacters();
                target1.addFriendliness(-2);
                target2.addFriendliness(2);
                console.log(`${target1.name} -2 友好, ${target2.name} +2 友好`);
            }
        },
        {
            name: "蝴蝶效應",
            effect: (culprit, area, scriptWriter) => {
                const target = scriptWriter.chooseCharacterInArea(area);
                const stat = scriptWriter.chooseStat(["anxiety", "friendliness", "conspiracyPoints"]);
                target[stat] += 1;
                console.log(`${target.name} 的 ${stat} +1`);
            }
        },
        {
            name: "褻瀆",
            effect: (shrine) => {
                shrine.addConspiracyPoints(2);
                console.log(`神社 +2 陰謀`);
            }
        }
    ],
    roles: {
        major: [
            {
                name: "關鍵人物",
                traits: [],
                abilities: [
                    {
                        type: "passive",
                        description: "死亡時腳本家勝利，輪迴結束",
                        trigger: (character, game) => {
                            if (character.isDead) {
                                console.log(`關鍵人物 ${character.name} 死亡，腳本家勝利`);
                                game.scriptWriter.winCycle();
                            }
                        }
                    }
                ]
            },
            {
                name: "殺手",
                traits: ["友好無視"],
                abilities: [
                    {
                        type: "passive",
                        description: "夜晚階段時，殺害同地區且陰謀>1的關鍵人物",
                        trigger: (character, game) => {
                            const area = character.currentArea;
                            const target = area.findCharacter(
                                char => char.role === "關鍵人物" && char.conspiracyPoints > 1
                            );
                            if (target) {
                                target.die();
                                console.log(`${character.name} 殺害了 ${target.name}`);
                            }
                        }
                    },
                    {
                        type: "passive",
                        description: "夜晚階段時，陰謀>3，腳本家勝利，輪迴結束",
                        trigger: (character, game) => {
                            if (character.conspiracyPoints > 3) {
                                console.log(`殺手 ${character.name} 陰謀 > 3，腳本家勝利`);
                                game.scriptWriter.winCycle();
                            }
                        }
                    }
                ]
            },
            {
                name: "黑幕",
                traits: ["友好無視"],
                abilities: [
                    {
                        type: "active",
                        description: "同地區其他角色或地區+1陰謀",
                        effect: (character, scriptWriter) => {
                            const target = scriptWriter.chooseTargetOrArea(character.currentArea);
                            if (target instanceof Character) {
                                target.addConspiracyPoints(1);
                                 if (isScriptwriterView) {
                                    console.log(`${target.name} +1 陰謀`);
                                }
                                console.log(`${target.name} +1 陰謀`);
                            } else {
                                target.addConspiracyPoints(1);
                                 if (isScriptwriterView) {
                                    console.log(`${target.name} +1 陰謀`);
                                }
                            }
                        }
                    }
                ]
            },
           {
                  name: "邪教徒",
                  traits: ["友好無效"],
                  abilities: [
                    {
                      type: "passive",
                      description: "行動結算階段，取消此地區偵探設置的陰謀禁止卡片",
                      effect: (area, isScriptwriterView) => {
                        area.removeConspiracyBan();
                        if (isScriptwriterView) {
                          console.log(`陰謀禁止卡片在地區 ${area.name} 被取消`);
                        }
                      }
                    }
                  ]
                },
                {
                  name: "魔女",
                  traits: ["友好無效"],
                  abilities: []
                },
                {
                  name: "時間旅行者",
                  traits: ["無法被殺害"],
                  abilities: [
                    {
                      type: passive,
                      description: "最後一天夜晚階段，若友好值<2，腳本家勝利，輪迴結束",
                      effect: (character, gameState, isScriptwriterView) => {
                        if (gameState.currentDay === gameState.finalDay && character.friendship < 2) {
                          gameState.endLoop("腳本家勝利");
                          if (isScriptwriterView) {
                            console.log(`${character.name} 的友好值不足，腳本家勝利`);
                          }
                        }
                      }
                    }
                  ]
                },
            
                    ],
        minor: [
            {
                name: "朋友",
                traits: [],
                abilities: [
                    {
                        type: "passive",
                        description: "輪迴結束死亡時，腳本家勝利並公開身分",
                        trigger: (character, game) => {
                            if (character.isDead) {
                                console.log(`朋友 ${character.name} 死亡，腳本家勝利`);
                                game.scriptWriter.winCycle();
                            }
                        }
                    }
                ]
            },
            
            {
              "name": "誤導者",
              "traits": [],
              "abilities": [
                {
                  "type": "active",
                  "description": "能力階段對同地區角色+1不安",
                  "effect": (target, isScriptwriterView) => {
                    target.addAnxiety(1);
                    if (isScriptwriterView) {
                      console.log(`${target.name} +1 不安`);
                    }
                  }
                }
              ]
            },
            {
              "name": "戀人",
              "traits": [],
              "abilities": [
                {
                  "type": "passive",
                  "description": "死亡時使情人+6不安",
                  "effect": (partner, isScriptwriterView) => {
                    partner.addAnxiety(6);
                    if (isScriptwriterView) {
                      console.log(`情人增加 6 不安`);
                    }
                  }
                }
              ]
            },
            {
              "name": "情人",
              "traits": [],
              "abilities": [
                {
                  "type": "passive",
                  "description": "死亡時使戀人+6不安",
                  "effect": (partner, isScriptwriterView) => {
                    partner.addAnxiety(6);
                    if (isScriptwriterView) {
                      console.log(`戀人增加 6 不安`);
                    }
                  }
                },
                {
                  "type": "passive",
                  "description": "夜晚階段若不安>3且陰謀值>0，腳本家勝利，輪迴結束",
                  "effect": (character, gameState, isScriptwriterView) => {
                    if (character.anxiety > 3 && character.conspiracy > 0) {
                      gameState.endLoop("腳本家勝利");
                      if (isScriptwriterView) {
                        console.log(`因為 ${character.name} 的條件滿足，腳本家勝利`);
                      }
                    }
                  }
                }
              ]
            },
            {
              "name": "殺人魔",
              "traits": [],
              "abilities": [
                {
                  "type": "passive",
                  "description": "夜晚階段若與其他角色獨處，殺害該角色",
                  "effect": (character, targets, isScriptwriterView) => {
                    if (targets.length === 1) {
                      targets[0].kill();
                      if (isScriptwriterView) {
                        console.log(`${targets[0].name} 被 ${character.name} 殺害`);
                      }
                    }
                  }
                }
              ]
            },
            {
              "name": "因子",
              "traits": ["友好無效"],
              "abilities": [
                {
                  "type": "passive",
                  "description": "學校陰謀值>1時，獲得誤導者能力",
                  "effect": (area, character, isScriptwriterView) => {
                    if (area.name === "學校" && area.conspiracy > 1) {
                      character.gainAbility("能力階段對同地區角色+1不安");
                      if (isScriptwriterView) {
                        console.log(`${character.name} 獲得了誤導者能力`);
                      }
                    }
                  }
                },
        {
          "type": "passive",
          "description": "鬧區陰謀值>1時，獲得關鍵人物能力",
          "effect": (area, character, isScriptwriterView) => {
            if (area.name === "鬧區" && area.conspiracy > 1) {
              character.gainAbility("死亡時，腳本家勝利，輪迴結束");
              if (isScriptwriterView) {
                console.log(`${character.name} 獲得了關鍵人物能力`);
              }
            }
          }
        }
      ]
    }
  ]
}        ]
    },
    mainRules: [
        {
            name: "殺人計畫",
            description: "關鍵人物*1、殺手*1、黑幕*1"
        },
        {
            name: "被封印之物",
            description: "黑幕*1、邪教徒*1，神社陰謀>1時輪迴結束，腳本家勝利"
        },
        {
            name: "和我簽下契約吧！",
            description: "關鍵人物*1，陰謀>1時腳本家勝利，必須設定角色關鍵人物為少女"
        }
    ]
};

// 輸入到遊戲系統
game.addMainRule(BasicTragedyX);



