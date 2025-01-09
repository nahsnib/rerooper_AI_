// 主要規則表框架

// 規則表主體
class RuleTable {
    constructor() {
        this.mainRules = []; // 主規則Y列表
        this.subRules = [];  // 副規則X列表
        this.Event = [];    // 事件列表
        this.Role = [];    // 身分列表
        this.SpecialRule = []; // 特殊規則 
    }
    // 顯示所有規則
    displayRules() {
        console.log("主規則:");
        this.mainRules.forEach((rule, index) => {
            console.log(`${index + 1}. ${rule.name}: ${rule.description}`);
        });
        console.log("副規則:");
        this.subRules.forEach((rule, index) => {
            console.log(`${index + 1}. ${rule.name}: ${rule.description}`);
        });
    }
}

// 事件類
class Event {
    constructor(name, effect) {
        this.name = name; // 事件名稱
        this.effect = effect; // 事件效果描述
    }
}

// 身分類
class Role {
    constructor(name, traits = [], abilities = []) {
        this.name = name; // 身分名稱
        this.traits = traits; // 特性列表
        this.abilities = abilities; // 能力列表
    }

// 規則類
class Rule {
    constructor(name, description, specialConditions = [], roles = []) {
        this.name = name; // 規則名稱
        this.description = description; // 規則描述
        this.specialConditions = specialConditions; // 特殊條件列表
        this.roles = roles; // 涉及的身分列表
    }
}

// 能力類
class Ability {
    constructor(name, type, effect) {
        this.name = name; // 能力名稱
        this.type = type; // 能力類型 ("主動" 或 "被動")
        this.effect = effect; // 能力效果描述
    }
}

// 顯示所有規則
ruleTable.load_RuleTable();

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



